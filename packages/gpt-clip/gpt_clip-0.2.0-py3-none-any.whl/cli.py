#!/usr/bin/env python3
"""
cli.py: Send clipboard content to OpenAI Chat API and copy response back to clipboard.

Copyright (c) 2024 Le Chen (chenle02@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Author: Le Chen (chenle02@gmail.com)

This script provides a command-line interface to interact with OpenAI's Chat API using
clipboard content. It reads text from the clipboard, sends it to OpenAI's API, and
copies the response back to the clipboard.

Requirements:
    - pyperclip: For clipboard operations
    - openai: For interacting with OpenAI's API
    - Valid OpenAI API key set in OPENAI_API_KEY environment variable
    - Configuration file in ~/.config/gpt-clip/config.json

Configuration file format:
    {
        "system_prompt": "Optional system prompt for ChatGPT",
        "model": "gpt-3.5-turbo"  // or any other available OpenAI model
    }
"""
import os
import sys
import json

try:
    import pyperclip
except ImportError:
    print("Missing dependency: pyperclip. Install with 'pip install pyperclip'", file=sys.stderr)
    sys.exit(1)

try:
    import openai
except ImportError:
    print("Missing dependency: openai. Install with 'pip install openai'", file=sys.stderr)
    sys.exit(1)

# XDG Base Directory for configuration
CONFIG_DIR = os.environ.get(
    'XDG_CONFIG_HOME',
    os.path.expanduser('~/.config')
)
CONFIG_PATH = os.path.join(CONFIG_DIR, 'gpt-clip', 'config.json')


def load_config(path=CONFIG_PATH):
    """
    Load configuration from JSON file.

    Args:
        path (str): Path to the configuration file. Defaults to CONFIG_PATH.

    Returns:
        dict: Configuration dictionary containing 'system_prompt' and 'model'.

    Raises:
        SystemExit: If configuration file is not found or contains invalid JSON.
    """
    if not os.path.isfile(path):
        print(f"Configuration file not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing config file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """
    Main function that orchestrates the clipboard-to-ChatGPT workflow.

    The function performs the following steps:
    1. Loads configuration from the config file
    2. Initializes OpenAI client (supports both new and legacy API)
    3. Reads text from clipboard
    4. Sends the text to OpenAI's Chat API
    5. Copies the response back to clipboard

    Raises:
        SystemExit: On various error conditions (empty clipboard, API errors, etc.)
    """
    # Load config
    config = load_config()

    # Set API key and initialize OpenAI client (new or legacy)
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    # New OpenAI client (v0.27+) uses OpenAI() class
    # Fallback to legacy top-level API if unavailable
    if hasattr(openai, 'OpenAI'):
        client = openai.OpenAI(api_key=api_key)
        use_legacy = False
    else:
        openai.api_key = api_key
        client = openai
        use_legacy = True

    # Read from clipboard
    clipboard_text = pyperclip.paste()
    if not clipboard_text.strip():
        print("Clipboard is empty or whitespace.", file=sys.stderr)
        sys.exit(1)

    # Prepare messages
    system_prompt = config.get('system_prompt', '')
    model = config.get('model', 'gpt-3.5-turbo')
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': clipboard_text})

    # Call OpenAI API
    try:
        if use_legacy:
            # Legacy ChatCompletion API
            response = client.ChatCompletion.create(
                model=model,
                messages=messages
            )
        else:
            # New client interface
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
    except Exception as e:
        print(f"OpenAI API request failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract and copy response
    try:
        # Both legacy and new client use same response structure
        reply = response.choices[0].message.content
    except (AttributeError, IndexError) as e:
        print(f"Unexpected API response format: {e}", file=sys.stderr)
        sys.exit(1)

    pyperclip.copy(reply)
    print(reply)
    print("Response copied to clipboard.")


if __name__ == '__main__':
    main()
