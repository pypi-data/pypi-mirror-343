---

# tinyAgent 🤖

![tinyAgent Logo](static/images/tinyAgent_logo_v2.png)

```
   __  .__                _____                         __
_/  |_|__| ____ ___.__. /  _  \    ____   ____   _____/  |_
\   __\  |/    <   |  |/  /_\  \  / ___\_/ __ \ /    \   __\
 |  | |  |   |  \___  /    |    \/ /_/  >  ___/|   |  \  |
 |__| |__|___|  / ____\____|__  /\___  / \___  >___|  /__|
              \/\/            \/\/_____/      \/     \/
```

# Why tinyAgent?

Turn any Python function into an AI‑powered agent in three lines:

```python
from tinyagent.decorators import tool
from tinyagent.agent import tiny_agent

@tool                  # 1️⃣  function → tool
def add(a: int, b: int) -> int:
    return a + b

agent = tiny_agent(tools=[add])             # 2️⃣  tool → agent
print(agent.run("add 40 and 2"))           # 3️⃣  natural‑language call
# → 42
```

- **Zero boilerplate** – just a decorator.
- **Built‑in LLM orchestration** – validation, JSON I/O, retry, fallback.
- **Scales as you grow** – add more tools or plug into tiny_chain without rewrites.

# Why tiny_chain?

Handle multi‑step questions with automatic tool planning in <10 lines.

```python
from tinyagent.factory.tiny_chain import tiny_chain
from tinyagent.tools.duckduckgo_search import get_tool as search
from tinyagent.tools.custom_text_browser import get_tool as browser
from tinyagent.decorators import tool

@tool
def summarize(text: str) -> str:            # simple LLM summariser
    return "TL;DR → " + text[:200]

chain = tiny_chain.get_instance(tools=[search(), browser(), summarize._tool])
print(chain.run("Find current US import tariffs and summarise"))
# → bullet‑point answer pulled from official sources
```

- **One entry point** – submit a natural‑language task, get JSON results.
- **LLM triage agent** – chooses the best tool chain (search → browser → summarise).
- **Robust fallback** – if planning fails, it just tries every tool once.

**Made by (x) [@tunahorse21](https://x.com/tunahorse21) | A product of [alchemiststudios.ai](https://alchemiststudios.ai)**

---

## Heads Up

tinyAgent is in **BETA** until V1. It's working but still evolving! I can't guarantee it's 100% bug-free, but I'm actively improving it whenever I can between my day job and business.  
Found something that could be better? Show off your skills and open an issue with a fix: I'd genuinely appreciate it!

---

## Overview

tinyAgent is a streamlined framework for building powerful, LLM-powered agents that solve complex tasks through tool execution, orchestration, and dynamic capability creation. Convert any Python function into a useful tool and then into an agent with minimal configuration, unlocking a world of scalable, modular possibilities.

---

## Installation

### Via pip (Recommended)

```bash
pip install tiny_agent_os
```

---

## Post-Installation Configuration for Pip Users

After installing via `pip`, you'll need to provide your own configuration files. For convenience, you can download the defaults directly:

---

### Download the Configuration File (`config.yml`)

**Using `wget`:**

```bash
wget https://raw.githubusercontent.com/alchemiststudiosDOTai/tinyAgent/v0.65/config.yml
```

---

### Download the Environment File (`.env`)

Download the example environment file and rename it to `.env`:

**Using `wget`:**

```bash
wget https://raw.githubusercontent.com/alchemiststudiosDOTai/tinyAgent/v0.65/.envexample -O .env
```

> **Note:** Be sure to edit the `.env` file with your actual API keys and any other required variables.

---

### Cloning for Development

```bash
git clone https://github.com/alchemiststudiosDOTai/tinyAgent.git
cd tinyAgent
```

---

## Post-Installation Configuration

After installing (either via pip or from source), remember to configure your environment and `.env` files with relevant API keys from https://openrouter.ai

Both the config.yml and env work out of the box with a openrouter API, you can use any openai API, and the config has an example of a local LLM.
The /documentation folder has more details and is being updated.

---

## Tools and the `@tool` Decorator

In tinyAgent, **any Python function** can be transformed into a usable "tool" by simply decorating it with `@tool`. This makes it discoverable by your agents, allowing them to execute that function in response to natural-language queries.

### Example

```python
from tinyagent.decorators import tool

@tool
def greet_person(name: str) -> str:
    """Return a friendly greeting."""
    return f"Hello, {name}!"
```

That's it! Once decorated, `greet_person` can be included in an agent's list of tools, letting your LLM-driven agent call it as needed.

### Example – `calculate_sum` Tool

Turn a plain Python function into a natural-language skill with `@tool` and `tiny_agent`.

```python
from tinyagent.decorators import tool
from tinyagent.agent import tiny_agent

@tool
def calculate_sum(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b

if __name__ == "__main__":
    agent = tiny_agent(tools=[calculate_sum])
    query = "calculate the sum of 5 and 3"
    result = agent.run(query, expected_type=int)
    print(f"Query: '{query}' -> Result: {result}")
```

Console output:

```
Validating args for tool: calculate_sum
Arguments provided: {'a': 5, 'b': 3}
Query: 'calculate the sum of 5 and 3' -> Result: 8
```

---

## Philosophy

tinyAgent is built on two core ideas:

### 1. Functions as Agents

Any Python function can be turned into a tool—and then seamlessly integrated into an agent. This approach makes extending and innovating simple.

```mermaid
flowchart LR
    A["Python Function"] --> B["Tool"]
    B --> C["Agent"]
    C --> D["Result"]
```

![Function to Agent Flow](static/images/func_agent.png)

```python
#!/usr/bin/env python3
"""
Example: Functions as Agents
"""
from tinyagent.decorators import tool
from tinyagent.agent import tiny_agent

@tool
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two integers."""
    return a + b


def main():
    # Create an agent with the calculate_sum tool
    agent = tiny_agent(tools=[calculate_sum])
    query = "calculate the sum of 5 and 3"
    result = agent.run(query, expected_type=int)
    print(f"Query: '{query}' -> Result: {result}")


if __name__ == "__main__":
    main()
```

### 2. tiny_chain Orchesration

- IN BETA

tiny_chain is the main engine of tinyAgent's orchestration. It lets your agent solve complex tasks by chaining together multiple tools, using an LLM-powered "triage agent" to plan the best sequence. If the plan fails, tiny_chain falls back to running all tools in sequence, ensuring robustness and reliability.

```mermaid
flowchart LR
    A["User Query"] --> B["Triage Agent"]
    B --> C["Tool Planning"]
    C --> D["Tool Execution"]
    D --> E["Search"] --> F["Browser"] --> G["Summarize"]
    G --> H["Final Result"]

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#bbf,stroke:#333,stroke-width:2px
    style F fill:#bbf,stroke:#333,stroke-width:2px
    style G fill:#bbf,stroke:#333,stroke-width:2px
```

- **Simple:** You describe your task in natural language. tiny_chain figures out which tools to use and in what order.
- **Smart:** The triage agent (an LLM) analyzes your query and suggests a plan—sometimes a single tool, sometimes a multi-step chain.
- **Robust:** If the triage agent can't make a good plan, tiny_chain just tries all tools, so you always get an answer.
- **Extensible:** Add new tools or improve the triage agent to handle more complex workflows.

**How it works (technical overview):**

- When you submit a task, tiny_chain asks the triage agent for a plan (JSON: single tool or sequence).
- If the plan is valid, tiny_chain executes the tools in order, passing results between them.
- If the plan is invalid or fails, tiny_chain runs all tools as a fallback.
- All errors are caught and logged, so you always get feedback.

### tiny_chain Example – "Tariff Research Tool"

Use this snippet (or drop-in file) anywhere in your docs to show **exactly how tiny_chain works** end-to-end.

```python
#!/usr/bin/env python3
"""
tiny_chain example: automatically find and summarise U.S. import-tariff data
"""
from tinyagent.factory.tiny_chain import tiny_chain
from tinyagent.tools.duckduckgo_search import get_tool as search_tool
from tinyagent.tools.custom_text_browser import get_tool as browser_tool
from tinyagent.decorators import tool
from tinyagent.agent import get_llm

@tool(name="summarize", description="Summarize input text with the LLM")
def summarize(text: str) -> str:
    prompt = f"Summarize the following text:\n\n{text}\n\nSummary:"
    return get_llm()(prompt).strip()

# 1 – build the chain
chain = tiny_chain.get_instance(
    tools=[search_tool(), browser_tool(), summarize._tool]
)

# 2 – submit any natural-language task
task_id = chain.submit_task(
    "Find current US import tariffs and visit official trade websites for details"
)

# 3 – get structured results
print(chain.get_task_status(task_id).result)
```

**What it demonstrates**

| tiny_chain feature                        | Visible in run                                     |
| ----------------------------------------- | -------------------------------------------------- |
| 🔗 Automatic tool planning (triage agent) | Picks _search → browser → summarize_               |
| 🛠 Pluggable tools                         | Search + browser + summarize tools in sequence     |
| 📝 Structured trace                       | `steps`, `tools_used`, errors if any               |
| 🤖 LLM-powered step                       | `summarize` converts page content → concise answer |

Copy-paste, run, and you have a minimal yet complete example of tiny_chain orchestrating multiple tools to solve a real research task.

### Key links

- **Harmonized Tariff Schedule (USITC)**  
  <https://hts.usitc.gov/>

- **FTA Tariff Tool (International Trade Administration)**  
  <https://www.trade.gov/fta-tariff-tool-home>

- **CBP – Determining Duty Rates**  
  <https://www.cbp.gov/trade/programs-administration/determining-duty-rates>

### Console Output

```text
============================================================
Tariff Research Tool
============================================================

Researching: 'Find current US import tariffs and use the browser to visit official trade websites to get details'
------------------------------------------------------------

Tool Chain Steps:

=== Step 1 ===
Tool: search
Top hit → Harmonized Tariff Schedule (hts.usitc.gov)

=== Step 2 ===
Tool: browser
Visited title → Harmonized Tariff Schedule

=== Step 3 ===
Tool: summarize
Result →
To find current US import tariffs, consult the **Harmonized Tariff Schedule (HTS)**
on the USITC website.
For Free‑Trade Agreement rates, use the **FTA Tariff Tool** on trade.gov.
CBP also provides duty‑rate guidance.

------------------------------------------------------------
Tools used: search → browser → summarize
```

**What it demonstrates**

| tiny_chain feature                        | Visible in run                                     |
| ----------------------------------------- | -------------------------------------------------- |
| 🔗 Automatic tool planning (triage agent) | Picks _search → browser → summarize_               |
| 🛠 Pluggable tools                         | Search + browser + summarize tools in sequence     |
| 📝 Structured trace                       | `steps`, `tools_used`, errors if any               |
| 🤖 LLM-powered step                       | `summarize` converts page content → concise answer |

Copy-paste, run, and you have a minimal yet complete example of tiny_chain orchestrating multiple tools to solve a real research task.

---

## (NEW) Retrieval-Augmented Memory (RAG)

> **Note:**
>
> - By default, all embeddings are generated locally using HuggingFace models (no external API calls).
> - To enable RAG, install with:
>   ```bash
>   pip install tiny_agent_os[rag]
>   ```
> - If you do not use RAG, these dependencies are not required.
> - **API-based embedding support (e.g., OpenAI, Cohere) is coming soon!**

tinyAgent now supports plug-and-play vector memory for contextual recall using ChromaDB. You can add memory to any agent in just a few lines:

```python
from tinyagent.decorators import tool
from tinyagent.agent import tiny_agent
from tinyagent.utils.vector_memory import VectorMemory

@tool
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two integers."""
    return a + b

mem = VectorMemory(persistence_directory="~/.tinyagent_mem")
agent = tiny_agent(tools=[calculate_sum], memory=mem)

# Store a fact in memory
question = "remember that my lucky numbers are 7 and 11"
agent.run(question)

# Retrieve the fact later
follow = "what were my lucky numbers?"
print(agent.run(follow))  # → "7 and 11"
```

This enables your agent to remember and retrieve facts, context, or instructions across turns—no extra boilerplate required.

## Features

- **Modular Design:** Easily convert any function into a tool.
- **Flexible Agent Options:** Use the simple orchestrator or advanced `AgentFactory`.
- **Robust Error Handling:** Improved debugging with custom exceptions.
- **Structured Output:** Enforce JSON formats for consistent outputs.

---

## Acknowledgments & Inspirations

- **my wife**
- [HuggingFace SmoLAgents](https://github.com/huggingface/smolagents)
- [Aider-AI](https://github.com/Aider-AI/aider)
- And many other open-source contributors!

---

## Contact

For questions, suggestions, or business inquiries:

- **Email**: [info@alchemiststudios.ai](mailto:info@alchemiststudios.ai)
- **X**: [@tunahorse21](https://x.com/tunahorse21)
- **Website**: [alchemiststudios.ai](https://alchemiststudios.ai)

---

## License

**Business Source License 1.1 (BSL)**
This project is licensed under the Business Source License 1.1. It is **free for individuals and small businesses** (with annual revenues under $1M).
For commercial use by larger businesses, an enterprise license is required.
For licensing or usage inquiries, please contact: [info@alchemiststudios.ai](mailto:info@alchemiststudios.ai)
