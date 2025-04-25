import os
import yaml

def load_resource_config():
    """
    Load and separate public and internal resource configuration files.

    Returns:
        dict: Dictionary with keys 'public' and 'internal' for both configs.
    """
    config = {
        "public": {},
        "internal": {}
    }

    # Public config (bundled with the package)
    public_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "resources_public.yaml")
    )
    if os.path.exists(public_path):
        with open(public_path, "r") as f:
            config["public"] = yaml.safe_load(f) or {}

    # Internal config (~/.sima-cli/resources_internal.yaml)
    internal_path = os.path.join(os.path.expanduser("~"), ".sima-cli", "resources_internal.yaml")
    if os.path.exists(internal_path):
        with open(internal_path, "r") as f:
            config["internal"] = yaml.safe_load(f) or {}

    return config
