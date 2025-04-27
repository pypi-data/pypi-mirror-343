# mypy: ignore-errors

from __future__ import annotations

import os
from pathlib import Path

from click.testing import CliRunner
from kedro.framework.cli.starters import create_cli as kedro_cli
from kedro.framework.startup import bootstrap_project
from pytest import fixture


@fixture(name="cli_runner", scope="session")
def cli_runner():
    runner = CliRunner()
    yield runner


def _create_kedro_settings_py(file_name, patterns):
    patterns_str = ", ".join([f'"{p}"' for p in patterns])
    content = f"""CONFIG_LOADER_ARGS = {{
    "base_env": "base",
    "default_run_env": "local",
    "config_patterns": {{
        "dagster": [{patterns_str}],  # configure the pattern for configuration files
    }}
}}
"""
    file_name.write_text(content)


@fixture(scope="session")
def temp_directory(tmpdir_factory):
    # Use tmpdir_factory to create a temporary directory with session scope
    return tmpdir_factory.mktemp("session_temp_dir")  # type: ignore[no-any-return]


@fixture(scope="session")
def kedro_project(cli_runner, temp_directory):  # type: ignore[no-untyped-def]
    os.chdir(temp_directory)

    CliRunner().invoke(
        # Supply name, tools, and example to skip interactive prompts
        kedro_cli,
        [
            "new",
            "-v",
            "--name",
            "Fake Project",
            "--tools",
            "none",
            "--example",
            "no",
        ],
    )
    pipeline_registry_py = """
from kedro.pipeline import Pipeline, node


def identity(arg):
    return arg


def register_pipelines():
    pipeline = Pipeline(
        [
            node(identity, ["input"], ["intermediate"], name="node0", tags=["tag0", "tag1"]),
            node(identity, ["intermediate"], ["output"], name="node1"),
            node(identity, ["intermediate"], ["output2"], name="node2", tags=["tag0"]),
            node(identity, ["intermediate"], ["output3"], name="node3", tags=["tag1", "tag2"]),
            node(identity, ["intermediate"], ["output4"], name="node4", tags=["tag2"]),
        ],
        tags="pipeline0",
    )
    return {
        "__default__": pipeline,
        "ds": pipeline,
    }
    """

    project_path = Path(temp_directory.join("fake-project"))
    (project_path / "src" / "fake_project" / "pipeline_registry.py").write_text(pipeline_registry_py)

    settings_file = project_path / "src" / "fake_project" / "settings.py"
    _create_kedro_settings_py(settings_file, ["dagster*", "dagster/**"])

    os.chdir(project_path)
    return project_path


@fixture(scope="session")
def metadata(kedro_project):
    project_path = kedro_project.resolve()
    metadata = bootstrap_project(project_path)
    return metadata  # type: ignore[no-any-return]
