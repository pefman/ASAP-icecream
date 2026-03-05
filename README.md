# SkynetToBe

A tiny self-evolving Python script. It reads a target script, asks an AI to improve it, tests the result, and overwrites the original if it passes — then repeats.

## Usage

```bash
python notskynet.py <endpoint> [prompt] [repo] [token]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `endpoint` | yes | OpenAI-compatible API, e.g. `your-endpoint.com/v1/chat/completions` |
| `prompt` | no | Evolution direction, e.g. `"Add error handling"` (default: `"Improve and evolve this code"`) |
| `repo` | no | GitHub repo to push evolved code to, e.g. `github.com/user/repo.git` |
| `token` | no | GitHub personal access token (only needed with `repo`) |

**Example — custom prompt + auto-push:**
```bash
python notskynet.py your-endpoint.com/v1/chat/completions "Make it faster" github.com/user/repo.git ghp_yourtoken
```

Point it at any OpenAI-compatible endpoint. It will run `ITER` evolution cycles on `main.py`.

## How it works

1. Reads the full source of `main.py`
2. Sends it to the AI with the prompt *"Improve and evolve this code"*
3. Writes the response to a temp file and runs it
4. If exit code is `0` → overwrites `main.py` with the improved version
5. Cleans up the temp file and repeats

## Config

| Variable | Default | Description |
|----------|---------|-------------|
| `SCRIPT` | `main.py` | File to evolve |
| `ITER`   | `5`      | Number of evolution cycles |
| `MODEL`  | `Qwen3.5-35B-A3B-UD-Q4_K_XL` | Model to use |

## Requirements

Python 3 standard library only — no dependencies.
