#/bin/bash
uv sync
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
source ~/.bashrc
git config --global --add safe.directory /fastapi-sample
pre-commit install
