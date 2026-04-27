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
    parser.add_argument('--port', type=int, default=7860,
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
                        help='API authentication key (empty = no auth)')
    parser.add_argument('--public-api', action='store_true',
                        help='Create a public API endpoint via Cloudflare tunnel')

    # UI settings
    parser.add_argument('--chat', action='store_true',
                        help='Launch in chat mode by default')
    parser.add_argument('--notebook', action='store_true',
                        help='Launch in notebook mode by default')
    parser.add_argument('--no-stream', action='store_true',
                        help='Disable token streaming in the UI')
    parser.add_argument('--theme', type=str, default='default',
                        help='Gradio theme to use for the UI')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose/debug logging')

    return parser.parse_args()


def setup_environment(args):
    """Configure environment variables and paths based on parsed arguments."""
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug('Verbose logging enabled')

    # Resolve model directory
    model_dir = ROOT_DIR / args.model_dir
    if not model_dir.exists():
        logger.info(f'Creating model directory: {model_dir}')
        model_dir.mkdir(parents=True, exist_ok=True)

    # Set listen address
    if args.listen:
        args.host = '0.0.0.0'
        logger.info('Listening on all network interfaces')

    return args


def main():
    """Main entry point — parse args, set up environment, and launch the UI."""
    args = parse_arguments()
    args = setup_environment(args)

    logger.info('Starting textgen server...')
    logger.info(f'Server address: http://{args.host}:{args.port}')

    if args.model:
        logger.info(f'Model to load: {args.model}')
    else:
        logger.info('No model specified — select one from the UI')

    # Lazy import to speed up startup and allow env setup first
    try:
        from modules.ui import create_interface
        interface = create_interface(args)
        interface.queue()
        interface.launch(
            server_name=args.host,
            server_port=args.port,
            share=args.share,
            inbrowser=False,
        )
    except ImportError as e:
        logger.error(f'Failed to import UI modules: {e}')
        logger.error('Please ensure all dependencies are installed: pip install -r requirements.txt')
        sys.exit(1)
    except Exception as e:
        logger.exception(f'Unexpected error during startup: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
