# textgen

A fork of [oobabooga/text-generation-webui](https://github.com/oobabooga/text-generation-webui) — a Gradio web UI for running Large Language Models.

## Features

- Support for multiple model backends (llama.cpp, ExLlamaV2, Transformers, etc.)
- Chat and notebook interfaces
- Extensions system for custom functionality
- OpenAI-compatible API
- LoRA support for fine-tuned models
- GPTQ, AWQ, and GGUF quantization support

## Installation

### One-click installers

Download the latest release for your platform from the [Releases](../../releases) page.

| Platform | File |
|----------|------|
| Windows (CUDA) | `textgen-windows-cuda.zip` |
| Linux (CUDA) | `textgen-linux-cuda.tar.gz` |
| macOS | `textgen-macos.tar.gz` |

### Manual Installation

#### Prerequisites

- Python 3.11
- CUDA 12.1+ (for GPU acceleration)
- Git

#### Steps

```bash
# Clone the repository
git clone https://github.com/your-org/textgen
cd textgen

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python server.py
```

## Usage

```bash
# Basic usage
python server.py

# With a specific model
python server.py --model your-model-name

# Enable API
python server.py --api

# Listen on all interfaces
python server.py --listen

# Use a specific port
python server.py --port 7860
```

## Command-line flags

| Flag | Description |
|------|-------------|
| `--model MODEL` | Name of the model to load |
| `--lora LORA [LORA ...]` | LoRA adapter(s) to load |
| `--model-dir DIR` | Path to directory with models |
| `--listen` | Listen on all network interfaces |
| `--port PORT` | Port to use for the web UI (default: 7860) |
| `--api` | Enable the API extension |
| `--api-port PORT` | Port to use for the API (default: 5000) |
| `--cpu` | Use CPU for inference |
| `--gpu-memory VRAM` | VRAM to allocate per GPU in GiB |
| `--load-in-4bit` | Load model in 4-bit precision |
| `--load-in-8bit` | Load model in 8-bit precision |
| `--bf16` | Load model in bfloat16 precision |
| `--no-cache` | Do not use KV cache |
| `--verbose` | Print verbose output |

## Extensions

Extensions can be loaded with the `--extensions` flag:

```bash
python server.py --extensions openai multimodal
```

## Docker

```bash
docker compose up --build
```

## My Setup

I run this on a machine with a single RTX 3080 (10GB VRAM). The flags I typically use:

```bash
python server.py --model mistral-7b-instruct --load-in-4bit --gpu-memory 9 --api
```

> **Note:** I've found that `--gpu-memory 9` is the sweet spot for the 3080 — going higher risks OOM errors
> when the context gets long. If you have a 3080 Ti (12GB), you can probably push to `--gpu-memory 11`.

## Contributing

Pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting.

## License

AGPL-3.0. See [LICENSE](LICENSE) for details.
