# Plano de atualização: GitHub Actions Node 24

Data: 2026-05-22

## Objetivo

Eliminar o aviso residual de depreciação futura do Node.js 20 no GitHub Actions, mantendo o mesmo comportamento do pipeline atual e verificando localmente e remotamente que o projeto continua funcionando.

## Contexto verificado

- O workflow atual usa actions JavaScript que ainda estavam em majors antigos:
  - `actions/checkout@v4`
  - `actions/setup-python@v5`
- O GitHub atualizou o cronograma: a partir de 2026-06-16 os runners começam a usar Node 24 por padrão para actions JavaScript.
- A recomendação oficial para usuários de Actions é atualizar workflows para versões recentes das actions que rodam em Node 24.
- Já existem versões compatíveis:
  - `actions/checkout@v6` com runtime Node 24.
  - `actions/setup-python@v6`, com dependências compatíveis com Node 24.

Fontes oficiais consultadas:

- GitHub Changelog: <https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/>
- `actions/checkout` releases: <https://github.com/actions/checkout/releases/latest>
- `actions/setup-python` releases: <https://github.com/actions/setup-python/releases/latest>

## Escopo da mudança

Atualizar apenas o workflow de CI:

```yaml
- uses: actions/checkout@v6
- uses: actions/setup-python@v6
```

Nao alterar:

- Versao do Python do projeto (`3.11`).
- Jobs, comandos de lint, testes, Qdrant ou build de docs.
- Dependencias Python ou configuracoes de runtime local.
- Variaveis temporarias como `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` ou `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION`.

## Plano de implementação

1. Confirmar que o branch local esta sincronizado com `origin/main`.
2. Atualizar `.github/workflows/ci.yml` de `checkout@v4` para `checkout@v6`.
3. Atualizar `.github/workflows/ci.yml` de `setup-python@v5` para `setup-python@v6`.
4. Registrar este plano em `docs/superpowers/plans/2026-05-22-github-actions-node24-update.md`.
5. Rodar validacoes locais.
6. Commitar somente os arquivos relacionados.
7. Fazer push para `origin/main`.
8. Acompanhar o GitHub Actions remoto ate o fim.

## Plano de testes

Validacoes locais:

```bash
./.venv/bin/ruff check .
./.venv/bin/pytest -q
./.venv/bin/mkdocs build --strict
```

Validacao remota apos push:

```bash
gh run list --limit 3
gh run watch <run-id> --exit-status
```

O CI remoto precisa passar pelos mesmos blocos atuais:

- Install
- Lint
- Tests
- Qdrant integration
- Docs build

## Critérios de aceite

- O workflow nao referencia mais `actions/checkout@v4` nem `actions/setup-python@v5`.
- As validacoes locais passam.
- O push para `origin/main` e concluido.
- O run remoto do GitHub Actions conclui com sucesso.
- Nao ha mudancas funcionais fora do CI e da documentacao do plano.

## Garantia e rollback

Se a atualizacao falhar no GitHub Actions:

1. Inspecionar logs do job que falhou antes de reverter.
2. Se a falha for incompatibilidade clara das novas actions com o ambiente do repo, reverter o commit da atualizacao.
3. Se for falha transitoria de infraestrutura, rerodar o workflow uma vez antes de qualquer rollback.
4. Evitar `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION=true` como solucao permanente; usar apenas como mitigacao temporaria e documentada caso o GitHub remova Node 20 antes de a action afetada ter alternativa estavel.

## Diferencial pratico

A atualizacao remove uma pendencia preventiva de plataforma antes de virar quebra real de CI. Isso fortalece a narrativa publica do projeto: alem de ter benchmark, testes, integracao com Qdrant e build de documentacao, o repositorio tambem acompanha a evolucao da infraestrutura de CI.
