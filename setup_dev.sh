#!/usr/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
PURPLE='\033[0;35m'
NC='\033[0m'
echo -e "${PURPLE}TRYING TO INSTALL${NC} pre-commit hooks to .git"
pre-commit install --install-hooks
echo -e "${GREEN}hooks installed successfully!${NC}"
pre-commit run --all-files
echo -e "${GREEN}manual pre-commit run succeed${NC}"
