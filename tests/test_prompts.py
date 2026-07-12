"""
Testes automatizados para validação de prompts.

Estes testes são ESTÁTICOS: validam a estrutura do YAML do prompt otimizado
(prompts/bug_to_user_story_v2.yml) sem chamar nenhum LLM — rodam em
milissegundos e sem custo. São a rede de segurança que garante que o prompt
nunca perca suas propriedades essenciais (persona, few-shot, técnicas) numa
edição futura.

Asserts robustos por design: usam substrings estáveis (case-insensitive)
em vez de frases exatas, para não quebrar em refactors legítimos do prompt.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"


def load_prompts(file_path):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def prompt():
    """Carrega o prompt v2 uma vez para toda a suíte."""
    return load_prompts(PROMPT_PATH)


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in prompt, "campo 'system_prompt' ausente no YAML"
        assert isinstance(prompt["system_prompt"], str), "'system_prompt' deve ser texto"
        assert prompt["system_prompt"].strip(), "'system_prompt' está vazio"

    def test_prompt_has_role_definition(self, prompt):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        sp = prompt["system_prompt"].lower()
        assert "você é um" in sp or "você é uma" in sp, \
            "prompt não define persona com 'Você é um/uma...'"
        assert "product manager" in sp or "persona" in sp, \
            "persona não especificada (esperado cargo/papel como 'Product Manager')"

    def test_prompt_mentions_format(self, prompt):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        sp = prompt["system_prompt"].lower()
        indicators = ["user story", "critérios de aceitação", "markdown"]
        assert any(ind in sp for ind in indicators), \
            "prompt não menciona formato de saída (User Story padrão ou Markdown)"

    def test_prompt_has_few_shot_examples(self, prompt):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        examples = prompt.get("few_shot_examples")
        assert isinstance(examples, list), "'few_shot_examples' ausente ou não é lista"
        assert len(examples) >= 2, "Few-shot exige ao menos 2 exemplos"
        for i, ex in enumerate(examples):
            assert str(ex.get("human", "")).strip(), f"exemplo #{i} sem entrada 'human'"
            assert str(ex.get("ai", "")).strip(), f"exemplo #{i} sem saída 'ai'"

    def test_prompt_no_todos(self, prompt):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        parts = [prompt.get("system_prompt", "")]
        for ex in prompt.get("few_shot_examples", []):
            parts.append(str(ex.get("human", "")))
            parts.append(str(ex.get("ai", "")))
        content = "\n".join(parts)
        assert "[TODO]" not in content, "há marcador [TODO] esquecido no texto do prompt"
        assert "TODO" not in content, "há 'TODO' cru no texto do prompt"

    def test_minimum_techniques(self, prompt):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt.get("techniques_applied")
        assert isinstance(techniques, list), "'techniques_applied' ausente ou não é lista"
        assert len(techniques) >= 2, \
            f"liste ao menos 2 técnicas em 'techniques_applied' (encontrado: {techniques})"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
