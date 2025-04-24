from google.oauth2 import service_account
from kfp.registry import RegistryClient
from google.cloud import artifactregistry_v1
from logging import getLogger

logger = getLogger()

class ArtifactRegistryHelper():

    def __init__(self, project_id, location):
        self.project_id = project_id
        self.location = location
        self.client = artifactregistry_v1.ArtifactRegistryClient()

    def check_repository(self, repository_id: str):

        parent = f'projects/{self.project_id}/locations/{self.location}'

        repos = self.client.list_repositories(parent=parent)

        for repo in repos:
            if repository_id in repo.name:
                return True
            else:
                return False

    def create_repository(self, repository_id: str, repository_format: str):

        if self.check_repository(repository_id):
            logger.info(f"Repository '{repository_id}' already exists.")
            return

        parent = f'projects/{self.project_id}/locations/{self.location}'

        if repository_format == 'docker':
            format = artifactregistry_v1.Repository.Format.DOCKER
        elif repository_format == 'kfp':
            format = artifactregistry_v1.Repository.Format.KFP
        else:
            raise ValueError(f"Invalid repository format: {repository_format}. Expected 'docker' or 'kfp'.")

        repository = artifactregistry_v1.Repository(
            name = f'{parent}/repositories/{repository_id}',
            format_ = format
        )

        operations = self.client.create_repository(parent=parent, repository_id=repository_id, repository=repository)

        response = operations.result()
        logger.info(f'Repository created: {response.name}')

    def upload_file_to_repository(self, repository_id: str, file_path: str, description: str = None, tags: list = None):

        if tags == None:
            tags = []

        host = f"https://{self.location}-kfp.pkg.dev/{self.project_id}/{repository_id}"
        client = RegistryClient(host=host)

        template_name, version_name = client.upload_pipeline(
            file_name=file_path,
            extra_headers={"description": description},
            tags = tags
        )
        logger.info(f"Successfully uploaded file as '{template_name}', version '{version_name}'.")