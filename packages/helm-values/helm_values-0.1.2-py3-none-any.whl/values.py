import yaml
import os
import git
import tempfile
import re
from typing import Dict, Any, Tuple


def deep_merge(source: Dict[str, Any], destination: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries
    """
    for key, value in source.items():
        if (
            isinstance(value, dict)
            and key in destination
            and isinstance(destination[key], dict)
        ):
            # If both values are dictionaries, recursively merge them
            destination[key] = deep_merge(value, destination[key])
        else:
            # Otherwise, source value overrides destination
            destination[key] = value
    return destination


def load_helm_values(
    chart_name: str,
    cluster_name: str,
    common_values_path: str,
    cluster_values_path: str,
    *additional_files: str,
) -> Dict[str, Any]:
    """
    Load and merge Helm values files, later files are more important
    """
    paths = [
        # The default values of the Helm Chart
        os.path.join("charts", chart_name, "values.yaml"),
        # Common values for all clusters
        os.path.join(common_values_path, "common.yaml"),
        # Chart values for all Cluster
        os.path.join(common_values_path, f"{chart_name}.yaml"),
        # Common values for this Cluster
        os.path.join(cluster_values_path, cluster_name, "common.yaml"),
        # Chart values for this Cluster
        os.path.join(cluster_values_path, cluster_name, f"{chart_name}.yaml"),
        *additional_files,
    ]

    result: Dict[str, Any] = {}

    for path in paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                values = yaml.safe_load(f) or {}
                result = deep_merge(values, result)

    return result


def parse_git_url(url: str) -> Tuple[str, str]:
    """
    Parse a Git URL in the format https://git.domain.com/username/repo.git/path
    and return the repo URL and path within the repo
    """
    # Pattern to match a Git URL with an optional path
    pattern = r"(https?://[^/]+/[^/]+/[^/]+\.git)(?:/(.*))?$"
    match = re.match(pattern, url)

    if not match:
        raise ValueError(f"Invalid Git URL format: {url}")

    repo_url = match.group(1)
    path_in_repo = match.group(2) or ""

    return repo_url, path_in_repo


def load_helm_values_git(
    chart_name: str,
    cluster_name: str,
    common_values_path: str,
    cluster_values_path: str,
    git_ref: str = "master",
    *additional_files: str,
) -> Dict[str, Any]:
    """
    Load and merge Helm values files from Git URLs

    Handles paths formatted like: https://git.domain.com/username/repo.git/path
    """
    # Parse Git URLs
    repo_url, common_path = parse_git_url(common_values_path)
    _, cluster_path = parse_git_url(cluster_values_path)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Clone the repository
        repo = git.Repo.clone_from(repo_url, temp_dir)
        repo.git.checkout(git_ref)

        # Define paths relative to the repository root
        paths = [
            # The default values of the Helm Chart
            os.path.join(temp_dir, "charts", chart_name, "values.yaml"),
            # Common values for all clusters
            os.path.join(temp_dir, common_path, "common.yaml"),
            # Chart values for all Cluster
            os.path.join(temp_dir, common_path, f"{chart_name}.yaml"),
            # Common values for this Cluster
            os.path.join(temp_dir, cluster_path, cluster_name, "common.yaml"),
            # Chart values for this Cluster
            os.path.join(temp_dir, cluster_path, cluster_name, f"{chart_name}.yaml"),
        ]

        # Add additional files with proper path
        for file_path in additional_files:
            if file_path.startswith(("http://", "https://")):
                _, path_in_repo = parse_git_url(file_path)
                paths.append(os.path.join(temp_dir, path_in_repo))
            else:
                paths.append(os.path.join(temp_dir, file_path))

        result: Dict[str, Any] = {}

        for path in paths:
            if os.path.exists(path):
                with open(path, "r") as f:
                    values = yaml.safe_load(f) or {}
                    result = deep_merge(values, result)

        return result
