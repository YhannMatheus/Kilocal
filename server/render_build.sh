#!/usr/bin/env bash
# Sair se houver erro
set -o errexit

# Instala as dependências
pip install -r requirements.txt

# Aplica as migrações no banco de dados do Neon
aerich upgrade