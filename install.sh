#/bin/bash
rye sync
git config --global --add safe.directory /fastapi-sample
pre-commit install
