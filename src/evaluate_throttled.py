"""
Wrapper para src/evaluate.py que injeta rate limiter no LLM antes da execução.

Uso: PYTHONIOENCODING=utf-8 python src/evaluate_throttled.py

Estratégia (sem alterar evaluate.py nem utils.py):

1. Importa utils primeiro (carrega o módulo).
2. Importa throttled_llm (define versões com rate_limiter).
3. Substitui utils.get_llm e utils.get_eval_llm pelas versões throttled.
4. SÓ DEPOIS importa evaluate (que internamente faz `from utils import get_llm`).
   Como utils.get_llm já está patchado, evaluate.py recebe a versão throttled.
5. Mesma lógica vale para metrics.py (que importa get_eval_llm).
6. Chama evaluate.main().

Crítico: imports de evaluate e metrics ANTES do patch usariam a versão original.
Por isso o patch acontece logo após carregar utils, antes de qualquer outro import.
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Garante que src/ está no sys.path para imports diretos (evaluate, utils, etc.)
sys.path.insert(0, str(Path(__file__).parent.resolve()))

import utils
import throttled_llm

# Monkey-patch: substitui as funções no módulo utils.
# Qualquer `from utils import get_llm/get_eval_llm` feito DEPOIS deste ponto
# vai pegar as versões throttled.
utils.get_llm = throttled_llm.get_llm
utils.get_eval_llm = throttled_llm.get_eval_llm

print("⚙️  Rate limiter ativo: 8 RPM compartilhado (margem vs 10 RPM real)")
print("⏱️  Avaliação completa estimada em ~7-8 minutos\n")

import evaluate  # noqa: E402  — import depois do patch é intencional

if __name__ == "__main__":
    sys.exit(evaluate.main())
