# tests/conftest.py
import sys, os

# Caminho absoluto para a pasta raiz do projeto (onde fica 'src/')
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
