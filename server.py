#!/usr/bin/env python3
"""
Main entry point for the textgen web UI server.
Fork of oobabooga/text-generation-webui.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ensure the project root is in the Python path
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(ROOT_DIR))


def parse_arguments():
    """Parse command-line arguments for the server."""
    parser = argparse.ArgumentParser(
        description='textgen - Text Generation Web UI',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Server settings
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Host address to bind the server to')
    # Changed default port from 7860 to 7861 to avoid conflicts with other Gradio apps I run locally
    parser.add_argument('--port', type=int, default=7861,
                        help='Port number to run the server on')
    parser.add_argument('--share', action='store_true',
                        help='Create a public Gradio share link')
    parser.add_argument('--listen', action='store_true',
                        help='Listen on all network interfaces (0.0.0.0)')

    # Model settings
    parser.add_argument('--model', type=str, default=None,
                        help='Name of the model to load at startup')
    parser.add_argument('--model-dir', type=str, default='models',
                        help='Directory containing model files')
    parser.add_argument('--lora', nargs='+', default=None,
                        help='List of LoRA adapters to apply')

    # Inference backend
    parser.add_argument('--loader', type=str, default=None,
                        choices=['transformers', 'llama.cpp', 'exllama', 'exllamav2',
                                 'ctransformers', 'gptq', 'awq'],
                        help='Model loader/backend to use')

    # Hardware settings
    parser.add_argument('--cpu', action='store_true',
                        help='Force CPU inference (no GPU)')
    parser.add_argument('--gpu-memory', nargs='+', type=str, default=None,
                        help='GPU memory limits per device (e.g. 8GiB)')
    parser.add_argument('--cpu-memory', type=str, default=None,
                        help='CPU memory limit for model offloading')
    parser.add_argument('--load-in-8bit', action='store_true',
                        help='Load model in 8-bit quantization')
    parser.add_argument('--load-in-4bit', action='store_true',
                        help='Load model in 4-bit quantization')

    # API settings
    parser.add_argument('--api', action='store_true',
                        help='Enable the API server')
    parser.add_argument('--api-port', type=int, default=5000,
                        help='Port for the API server')
    parser.add_argument('--api-key', type=str, default='',
                        help='API authenticati