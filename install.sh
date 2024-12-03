#/bin/bash
uv sync
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
source ~/.bashrc
uv tool install ruff==0.8.1
uv tool install mypy==1.13.0
git config --global --add safe.directory /fastapi-sample
pre-commit install
