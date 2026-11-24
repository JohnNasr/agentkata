# agentkata

**Learn to build an AI agent from scratch, one failing test at a time.**

Frameworks hide how agents work. agentkata makes you build one yourself: messages, tool calling, the
agent loop, retries, memory trimming, guardrails, structured output. That's the machinery behind
every coding agent and chatbot. You write each piece in plain Python until its tests pass.

- **No API key, no account, no cost.** Tests use a scripted fake model. At the end you plug in a real
  local model through [Ollama](https://ollama.com), which is free and runs offline.
- **No framework.** Just Python 3.10+ and pytest. When you're done, you'll understand what LangChain,
  the Claude Agent SDK and friends do for you.
- **Each exercise teaches one idea.** The lesson is in the file's docstring, right above the code you write.

## Start

```powershell
git clone https://github.com/JohnNasr/agentkata
cd agentkata
pip install pytest
python -m agentkata
```

The runner checks every exercise in order and stops at the first one that isn't done:

```
  done ex01_messages
  done ex02_ask
  todo ex03_tool_schema

Open exercises/ex03_tool_schema.py, read the docstring, and make this pass:

tests\test_ex03_tool_schema.py:26: in test_simple_function
    assert ex.function_to_tool(add) == {
E   NotImplementedError: Exercise 03: write function_to_tool()

2/10 done. Run `python -m agentkata` again after editing.
```

Run just one exercise with `python -m agentkata 03`.

## The exercises

| # | You build | The idea |
|---|---|---|
| 01 | `build_messages` | Models have no memory; you send the whole conversation every time. |
| 02 | `ask` | Calling a model through one small interface, so fake and real models swap freely. |
| 03 | `function_to_tool` | Describing Python functions as JSON Schema tools a model can request. |
| 04 | `parse_tool_call` | Pulling a tool call out of chatty text, for small models without native tool calling. |
| 05 | `run_tool` | Running what the model asked for without ever crashing; errors go back to the model. |
| 06 | `run_agent` | **The agent loop**: model → tools → results → model, with a step limit. |
| 07 | `with_retry` | Exponential backoff for flaky networks, without retrying your own bugs. |
| 08 | `trim_history` | Fitting a long chat into a token budget without orphaning tool results. |
| 09 | `guard_tools` | "Allow / Don't allow" prompts before dangerous tools run. |
| 10 | `ask_json` | Getting reliable JSON by showing the model its own mistake and asking again. |

Later exercises reuse your earlier code. Exercise 06 calls your 03 and 05, so a bug early shows up later.

## Then: talk to your agent

```powershell
ollama pull qwen3:4b
python examples/chat.py
```

That's your code from exercises 06, 07 and 09 running a real model. It has a calculator, a clock, and a
note-saving tool that asks your permission first. Use `--model <name>` for any Ollama model with tool support.

## Stuck?

Reference solutions are in `solutions/`. Try for a while first; that's where the learning happens. To check
the whole course works on your machine: `KATA_SOLUTIONS=1 pytest` (PowerShell: `$env:KATA_SOLUTIONS=1; pytest`).

## Contributing

Lessons live in `solutions/`. Edit a solution's docstring or code, then regenerate the blank exercises:

```powershell
python tools/make_exercises.py
```

CI runs every test against the solutions and fails if `exercises/` is out of date.

MIT licensed.
