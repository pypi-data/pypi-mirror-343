<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/gtauzin/kedro-dagster/main/docs/images/logo_light.png">
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gtauzin/kedro-dagster/main/docs/images/logo_dark.png">
    <img src="https://raw.githubusercontent.com/gtauzin/kedro-dagster/main/docs/images/logo_light.png" alt="Kedro-Dagster">
  </picture>
</p>

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)
[![Python Version](https://img.shields.io/pypi/pyversions/kedro-dagster)](https://pypi.org/project/kedro-dagster/)
[![License](https://img.shields.io/github/license/gtauzin/kedro-dagster)](https://github.com/gtauzin/kedro-dagster/blob/main/LICENSE.md)
[![PyPI Version](https://img.shields.io/pypi/v/kedro-dagster)](https://pypi.org/project/kedro-dagster/)
[![Run tests and checks](https://github.com/gtauzin/kedro-dagster/actions/workflows/check.yml/badge.svg)](https://github.com/gtauzin/kedro-dagster/actions/workflows/check.yml)
[![Slack Organisation](https://img.shields.io/badge/slack-chat-blueviolet.svg?label=Kedro%20Slack&logo=slack)](https://slack.kedro.org)

## What is Kedro-Dagster?

The Kedro-Dagster plugin enables seamless integration between [Kedro](https://kedro.readthedocs.io/), a framework for creating reproducible and maintainable data science code, and [Dagster](https://dagster.io/), a data orchestrator for machine learning and data pipelines. This plugin makes use of Dagster's orchestration capabilities to automate and monitor Kedro pipelines effectively.

## What are the features of Kedro-Dagster?

- **Configuration‑Driven Workflows:** Centralize orchestration settings in a `dagster.yml` file for each Kedro environment. Define jobs from filtered Kedro pipelines, assign executors, retries, resource limits, and cron-based schedules.
- **Customization:** The core integration lives in the auto‑generated Dagster `definitions.py`. For advanced use cases, you can extend or override these definitions.
- **Kedro Hooks Preservation:** Kedro hooks are preserved and called at the appropriate time during pipeline execution, so custom logic (e.g., data validation, logging) continues to work seamlessly.
- **MLflow Compatibility:** Use [Kedro-MLflow](https://github.com/Galileo-Galilei/kedro-mlflow) with Dagster’s [MLflow integration](https://dagster.io/integrations/dagster-mlflow) to track experiments, log models, and register artifacts.
- **Logger Integration:** Unifies Kedro and Dagster logging so logs from Kedro nodes appear in the Dagster UI and are easy to trace and debug.

## How to install Kedro-Dagster?

Install the Kedro-Dagster plugin using pip:

```bash
pip install kedro-dagster
```

## How to get started with Kedro-Dagster?

1. **Installation**

Install the plugin with `pip`:

```bash
pip install kedro-dagster
```

or add `kedro-dagster` to your project's `requirements.txt` or `pyproject.toml`.

2. **Initialize the plugin in your Kedro project**

Use the following command to generate a `definitions.py` file, where all translated Kedro objects are available as Dagster objects, and a `dagster.yml` configuration file:

```bash
kedro dagster init --env <ENV_NAME>
```

3. **Configure Jobs, Executors, and Schedules**

Define your job executors and schedules in the `dagster.yml` configuration file located in your Kedro project's `conf/<ENV_NAME>` directory. This file allows you to filter Kedro pipelines and assign specific executors and schedules to them.

```yaml
# conf/local/dagster.yml
schedules:
  daily: # Schedule name
    cron_schedule: "0 0 * * *" # Schedule parameters

executors: # Executor name
  sequential: # Executor parameters
    in_process:

  multiprocess:
    multiprocess:
      max_concurrent: 2

jobs:
  default: # Job name
    pipeline: # Pipeline filter parameters
      pipeline_name: __default__
    executor: sequential

  parallel_data_processing:
    pipeline:
      pipeline_name: data_processing
      node_names:
      - preprocess_companies_node
      - preprocess_shuttles_node
    schedule: daily
    executor: multiprocess

  data_science:
    pipeline:
      pipeline_name: data_science
    schedule: daily
    executor: sequential
```

4. **Launch the Dagster UI**

Start the Dagster UI to monitor and manage your pipelines using the following command:

```bash
kedro dagster dev --env <ENV_NAME>
```

The Dagster UI will be available at [http://127.0.0.1:3000](http://127.0.0.1:3000).

For a concrete use-case, see the [Kedro-Dagster example repository](https://github.com/gtauzin/kedro-dagster-example).

## How do I use Kedro-Dagster?

Full documentation is available at [https://gtauzin.github.io/kedro-dagster/](https://gtauzin.github.io/kedro-dagster/).

## Can I contribute?

We welcome contributions, feedback, and questions:

- **Report issues or request features:** [GitHub Issues](https://github.com/gtauzin/kedro-dagster/issues)
- **Join the discussion:** [Kedro Slack](https://slack.kedro.org/)
- **Contributing Guide:** [CONTRIBUTING.md](https://github.com/gtauzin/kedro-dagster/blob/main/CONTRIBUTING.md)

If you are interested in becoming a maintainer or taking a more active role, please reach out to Guillaume Tauzin on the [Kedro Slack](https://slack.kedro.org/).

## Where can I learn more?

There is a growing community around the Kedro project and we encourage you to become part of it. To ask and answer technical questions on the Kedro [Slack](https://slack.kedro.org/) and bookmark the [Linen archive of past discussions](https://linen-slack.kedro.org/). For questions related specifically to Kedro-Dagster, you can also open a [discussion](https://github.com/gtauzin/kedro-dagster/discussions).

## License

This project is licensed under the terms of the [Apache 2.0 License](https://github.com/gtauzin/kedro-dagster/blob/main/LICENSE.md).

## Acknowledgements

This plugin is inspired by existing Kedro plugins such as the [official Kedro plugins](https://github.com/kedro-org/kedro-plugins), [kedro-kubeflow](https://github.com/getindata/kedro-kubeflow), [kedro-mlflow](https://github.com/Galileo-Galilei/kedro-mlflow).
