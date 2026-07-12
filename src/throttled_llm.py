"""
Versões throttled de get_llm / get_eval_llm para uso com tier free do Gemini.

Insere um InMemoryRateLimiter compartilhado entre aluno e juiz, configurado
com folga abaixo do limite real (10 RPM) para evitar 429.

NÃO alterar utils.py — usar este módulo via monkey-patch (evaluate_throttled.py).

Por quê o limiter é compartilhado:
- O limite "10 RPM por modelo" é cumulativo. Aluno e juiz usam o mesmo
  gemini-2.5-flash-lite, então as chamadas se somam.
- Um único limiter garante que o budget seja respeitado independente de
  qual função chamou o LLM.
"""

import os

from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_google_genai import ChatGoogleGenerativeAI


# 8 RPM = 0.1333 req/s. Margem de 20% sob o limite real (10 RPM) do flash-lite.
SHARED_LIMITER = InMemoryRateLimiter(
    requests_per_second=8 / 60,
    check_every_n_seconds=0.1,
    max_bucket_size=1,
)


def _build_throttled_llm(model_name: str, temperature: float) -> ChatGoogleGenerativeAI:
    """Constrói ChatGoogleGenerativeAI com rate_limiter compartilhado."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY não configurada no .env\n"
            "Obtenha uma chave em: https://aistudio.google.com/app/apikey"
        )
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=api_key,
        rate_limiter=SHARED_LIMITER,
    )


def get_llm(model=None, temperature: float = 0.0) -> ChatGoogleGenerativeAI:
    """Substituto de utils.get_llm com rate_limiter (assinatura compatível)."""
    model_name = model or os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")
    return _build_throttled_llm(model_name, temperature)


def get_eval_llm(temperature: float = 0.0) -> ChatGoogleGenerativeAI:
    """Substituto de utils.get_eval_llm com rate_limiter (assinatura compatível)."""
    eval_model = os.getenv("EVAL_MODEL", "gemini-2.5-flash-lite")
    return _build_throttled_llm(eval_model, temperature)
