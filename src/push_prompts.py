"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê o prompt otimizado de prompts/bug_to_user_story_v2.yml
2. Valida a estrutura
3. Faz push PÚBLICO para o LangSmith Hub com metadata (description, tags)
"""

import sys
from typing import Tuple, List
from dotenv import load_dotenv
from langchain import hub

from utils import check_env_vars, print_section_header, validate_prompt_structure
from prompt_io import load_prompt_yaml, build_chat_prompt_template

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

YAML_PATH = "prompts/bug_to_user_story_v2.yml"

TAGS = [
    "bug-to-user-story",
    "pt-br",
    "few-shot",
    "role-prompting",
    "chain-of-thought",
    "skeleton-of-thought",
    "mba-exercise",
    "v2",
]


def validate_prompt(prompt_data: dict) -> Tuple[bool, List[str]]:
    """Valida a estrutura do prompt (delega para validate_prompt_structure)."""
    return validate_prompt_structure(prompt_data)


def _confirm_push(prompt_name: str) -> bool:
    """Pede confirmação interativa antes de pushar para o Hub público."""
    print(f"\n⚠️  Você está prestes a fazer push PÚBLICO de '{prompt_name}'.")
    print("   Isso cria uma nova versão visível no LangSmith Hub.")
    answer = input("   Confirma o push? [y/N]: ").strip().lower()
    return answer in ("y", "yes", "s", "sim")


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """Faz push do prompt otimizado para o LangSmith Hub (público)."""
    try:
        chat_prompt = build_chat_prompt_template(prompt_data)
    except Exception as e:
        print(f"❌ Falha ao construir ChatPromptTemplate: {e}")
        return False

    try:
        url = hub.push(
            prompt_name,
            chat_prompt,
            new_repo_is_public=True,
            new_repo_description=prompt_data.get("description", ""),
            tags=TAGS,
        )
    except Exception as e:
        print(f"❌ Falha no push de '{prompt_name}': {e}")
        print("   Verifique LANGSMITH_API_KEY no .env e sua conexão de rede.")
        print("   Confirme também que o handle do Hub corresponde à sua conta.")
        return False

    print("\n✅ Prompt publicado com sucesso!")
    print(f"   URL: {url}")
    return True


def main() -> int:
    print_section_header(f"Push do Prompt v2 — {YAML_PATH}")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    try:
        data = load_prompt_yaml(YAML_PATH)
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    prompt_name = data.get("name")
    if not prompt_name or "/" not in prompt_name:
        print(f"❌ Campo 'name' inválido no YAML: {prompt_name!r}")
        print("   Esperado formato '<handle>/<repo>' (ex: test1233456/bug_to_user_story_v2)")
        return 1

    print(f"📋 Prompt:    {prompt_name}")
    print(f"📋 Versão:    {data.get('version')}")
    print(f"📋 Técnicas:  {', '.join(data.get('techniques_applied', []))}")
    print(f"📋 Tags:      {', '.join(TAGS)}")
    print(f"📋 Descrição: {data.get('description', '')[:100]}...")

    if not _confirm_push(prompt_name):
        print("\n⏸️  Push cancelado pelo usuário.")
        return 0

    return 0 if push_prompt_to_langsmith(prompt_name, data) else 1


if __name__ == "__main__":
    sys.exit(main())
