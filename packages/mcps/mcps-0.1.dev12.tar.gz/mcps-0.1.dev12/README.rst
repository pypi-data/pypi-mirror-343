.. image:: https://img.shields.io/pypi/v/mcps.svg
    :alt: PyPI-Server
    :target: https://pypi.org/project/mcps/

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

====
MCPS
====


    Multi-Component Platform System (MCPS) - A framework for managing distributed services and agents


MCPS is a comprehensive framework for managing distributed services and intelligent agents. It provides tools for service discovery, lifecycle management, and runtime execution in various environments.

Features
========

- **Agent Discovery**: Find and query agents using natural language or capability matching
- **Lifecycle Management**: Deploy, start, stop, and monitor agents
- **Runtime Environments**: Support for Python, Docker, and other runtime environments
- **Service Integration**: Connect agents with tools and services
- **Caching Strategy**: Efficient caching of messages, logs, and agent state
- **CLI Interface**: Command-line tools for managing agents and services

Installation
============

.. code-block:: bash

    pip install mcps

Quick Start
===========

.. code-block:: python

    from mcps import MCPS_Client
    from mcps import Agents_Client

    # Query for tools
    mcps_tools_client = MCPS_Client(api_key="YOUR_KEY")
    tools = mcps_tools_client.query("北京的天气怎么样？", topk=1)[0]

    # Query for agents
    mcps_agent_client = Agents_Client(api_key="YOUR_KEY")
    agent = mcps_agent_client.call_from_query("北京的天气怎么样？", topl=1)[0]

    # Run agent with tools
    result = agent.run(query="北京的天气怎么样？", tools=tools)

CLI Usage
=========

.. code-block:: bash

    # List available agents
    mcps agent list

    # Query for agents
    mcps agent query "weather forecast"

    # Deploy and run an agent
    mcps agent deploy weather_agent_1
    mcps agent start weather_agent_1
    mcps agent run weather_agent_1 "What's the weather in Beijing?"
    mcps agent stop weather_agent_1
    mcps agent cleanup weather_agent_1

License
=======

MIT License
