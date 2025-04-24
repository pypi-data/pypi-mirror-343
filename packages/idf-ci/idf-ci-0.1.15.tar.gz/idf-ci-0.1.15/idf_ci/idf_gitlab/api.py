# SPDX-FileCopyrightText: 2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import re
import typing as t
from datetime import timedelta
from functools import lru_cache
from pathlib import Path

import minio
from gitlab import Gitlab
from gitlab.v4.objects import MergeRequest

from .._vendor import translate
from ..envs import GitlabEnvVars
from ..settings import CiSettings
from ..utils import get_current_branch
from .s3 import create_s3_client, download_from_s3, upload_to_s3

logger = logging.getLogger(__name__)


class ArtifactManager:
    """Tool interface for managing artifacts in GitLab pipelines.

    This class provides a unified interface for downloading and uploading artifacts,
    supporting both GitLab's built-in storage and S3 storage. It handles:

    1. GitLab API operations (pipeline, merge request queries)
    2. S3 storage operations (artifact upload/download)
    3. Fallback to GitLab storage when S3 is not configured

    :var env: GitLab environment variables
    :var settings: CI settings
    """

    def __init__(self):
        self.env = GitlabEnvVars()
        self.settings = CiSettings()

    @property
    @lru_cache()
    def gl(self):
        return Gitlab(
            self.env.GITLAB_HTTPS_SERVER,
            private_token=self.env.GITLAB_ACCESS_TOKEN,
        )

    @property
    @lru_cache()
    def project(self):
        """Lazily initialize and cache the GitLab project."""
        project = self.gl.projects.get(self.settings.gitlab.project)
        if not project:
            raise ValueError(f'Project {self.settings.gitlab.project} not found')
        return project

    def get_mr_obj_by_branch(self, branch: str) -> MergeRequest:
        """Get a merge request by its branch name.

        :param branch: Branch name of the merge request to get

        :returns: The merge request object
        """
        mrs = self.project.mergerequests.list(state='opened', source_branch=branch)
        if not mrs:
            raise ValueError(f'No open merge request found for branch {branch}')
        return mrs[0]

    def _get_upload_details_by_type(self, artifact_type: t.Optional[str]) -> t.Dict[str, t.List[str]]:
        """Get file patterns grouped by bucket name based on the artifact type.

        :param artifact_type: Type of artifacts to download (debug, flash, metrics)

        :returns: Dictionary mapping bucket names to lists of patterns

        :raises ValueError: If the artifact type is invalid
        """
        if artifact_type:
            if artifact_type not in self.settings.gitlab.artifacts.available_s3_types:
                raise ValueError(
                    f'Invalid artifact type: {artifact_type}. '
                    f'Available types: {self.settings.gitlab.artifacts.available_s3_types}'
                )
            config = self.settings.gitlab.artifacts.s3[artifact_type]
            return {config['bucket']: config['patterns']}
        else:
            # If no type specified, return all configurations grouped by bucket
            bucket_patterns: t.Dict[str, t.List[str]] = {}
            for config in self.settings.gitlab.artifacts.s3.values():
                bucket = config['bucket']
                if bucket not in bucket_patterns:
                    bucket_patterns[bucket] = []
                bucket_patterns[bucket].extend(config['patterns'])

            if not bucket_patterns:
                raise ValueError('No S3 buckets configured')
            return bucket_patterns

    def download_artifacts(
        self,
        commit_sha: t.Optional[str] = None,
        branch: t.Optional[str] = None,
        artifact_type: t.Optional[str] = None,
        folder: t.Optional[str] = None,
    ) -> None:
        """Download artifacts from a pipeline.

        This method downloads artifacts from either GitLab's built-in storage or S3
        storage, depending on the configuration and artifact type.

        There are two main use cases:

        1. CI use case: Use commit_sha to download artifacts from a specific commit
        2. Local use case: Use branch to download artifacts from the latest pipeline of
           a branch

        :param commit_sha: Optional commit SHA. If provided, will download from this
            specific commit
        :param branch: Optional Git branch. If no commit_sha provided, will use current
            branch
        :param artifact_type: Type of artifacts to download (debug, flash, metrics)
        :param folder: download artifacts under this folder
        """
        if folder is None:
            folder = os.getcwd()
        from_path = Path(folder)

        # Get the commit SHA
        if commit_sha:
            pass
        else:
            # Local use case: Use latest commit of the remote branch
            if branch is None:
                branch = get_current_branch()
                logger.debug(f'Using current branch: {branch}')
            else:
                logger.debug(f'Using specified branch: {branch}')

            # Check if MR exists for this branch
            mr = self.get_mr_obj_by_branch(branch)
            commit_sha = next(mr.commits()).id

        s3_client = create_s3_client()
        if s3_client:
            s3_prefix = f'{self.settings.gitlab.project}/{commit_sha}/'
            logger.info(f'Downloading artifacts under {from_path} from s3 (commit sha: {commit_sha})')

            for bucket, patterns in self._get_upload_details_by_type(artifact_type).items():
                download_from_s3(
                    s3_client=s3_client,
                    bucket=bucket,
                    prefix=s3_prefix,
                    from_path=from_path,
                    patterns=patterns,
                )
        else:
            # TODO:
            # - get the latest pipeline for the commit
            # - get job `upload_presigned_urls_json`
            # - download artifact `presigned_urls.json`
            # - download artifacts listed in `presigned_urls.json`
            raise ValueError('Configure S3 storage to download artifacts')

    def upload_artifacts(
        self,
        *,
        commit_sha: str,
        artifact_type: t.Optional[str] = None,
        folder: t.Optional[str] = None,
    ) -> None:
        """Upload artifacts to S3 storage.

        This method uploads artifacts to S3 storage only. GitLab's built-in storage is
        not supported. The commit SHA is required to identify where to store the
        artifacts.

        :param commit_sha: Commit SHA to upload artifacts to
        :param artifact_type: Type of artifacts to upload (debug, flash, metrics)
        :param folder: upload artifacts under this folder

        :raises ValueError: If commit_sha is not provided or S3 is not configured
        """
        if folder is None:
            folder = os.getcwd()
        from_path = Path(folder)

        if not commit_sha:
            raise ValueError('Commit SHA is required to upload artifacts')

        s3_client = create_s3_client()
        if not s3_client:
            raise ValueError('Configure S3 storage to upload artifacts')

        prefix = f'{self.settings.gitlab.project}/{commit_sha}/'
        logger.info(f'Uploading artifacts under {from_path} to s3 (commit sha: {commit_sha})')

        for bucket, patterns in self._get_upload_details_by_type(artifact_type).items():
            upload_to_s3(
                s3_client=s3_client,
                bucket=bucket,
                prefix=prefix,
                from_path=from_path,
                patterns=patterns,
            )

    def generate_presigned_json(
        self,
        *,
        commit_sha: str,
        artifact_type: t.Optional[str] = None,
        folder: t.Optional[str] = None,
        expire_in_days: int = 4,
    ) -> t.Dict[str, str]:
        """Generate presigned URLs for artifacts in S3 storage.

        This method generates presigned URLs for artifacts that would be uploaded to S3
        storage. The URLs can be used to download the artifacts directly from S3.

        :param commit_sha: Commit SHA to generate presigned URLs for
        :param artifact_type: Type of artifacts to generate URLs for (debug, flash,
            metrics)
        :param folder: Base folder to generate relative paths from
        :param expire_in_days: Expiration time in days for the presigned URLs (default:
            4 days)

        :returns: Dictionary mapping relative paths to presigned URLs

        :raises ValueError: If commit_sha is not provided or S3 is not configured
        """
        if folder is None:
            folder = os.getcwd()
        from_path = Path(folder)

        if not commit_sha:
            raise ValueError('Commit SHA is required to generate presigned URLs')

        s3_client = create_s3_client()
        if not s3_client:
            raise ValueError('Configure S3 storage to generate presigned URLs')

        env = GitlabEnvVars()

        prefix = f'{self.settings.gitlab.project}/{commit_sha}/'
        rel_path = str(from_path.relative_to(env.IDF_PATH))
        if rel_path != '.':
            s3_path = f'{prefix}{rel_path}'
        else:
            s3_path = prefix

        presigned_urls: t.Dict[str, str] = {}
        for bucket, patterns in self._get_upload_details_by_type(artifact_type).items():
            patterns_regexes = [
                re.compile(translate(pattern, recursive=True, include_hidden=True)) for pattern in patterns
            ]

            for obj in s3_client.list_objects(
                bucket,
                prefix=s3_path,
                recursive=True,
            ):
                try:
                    output_path = Path(env.IDF_PATH) / obj.object_name.replace(prefix, '')
                    rel_path = obj.object_name.replace(prefix, '')

                    if not any(pattern.match(str(output_path)) for pattern in patterns_regexes):
                        continue

                    presigned_url = s3_client.get_presigned_url(
                        'GET',
                        bucket_name=bucket,
                        object_name=obj.object_name,
                        expires=timedelta(days=expire_in_days),
                    )
                    presigned_urls[rel_path] = presigned_url
                except minio.error.S3Error as e:
                    logger.error(f'Error presigning from S3: {e}')
                    raise

        return presigned_urls
