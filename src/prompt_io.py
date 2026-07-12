"""
Carregamento e construção de ChatPromptTemplate a partir dos YAMLs do projeto.

Usado por:
- Validação local de prompts antes do push
- src/push_prompts.py (Etapa 5) para push ao LangSmith Hub

Formato esperado do YAML (achatado, conforme convenção do projeto):

    name: <handle/nome>
    description: <descrição curta>
    version: "<x.y>"
    techniques_applied: [<tecnica1>, <tecnica2>, ...]   # mínimo 2
    input_variables: [bug_report]
    system_prompt: |
      <texto do system prompt, sem placeholder de bug_report>
    few_shot_examples:                                   # opcional
      - human: |
          <bug exemplo>
        ai: |
          <user story exemplo>
    user_template: "{bug_report}"
"""

import sys
from typing import Any, Dict

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from utils import load_yaml, validate_prompt_structure

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def load_prompt_yaml(path: str) -> Dict[str, Any]:
    """Carrega o YAML do prompt e valida estrutura básica.

    Raises:
        ValueError: se o YAML estiver ausente, inválido, ou sem campos obrigatórios.
    """
    data = load_yaml(path)
    if data is None:
        raise ValueError(f"Não foi possível carregar o YAML: {path}")

    is_valid, errors = validate_prompt_structure(data)
    if not is_valid:
        raise ValueError(
            "Estrutura inválida no YAML do prompt:\n"
            + "\n".join(f"  - {e}" for e in errors)
        )

    return data


def build_chat_prompt_template(data: Dict[str, Any]) -> ChatPromptTemplate:
    """Monta um ChatPromptTemplate a partir do dict carregado do YAML.

    Estrutura das mensagens montadas:
        [system_prompt]
        [human few-shot 1] [ai few-shot 1]
        [human few-shot 2] [ai few-shot 2]
        ...
        [human user_template]   <- aqui mora o {bug_report}

    Few-shot examples são literais (HumanMessage / AIMessage), não templates,
    para que chaves no texto não sejam interpretadas como placeholders.
    """
    messages = [
        SystemMessagePromptTemplate.from_template(data["system_prompt"])
    ]

    for example in data.get("few_shot_examples", []):
        messages.append(HumanMessage(content=example["human"]))
        messages.append(AIMessage(content=example["ai"]))

    messages.append(
        HumanMessagePromptTemplate.from_template(data["user_template"])
    )

    return ChatPromptTemplate.from_messages(messages)
