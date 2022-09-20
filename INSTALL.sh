#!/bin/bash

# Get the directory of this script
# https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd "$DIR"
cd ../
ln -s evans_django_tools/bypass-lint.sh .
ln -s evans_django_tools/lint.sh .
mkdir -p .github/workflows
ln -s ../../evans_django_tools/workflows/codeql-analysis.yml .github/workflows/codeql-analysis.yml
ln -s ../../evans_django_tools/workflows/main.yml .github/workflows/main.yml
ln -s ../../evans_django_tools/workflows/pyright_to_rdjson.py .github/workflows/pyright_to_rdjson.py
