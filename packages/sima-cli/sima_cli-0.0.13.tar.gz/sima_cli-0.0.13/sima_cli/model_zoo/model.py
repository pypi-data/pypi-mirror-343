# model_zoo/models.py

import requests
import click
import os
from urllib.parse import urlparse

from sima_cli.utils.config import get_auth_token
from sima_cli.download import download_file_from_url

ARTIFACTORY_BASE_URL = "https://artifacts.eng.sima.ai:443/artifactory"

def _is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def _download_model_internal(ver: str, model_name: str):
    repo = "sima-qa-releases"
    base_path = f"SiMaCLI-SDK-Releases/{ver}-Release/modelzoo_edgematic/{model_name}"
    aql_query = f"""
                items.find({{
                "repo": "{repo}",
                "path": {{
                    "$match": "{base_path}*"
                }},
                "type": "file"
                }}).include("repo", "path", "name")
                """.strip()

    aql_url = f"{ARTIFACTORY_BASE_URL}/api/search/aql"
    headers = {
        "Content-Type": "text/plain",
        "Authorization": f"Bearer {get_auth_token(internal=True)}"
    }

    response = requests.post(aql_url, data=aql_query, headers=headers)
    if response.status_code != 200:
        click.echo(f"Failed to list model files. Status: {response.status_code}, path: {aql_url}")
        click.echo(response.text)
        return

    results = response.json().get("results", [])
    if not results:
        click.echo(f"No files found for model: {model_name}")
        return

    dest_dir = os.path.join(os.getcwd(), model_name)
    os.makedirs(dest_dir, exist_ok=True)

    click.echo(f"Downloading files for model '{model_name}' to '{dest_dir}'...")

    for item in results:
        file_path = item["path"]
        file_name = item["name"]
        download_url = f"{ARTIFACTORY_BASE_URL}/{repo}/{file_path}/{file_name}"

        try:
            local_path = download_file_from_url(download_url, dest_folder=dest_dir, internal=True)
            click.echo(f"✅ {file_name} -> {local_path}")
        except Exception as e:
            click.echo(f"❌ Failed to download {file_name}: {e}")

    # Check for model_path.txt and optionally download external ONNX model
    model_path_file = os.path.join(dest_dir, "model_path.txt")
    if os.path.exists(model_path_file):
        with open(model_path_file, "r") as f:
            first_line = f.readline().strip()
            if _is_valid_url(first_line):
                click.echo(f"\n🔍 model_path.txt contains external model link:\n{first_line}")
                if click.confirm("Do you want to download the FP32 ONNX model from this link?", default=True):
                    try:
                        external_model_path = download_file_from_url(first_line, dest_folder=dest_dir, internal=True)
                        click.echo(f"✅ External model downloaded to: {external_model_path}")
                    except Exception as e:
                        click.echo(f"❌ Failed to download external model: {e}")
            else:
                click.echo("⚠️ model_path.txt exists but does not contain a valid URL.")

def _list_available_models_internal(version: str):
    repo_path = f"SiMaCLI-SDK-Releases/{version}-Release/modelzoo_edgematic"
    aql_query = f"""
                items.find({{
                "repo": "sima-qa-releases",
                "path": {{
                    "$match": "{repo_path}/*"
                }},
                "type": "folder"
                }}).include("repo", "path", "name")
                """.strip()

    aql_url = f"{ARTIFACTORY_BASE_URL}/api/search/aql"
    headers = {
        "Content-Type": "text/plain",
        "Authorization": f"Bearer {get_auth_token(internal=True)}"
    }

    response = requests.post(aql_url, data=aql_query, headers=headers)

    if response.status_code != 200:
        click.echo(f"Failed to retrieve model list. Status: {response.status_code}")
        click.echo(response.text)
        return

    results = response.json().get("results", [])
    
    base_prefix = f"SiMaCLI-SDK-Releases/{version}-Release/modelzoo_edgematic/"
    model_paths = sorted({
        item["path"].replace(base_prefix, "").rstrip("/") + "/" + item["name"]
        for item in results
    })

    if not model_paths:
        click.echo("No models found.")
        return

    # Pretty print table
    max_len = max(len(name) for name in model_paths)
    click.echo(f"{'-' * max_len}")
    for path in model_paths:
        click.echo(path.ljust(max_len))

    return model_paths

def list_models(internal, ver):
    if internal:
        click.echo("Model Zoo Source : SiMa Artifactory...")
        return _list_available_models_internal(ver)
    else:
        print('External model zoo not supported yet')

def download_model(internal, ver, model_name):
    if internal:
        click.echo("Model Zoo Source : SiMa Artifactory...")
        return _download_model_internal(ver, model_name)
    else:
        print('External model zoo not supported yet')

# Module CLI tests
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python models.py <version>")
    else:
        version_arg = sys.argv[1]
        _list_available_models_internal(version_arg)
