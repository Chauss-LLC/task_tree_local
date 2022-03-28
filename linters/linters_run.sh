#!/bin/bash -e

YELLOW='\033[1;33m'
NC='\033[0m' # No color
MAX_LINE_LENGTH=100

echo -e "${YELLOW}Running black to autoformat code...${NC}"
python -m black -l $MAX_LINE_LENGTH $@
echo -e "${YELLOW}Running flake8 to check code...${NC}"
python -m flake8 --max-line-length $MAX_LINE_LENGTH $@
echo -e "${YELLOW}Running pydocstyle to check doc strings...${NC}"
python -m pydocstyle -e $@
echo -e "${YELLOW}Running pycodestyle to check code...${NC}"
python -m pycodestyle --show-source --max-line-length=$MAX_LINE_LENGTH $@
echo -e "${YELLOW}Running py3kwarn to find troubles with python3...${NC}"
python -m py3kwarn $@
echo -e "${YELLOW}Running pyflakes to check code...${NC}"
python -m pyflakes $@
echo -e "${YELLOW}Running pylama to check code...${NC}"
python -m pylama --async -m $MAX_LINE_LENGTH $@
echo -e "${YELLOW}Running pylint to check code...${NC}"
python -m pylint --enable-all-extensions --persistent=n $@
echo -e "${YELLOW}Running mypy to check types...${NC}"
python -m mypy  --strict --python-version 3.8 $@
