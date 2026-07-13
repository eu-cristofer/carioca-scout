# CariocaScout 🛫

Monitor automatizado de quedas de preço (≥25% vs média móvel de 30 dias)
em passagens saindo do Rio (GIG/SDU) para POA, FLN, NYC e FLR, focado
nos feriados estaduais e municipais do RJ e suas emendas.

**Este repo é um projeto-escola de Spec-Driven Development + TDD** com
OpenCode, OpenSpec e Skills. Comece pelo **[MANUAL.md](MANUAL.md)**.

## Quickstart

```bash
pip install pytest
python3 -m pytest -q                 # 42 testes
python3 scripts/run_daily.py         # um "dia de cron" manual
python3 -m http.server -d docs 8000  # dashboard em http://localhost:8000
```

## Mapa

| Onde | O quê |
|---|---|
| `openspec/specs/` | Fonte da verdade (4 specs vivas) |
| `openspec/changes/add-sparkline-trend/` | Exemplo de change congelada no meio do ciclo |
| `.opencode/skills/` | 4 skills: TDD, disciplina git/OpenSpec, etiqueta de scraper, dashboard iPad-first |
| `src/carioca_scout/` | Core puro + ports & adapters |
| `tests/` | Cada regra de negócio pinada por um teste nomeado |
| `docs/` | Dashboard estático (GitHub Pages) |

Licença: use como quiser para aprender.
