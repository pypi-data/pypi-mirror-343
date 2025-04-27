# API Reference

This section provides an overview and links to the Kedro-Dagster API documentation.

## Command Line Interface

Kedro-Dagster provides CLI commands to initialize and run the translation of your Kedro project into Dagster.

### `kedro dagster init`

Initializes Dagster integration for your Kedro project by generating the necessary `definitions.py` and configuration files.

::: kedro_dagster.cli.init

**Usage:**

```bash
uv run kedro dagster init --env <ENV_NAME> --force --silent
```

- `--env`: The Kedro environment where the `dagster.yml` should be created (default: `local`).
- `--force`: Overwrite existing files without prompting.
- `--silent`: Suppress output messages when files are modified.

### `kedro dagster dev`

Starts the Dagster development UI and launches your Kedro pipelines as Dagster jobs for interactive development and monitoring.

::: kedro_dagster.cli.dev

**Usage:**

```bash
uv run kedro dagster dev --env <ENV_NAME> --log-level <LEVEL> --log-format <FORMAT> --port <PORT> --host <HOST> --live-data-poll-rate <RATE>
```

- `--env`: The Kedro environment to use (e.g., `local`).
- `--log-level`: Logging level (`debug`, `info`, `warning`, `error`, or `critical`).
- `--log-format`: Log output format (`colored`, `json`, `default`).
- `--port`: Port for the Dagster UI.
- `--host`: Host address for the Dagster UI.
- `--live-data-poll-rate`: Polling rate for live data in milliseconds.

If specified, those options will override the ones specified in your `conf/<ENV_NAME>/dagster.yml`. See [`DevOptions`](#devoptions).

## Configuration

The following classes define the configuration schema for Kedro-Dagster's `dagster.yml`, using Pydantic models.

### `KedroDagsterConfig`

Main configuration class for Kedro-Dagster, representing the structure of the `dagster.yml` file.

::: kedro_dagster.config.kedro_dagster.KedroDagsterConfig

---

### `DevOptions`

Options for the `kedro dagster dev` command.

::: kedro_dagster.config.dev.DevOptions

---

### `JobOptions`

Configuration options for a Dagster job, including pipeline filtering, executor, and schedule.

::: kedro_dagster.config.job.JobOptions

---

### `PipelineOptions`

Options for filtering and configuring Kedro pipelines within jobs.

::: kedro_dagster.config.job.PipelineOptions

---

### `ExecutorOptions`

Base class for executor configuration. See specific executor option classes below.

::: kedro_dagster.config.execution.ExecutorOptions

---

#### `InProcessExecutorOptions`

Options for the in-process executor.

::: kedro_dagster.config.execution.InProcessExecutorOptions

---

#### `MultiprocessExecutorOptions`

Options for the multiprocess executor.

::: kedro_dagster.config.execution.MultiprocessExecutorOptions

---

#### `DaskExecutorOptions`

Options for the Dask executor.

::: kedro_dagster.config.execution.DaskExecutorOptions

where `DaskClusterConfig` is defined as:

::: kedro_dagster.config.execution.DaskClusterConfig

---

#### `DockerExecutorOptions`

Options for the Docker-based executor.

::: kedro_dagster.config.execution.DockerExecutorOptions

---

#### `CeleryExecutorOptions`

Options for the Celery-based executor.

::: kedro_dagster.config.execution.CeleryExecutorOptions

---

#### `CeleryDockerExecutorOptions`

Options for the Celery executor with Docker support.

::: kedro_dagster.config.execution.CeleryDockerExecutorOptions

---

#### `K8sJobExecutorOptions`

Options for the Kubernetes-based executor.

::: kedro_dagster.config.execution.K8sJobExecutorOptions

where `K8sJobConfig` is defined as:

::: kedro_dagster.config.execution.K8sJobConfig

---

#### `CeleryK8sJobExecutorOptions`

Options for the Celery executor with Kubernetes support.

::: kedro_dagster.config.execution.CeleryK8sJobExecutorOptions

where `K8sJobConfig` is defined as:

::: kedro_dagster.config.execution.K8sJobConfig

---

### `ScheduleOptions`

Options for defining Dagster schedules.

::: kedro_dagster.config.automation.ScheduleOptions

---

## Translation Modules

The following classes are responsible for translating Kedro concepts into Dagster constructs:

### `KedroProjectTranslator`

Translates an entire Kedro project into a Dagster code location, orchestrating the translation of pipelines, datasets, hooks, and loggers.

::: kedro_dagster.translator.KedroProjectTranslator

---

### `DagsterCodeLocation`

Collects the Dagster job, asset, resource, executor, schedule, sensor, and loggers definitions generated for the Kedro project-based Dagster code location.

::: kedro_dagster.translator.DagsterCodeLocation

---

### `CatalogTranslator`

Translates Kedro datasets into Dagster IO managers and assets, enabling seamless data handling between Kedro and Dagster.

::: kedro_dagster.catalog.CatalogTranslator

---

### `NodeTranslator`

Converts Kedro nodes into Dagster ops and assets, handling Kedro parameter passing.

::: kedro_dagster.nodes.NodeTranslator

---

### `PipelineTranslator`

Maps Kedro pipelines to Dagster jobs, supporting pipeline filtering, hooks, job configuration, and resource assignment.

::: kedro_dagster.pipelines.PipelineTranslator

---

### `KedroRunTranslator`

Manages translation of Kedro run parameters and hooks into Dagster resources and sensors, including error handling and context propagation.

::: kedro_dagster.kedro.KedroRunTranslator

---

### `ExecutorCreator`

Creates Dagster executors from configuration, allowing for granular execution strategies.

::: kedro_dagster.dagster.ExecutorCreator

---

### `LoggerTranslator`

Translates Kedro loggers to Dagster loggers for unified logging across both frameworks.

::: kedro_dagster.dagster.LoggerTranslator

---

### `ScheduleCreator`

Generates Dagster schedules from configuration, enabling automated pipeline execution.

::: kedro_dagster.dagster.ScheduleCreator

---

### Utilities

Helper functions for formatting, filtering, and supporting translation between Kedro and Dagster concepts.

::: kedro_dagster.utils
