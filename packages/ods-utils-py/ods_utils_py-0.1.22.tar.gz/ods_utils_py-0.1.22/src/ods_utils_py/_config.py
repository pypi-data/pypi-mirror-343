"""
This module is responsible for loading environment variables from the environment file.
"""
from dotenv import load_dotenv
from pathlib import Path
import os

current_dir = Path(__file__).resolve().parent

environment_filename = ".ods_utils_py.env"

project_root = current_dir
while not (project_root / environment_filename).exists():
    if project_root.parent == project_root:
        raise FileNotFoundError(f"Could not find the {environment_filename} file in any parent directory")
    project_root = project_root.parent

env_path = project_root / environment_filename
load_dotenv(env_path)

def _check_all_environment_variables_are_set():
    environment_variables = ["ODS_API_KEY",
                             "USE_PROXY",
                             "PROXY_USER",
                             "PROXY_PASSWORD",
                             "PROXY_ADDRESS",
                             "PROXY_PORT",
                             "ODS_DOMAIN",
                             "ODS_API_TYPE"]

    for environment_variable in environment_variables:
        ev = os.getenv(environment_variable)
        if not ev:
            raise ValueError(f"{environment_variable} not found in the {environment_filename} file. "
                             f"Please define it as '{environment_variable}'.")
        if ev == "your_" + environment_variable.lower():
            raise ValueError(f"Please define the environment variable '{environment_variable}' in the {environment_filename} file.")


def get_base_url() -> str:
    return _get_ods_url()

def _get_ods_url() -> str:
    """
    Constructs the ODS (Open Data Service) API URL based on environment variables.

    Returns:
        str: The constructed ODS API URL **without** trailing slash ('/'): https://<ODS_DOMAIN>/api/<ODS_API_TYPE>
    """
    _ods_domain = os.getenv('ODS_DOMAIN')
    _ods_api_type = os.getenv('ODS_API_TYPE')
    _url_no_prefix = f"{_ods_domain}/api/{_ods_api_type}".replace("//", "/")
    _url = "https://" + _url_no_prefix
    return _url

def _get_headers():
    _api_key = os.getenv('ODS_API_KEY')
    _headers = {'Authorization': f'apikey {_api_key}'}
    return _headers

def _get_proxies() -> dict[str, str]:
    use_proxy = os.getenv("USE_PROXY")
    if use_proxy.lower() == 'false':
        proxies = None

    elif use_proxy.lower() == 'true':
        proxy_user = os.getenv("PROXY_USER")
        proxy_password = os.getenv("PROXY_PASSWORD")
        proxy_address = os.getenv("PROXY_ADDRESS")
        proxy_port = os.getenv("PROXY_PORT")

        proxy = f"http://{proxy_user}:{proxy_password}@{proxy_address}:{proxy_port}/"
        proxies = {
            "http": proxy,
            "https": proxy,
        }

    else:
        raise ValueError(f"The value USE_PROXY in the .ods_utils_py.env is {use_proxy}, but should be 'true' or 'false' "
                         f"(case insensitive)")

    return proxies
