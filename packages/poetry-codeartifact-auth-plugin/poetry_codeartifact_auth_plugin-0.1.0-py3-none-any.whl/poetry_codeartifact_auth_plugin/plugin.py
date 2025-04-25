import re

import boto3
from cleo.io.io import IO
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry
from tomlkit import TOMLDocument


class CodeartifactLoginPlugin(Plugin):
    def find_sources(self, data: TOMLDocument) -> list:
        sources = data.get("tool", {}).get("poetry", {}).get("source", [])
        if not sources:
            return []
        if not isinstance(sources, list):
            sources = [sources]
        for source in sources:
            if not isinstance(source, dict):
                raise ValueError("Source must be a dictionary")
            if "name" not in source or "url" not in source:
                raise ValueError("Source must have 'name' and 'url' keys")
        return sources

    def find_codeartifact_sources(self, data: TOMLDocument) -> list:
        sources = self.find_sources(data)
        return [source for source in sources if "codeartifact" in source["url"]]

    def get_codeartifact_credentials(self, source: dict) -> dict:
        client = boto3.client("codeartifact")
        try:
            domain_data = re.match(
                r"^https://(?P<domain>[^.]+)\.d\.codeartifact", source["url"]
            )
            if not domain_data:
                raise ValueError("Invalid CodeArtifact URL")
            domain, domain_owner = domain_data.group(1).split("-")
            response = client.get_authorization_token(
                domain=domain,
                domainOwner=domain_owner,
            )
            auth_token = response.get("authorizationToken")
            if not auth_token:
                raise ValueError("Failed to get authorization token")
            return auth_token
        finally:
            client.close()

    def activate(self, poetry: Poetry, io: IO):
        for source in self.find_codeartifact_sources(poetry.pyproject.data):
            token = self.get_codeartifact_credentials(source)
            poetry.config.merge(
                config={
                    "http-basic": {
                        source["name"]: {"username": "aws", "password": token}
                    }
                },
            )
