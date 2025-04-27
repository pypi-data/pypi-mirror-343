"""Generated (extended for usability).

Provide convenient field flags *or* --file to read raw JSON/YAML body.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

import yaml
from typer import Typer, Option, Argument

from igniteops_sdk.client import AuthenticatedClient
from igniteops_sdk.types import UNSET
from ignite.utils.output import show
from ignite.client import API_BASE, TOKEN_FILE

from igniteops_sdk.models.project_create_request import ProjectCreateRequest
from igniteops_sdk.models.integration_repository_create_request import (
    IntegrationRepositoryCreateRequest,
    IntegrationRepositoryCreateRequestAccountType,
    IntegrationRepositoryCreateRequestProvider,
)

from igniteops_sdk.api.integrations.create_repository import sync as create_repository_sync
from igniteops_sdk.api.projects.create_project import sync as create_project_sync
from igniteops_sdk.api.subscriptions.create_subscription import sync as create_subscription_sync

app = Typer(help="Create commands.")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sdk_client() -> AuthenticatedClient:
    token = None
    try:
        if TOKEN_FILE.exists():
            token = TOKEN_FILE.read_text().strip()
    except Exception:
        pass
    return AuthenticatedClient(base_url=API_BASE, token=token or "")


def _read_body_file(file_path: str) -> dict:
    """Read JSON / YAML from *file_path* ('-' for stdin)."""

    data_str = sys.stdin.read() if file_path == "-" else Path(file_path).read_text()
    try:
        return json.loads(data_str)
    except json.JSONDecodeError:
        return yaml.safe_load(data_str)


@app.command("repository")
def create_repository(
    # file override
    file: Optional[str] = Option(
        None,
        "--file",
        "-f",
        help="Path to JSON/YAML body file or '-' for STDIN. Overrides field flags.",
    ),
    # required fields
    account_name: Optional[str] = Option(None, help="VCS account / org name"),
    account_type: Optional[str] = Option(None, help="Account type (user|organization)"),
    name: Optional[str] = Option(None, help="Repository name"),
    provider: Optional[str] = Option(None, help="Provider (github|gitlab|bitbucket)"),
    token: Optional[str] = Option(None, help="Access token"),
    # optional
    api_endpoint: Optional[str] = Option(None, help="Custom API endpoint (self-hosted)"),
    # output
    json_: bool = Option(False, "--json", help="Output as raw JSON"),
    yaml_: bool = Option(False, "--yaml", help="Output as raw YAML"),
):
    """Create a repository integration."""

    client = _sdk_client()

    if file:
        body_dict = _read_body_file(file)
        body_obj = IntegrationRepositoryCreateRequest.from_dict(body_dict)  # type: ignore[arg-type]
    else:
        if not all([account_name, account_type, name, provider, token]):
            raise ValueError("Missing required fields. Provide --file or all mandatory flags.")

        body_obj = IntegrationRepositoryCreateRequest(
            account_name=account_name,
            account_type=IntegrationRepositoryCreateRequestAccountType(account_type),
            name=name,
            provider=IntegrationRepositoryCreateRequestProvider(provider),
            token=token,
            api_endpoint=api_endpoint if api_endpoint is not None else UNSET,
        )

    resp = create_repository_sync(client=client, body=body_obj)
    show(resp, raw_json=json_, raw_yaml=yaml_)


@app.command("project")
def create_project(
    # file override
    file: Optional[str] = Option(None, "--file", "-f", help="Path to JSON/YAML body file or '-' for STDIN."),
    # required fields
    project_name: Optional[str] = Option(None, "--name", help="Project name"),
    description: Optional[str] = Option(None, "--description", help="Project description"),
    language: Optional[str] = Option(None, "--language", help="Language, e.g. python|node"),
    framework: Optional[str] = Option(None, "--framework", help="Framework name"),
    integration_id: Optional[str] = Option(None, "--integration-id", help="Integration ID"),
    # optional
    connection_id: Optional[str] = Option(None, "--connection-id", help="Connection ID"),
    repository_name: Optional[str] = Option(None, "--repository-name", help="Repository name"),
    # output
    json_: bool = Option(False, "--json", help="Output as raw JSON"),
    yaml_: bool = Option(False, "--yaml", help="Output as raw YAML"),
):
    """Create a new project."""

    client = _sdk_client()

    if file:
        body_dict = _read_body_file(file)
        body_obj = ProjectCreateRequest.from_dict(body_dict)  # type: ignore[arg-type]
    else:
        # validate required fields
        required = [project_name, description, language, framework, integration_id]
        if not all(required):
            raise ValueError("Missing required fields. Provide --file or all mandatory flags.")

        kwargs = dict(
            project_name=project_name,
            description=description,
            language=language,
            framework=framework,
            integration_id=integration_id,
            connection_id=connection_id if connection_id else UNSET,
            repository_name=repository_name if repository_name else UNSET,
        )
        body_obj = ProjectCreateRequest(**kwargs)  # type: ignore[arg-type]

    resp = create_project_sync(client=client, body=body_obj)
    show(resp, raw_json=json_, raw_yaml=yaml_)


@app.command("subscription")
def create_subscription(
    file: str = Argument(..., help="Path to JSON/YAML body file or '-' for STDIN."),
    json_: bool = Option(False, "--json", help="Output as raw JSON"),
    yaml_: bool = Option(False, "--yaml", help="Output as raw YAML"),
):
    """Create a new subscription (file input only for now)."""

    body_dict = _read_body_file(file)
    client = _sdk_client()
    resp = create_subscription_sync(client=client, body=body_dict)  # type: ignore[arg-type]
    show(resp, raw_json=json_, raw_yaml=yaml_)
