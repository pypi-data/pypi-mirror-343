<!--
  ~ Copyright (c) 2023-2024 Datalayer, Inc.
  ~
  ~ BSD 3-Clause License
-->

[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# 🪐 ✨ Jupyter AI Agents

[![Github Actions Status](https://github.com/datalayer/jupyter-ai-agents/workflows/Build/badge.svg)](https://github.com/datalayer/jupyter-ai-agents/actions/workflows/build.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/jupyter-ai-agents)](https://pypi.org/project/jupyter-ai-agents)

*The Jupyter AI Agents are equipped with tools like 'execute', 'insert_cell', and more, to transform your Jupyter Notebooks into an intelligent, interactive workspace!*

![Jupyter AI Agents](https://assets.datalayer.tech/jupyter-ai-agent/ai-agent-prompt-demo-terminal.gif)

```
Jupyter AI Agents <---> JupyterLab
       |
       | RTC (Real Time Collaboration)
       |
Jupyter Clients
```

Jupyter AI Agents empowers **AI** models to **interact** with and **modify Jupyter Notebooks**. The agent is equipped with tools such as adding code cells, inserting markdown cells, executing code, enabling it to modify the notebook comprehensively based on user instructions or by reacting to the Jupyter notebook events.

This agent is **innovative** as it is designed to **operate on the entire notebook**, not just at the cell level, enabling more comprehensive and seamless modifications. The agent can also run separetely from the Jupyter server as the communication is achieved through RTC () via the [Jupyter NbModel Client](https://github.com/datalayer/jupyter-nbmodel-client) and the [Jupyter Kernel Client](https://github.com/datalayer/jupyter-kernel-client).

The [LangChain Agent Framework](https://python.langchain.com/v0.1/docs/modules/agents/how_to/custom_agent) is used to manage the interactions between the AI model and the tools.

This library is documented on https://jupyter-ai-agents.datalayer.tech.

## Install

To install Jupyter AI Agents, run the following command.

```bash
pip install jupyter_ai_agents
```

Or clone this repository and install it from source.

```bash
git clone https://github.com/datalayer/jupyter-ai-agents
cd jupyter-ai-agents
pip install -e .
```

The Jupyter AI Agents can directly interact with JupyterLab. The modifications made by the Jupyter AI Agents can be seen in real-time thanks to [Jupyter Real Time Collaboration](https://jupyterlab.readthedocs.io/en/stable/user/rtc.html). Make sure you have JupyterLab installed with the Collaboration extension.

```bash
pip install jupyterlab==4.4.1 jupyter-collaboration==4.0.2 ipykernel
```

We ask you to take additional actions to overcome limitations and bugs of the pycrdt library. Ensure you create a new shell after running the following commands.

```bash
pip uninstall -y pycrdt datalayer_pycrdt
pip install datalayer_pycrdt==0.12.15
```

## Use from the CLI

We put here a quick example for a Out-Kernel Stateless Agent via CLI helping your JupyterLab session.

Start JupyterLab, setting a `port` and a `token` to be reused by the agent, and create a notebook `test.ipynb`.

```bash
jupyter lab --port 8888 --IdentityProvider.token MY_TOKEN
```

You can also start JupyterLab with the following command.

```bash
make jupyterlab
```

Jupyter AI Agents supports multiple AI model providers (more information can be found on [this documentation page](https://jupyter-ai-agents.datalayer.tech/docs/models)).

The following takes you through an example with the Azure OpenAI provider. Read the [Azure Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai) to get the needed credentials and make sure you define them in the following `.env` file.

```bash
cat << EOF >>.env
OPENAI_API_VERSION="..."
AZURE_OPENAI_ENDPOINT="..."
AZURE_OPENAI_API_KEY="..."
EOF
```

**Prompt Agent**

To use the Jupyter AI Agents, an easy way is to launch a CLI (update the Azure deployment name based on your setup).

```bash
# Prompt agent example.
jupyter-ai-agents prompt \
  --url http://localhost:8888 \
  --token MY_TOKEN \
  --model-provider azure-openai \
  --model-name gpt-4o-mini \
  --path test.ipynb \
  --input "Create a matplotlib example"
```

You can also start prompt with the following command.

```bash
make prompt
```

![Jupyter AI Agents](https://assets.datalayer.tech/jupyter-ai-agent/ai-agent-prompt-demo-terminal.gif)

**Explain Error Agent**

```bash
# Explain Error agent example.
jupyter-ai-agents explain-error \
  --url http://localhost:8888 \
  --token MY_TOKEN \
  --model-provider azure-openai \
  --model-name gpt-4o-mini \
  --path test.ipynb
```

You can also start request the error explanation with the following command.

```bash
make explain-error
```

![Jupyter AI Agents](https://assets.datalayer.tech/jupyter-ai-agent/ai-agent-explainerror-demo-terminal.gif)

## Uninstall

To uninstall the agent, execute.

```bash
pip uninstall jupyter_ai_agents
```

## Deploy in a Server

You can start a Jupyter AI Agents server to be used in combination with the [Datalayer online services](https://datalayer.app).

```bash
make server
```

## Contributing

### Development install

```bash
# Clone the repo to your local environment
# Change directory to the jupyter_ai_agents directory
# Install package in development mode - will automatically enable
# The server extension.
pip install -e ".[test,lint,typing]"
```

### Running Tests

Install dependencies:

```bash
pip install -e ".[test]"
```

To run the python tests, use:

```bash
pytest
```

### Development uninstall

```bash
pip uninstall jupyter_ai_agents
```

### Packaging the library

See [RELEASE](RELEASE.md).
