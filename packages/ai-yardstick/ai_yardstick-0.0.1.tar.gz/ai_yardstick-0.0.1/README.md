# ai-yardstick

[![PyPI](https://img.shields.io/pypi/v/ai-yardstick.svg)](https://pypi.org/project/ai-yardstick/)
[![Changelog](https://img.shields.io/github/v/release/kevinschaul/ai-yardstick?include_prereleases&label=changelog)](https://github.com/kevinschaul/ai-yardstick/releases)
[![Tests](https://github.com/kevinschaul/ai-yardstick/actions/workflows/test.yml/badge.svg)](https://github.com/kevinschaul/ai-yardstick/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/kevinschaul/ai-yardstick/blob/master/LICENSE)

A CLI tool for running and managing LLM evaluations

See [my own evals](https://github.com/kevinschaul/llm-evals/)

## Installation

Install this tool using `pip`:
```bash
pip install ai-yardstick
```
## Usage

Create a new eval with:
```bash
ai-yardstick create EVAL_NAME
```

Then edit prompts.csv, models.csv and tests.csv with your test cases.

Run an eval with:
```bash
ai-yardstick run path/to/config.yaml
```

For help, run:
```bash
ai-yardstick --help
```
You can also use:
```bash
python -m llm_evals_cli --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd ai-yardstick
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
