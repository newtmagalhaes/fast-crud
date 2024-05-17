#!/bin/sh
set -e

# por ser apenas uma demo, garante que migrações estão aplicadas
alembic upgrade head

# executa em modo de produção
fastapi run app/ --port 8000
