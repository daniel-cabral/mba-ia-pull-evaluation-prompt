"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import sys
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

HUB_NAME = "leonanluppi/bug_to_user_story_v1"
OUTPUT_PATH = "prompts/bug_to_user_story_v1.yml"

_ROLE_BY_CLASS = {
    "SystemMessagePromptTemplate": "system",
    "HumanMessagePromptTemplate": "human",
    "AIMessagePromptTemplate": "ai",
    "ChatMessagePromptTemplate": "chat",
    "SystemMessage": "system",
    "HumanMessage": "human",
    "AIMessage": "ai",
}


def _message_to_dict(msg):
    """Converte uma mensagem do ChatPromptTemplate em {role, content}.

    Suporta tanto *PromptTemplate (com placeholders {var}) quanto
    *Message literais (sem placeholders).
    """
    cls_name = type(msg).__name__
    role = _ROLE_BY_CLASS.get(cls_name, cls_name.lower())

    if hasattr(msg, "prompt") and hasattr(msg.prompt, "template"):
        content = msg.prompt.template
    else:
        content = getattr(msg, "content", str(msg))

    return {"role": role, "content": content}


def pull_prompts_from_langsmith() -> int:
    """Faz pull do prompt v1 do Hub e salva em YAML local."""
    try:
        prompt = hub.pull(HUB_NAME)
    except Exception as e:
        print(f"❌ Falha no pull de '{HUB_NAME}': {e}")
        print("   Verifique LANGSMITH_API_KEY no .env e sua conexão de rede.")
        return 1

    try:
        data = {
            "name": HUB_NAME,
            "source": "LangSmith Prompt Hub (pull)",
            "input_variables": list(getattr(prompt, "input_variables", [])),
            "messages": [_message_to_dict(m) for m in prompt.messages],
        }
    except Exception as e:
        print(f"❌ Estrutura inesperada no prompt retornado: {e}")
        return 1

    if not save_yaml(data, OUTPUT_PATH):
        return 1

    print(f"✅ Prompt salvo em {OUTPUT_PATH}")
    print(f"   Mensagens: {len(data['messages'])} | Variáveis: {data['input_variables']}")
    return 0


def main() -> int:
    print_section_header(f"Pull do Prompt v1 — {HUB_NAME}")
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1
    return pull_prompts_from_langsmith()


if __name__ == "__main__":
    sys.exit(main())
