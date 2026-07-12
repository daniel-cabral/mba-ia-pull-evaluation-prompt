# CLAUDE.md — Diretrizes do Projeto

## Contexto

Este projeto é um **exercício de MBA em Engenharia de Software com GenAI** do Daniel Cabral. O objetivo final é entregar o software descrito em [README.md](README.md): fazer pull, otimizar, push e avaliar prompts no LangSmith Prompt Hub, atingindo **>= 0.8** em todas as 5 métricas (Helpfulness, Correctness, F1-Score, Clarity, Precision).

> **Nota (2026-07-12):** o corte de aprovação do desafio foi **reduzido de 0.9 para 0.8** numa atualização do fork (README + `src/evaluate.py`, ambos agora em 0.8). Toda referência a "0.9" em iterações anteriores do MEMORIAL é histórica.

## Modo de Trabalho (OBRIGATÓRIO)

Este é um exercício **pedagógico**. O usuário precisa **aprender**, não apenas receber a solução pronta.

### Regras de colaboração

1. **Passo a passo, sempre.** Nunca executar múltiplas fases do README de uma vez. Uma etapa por vez, com confirmação explícita antes de avançar.
2. **Ensinar antes de codar.** Antes de escrever qualquer código ou arquivo, explicar:
   - O que vamos fazer nesta etapa
   - Por que essa abordagem (conceito, técnica, trade-off)
   - Como isso se conecta ao objetivo maior do exercício
3. **Usuário participa.** Perguntar, propor opções, deixar o Daniel decidir direções importantes (ex.: quais técnicas de prompt engineering aplicar, estrutura do YAML, estilo dos few-shots).
4. **Não adiantar trabalho.** Não criar `bug_to_user_story_v2.yml`, `pull_prompts.py`, `push_prompts.py` ou `test_prompts.py` sem antes planejar juntos e receber o "ok, pode escrever".
5. **Explicar o que cada mudança faz.** Após cada edit relevante, resumir brevemente o que foi feito e por quê — reforçando o aprendizado.
6. **Linguagem: Português (PT-BR).** O Daniel está no curso em português; responder em PT-BR por padrão.

### Fluxo padrão por etapa

```
1. Claude explica o conceito e o plano da etapa
2. Daniel faz perguntas / escolhe abordagem
3. Claude propõe a implementação (ainda sem escrever)
4. Daniel aprova
5. Claude implementa
6. Claude atualiza MEMORIAL.md com explicações + progresso
7. Claude resume o que foi feito e sugere a próxima etapa
```

### Memorial descritivo (obrigatório)

O arquivo [MEMORIAL.md](MEMORIAL.md) é o **diário de bordo** do exercício. Ele deve crescer incrementalmente a cada etapa:

- Conceitos explicados ao Daniel → vão para o memorial
- Decisões tomadas (provider, técnicas, estrutura) → vão para o memorial
- Progresso por etapa (checklist, status) → vai para o memorial
- Resultados de avaliações, iterações de prompt → vão para o memorial

**Nunca encerrar uma etapa sem atualizar o memorial.** É tão importante quanto o código entregue — é o registro de aprendizado do curso.

### O que NÃO fazer

- ❌ Gerar o prompt v2 otimizado inteiro sem antes discutir técnicas com o Daniel
- ❌ Implementar pull + push + testes tudo de uma vez
- ❌ "Só para adiantar" — adiantar trabalho quebra o propósito pedagógico
- ❌ Pular a explicação conceitual porque "é óbvio"

## Stack do projeto

- Python 3.9+, LangChain, LangSmith Prompt Hub, YAML
- LLMs suportados: OpenAI (gpt-4o-mini / gpt-4o) ou Gemini (gemini-2.5-flash)
- Arquivos prontos (NÃO alterar): `src/evaluate.py`, `src/metrics.py`, `src/utils.py`, `datasets/bug_to_user_story.jsonl`

## Entregáveis (a implementar juntos, nesta ordem)

1. `src/pull_prompts.py` — fazer pull do `leonanluppi/bug_to_user_story_v1`
2. `prompts/bug_to_user_story_v2.yml` — prompt otimizado com Few-shot + pelo menos uma técnica adicional
3. `src/push_prompts.py` — push do v2 para o LangSmith
4. `tests/test_prompts.py` — 6 testes pytest listados no README
5. `README.md` — documentar técnicas aplicadas, resultados e como executar
