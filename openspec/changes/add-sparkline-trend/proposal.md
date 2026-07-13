# Proposal: add-sparkline-trend

## Why
Os cards do dashboard mostram o preço e a % de queda, mas o usuário não
consegue julgar se a queda é um outlier ou uma tendência. Um minigráfico
dos últimos 14 mínimos diários dá esse contexto de graça.

## What Changes
- `deals.json` ganha o campo `trend: number[]` (máx. 14 pontos) por deal.
- `build_deal()` trunca a série ao rabo de 14 pontos.
- `app.js` renderiza uma sparkline SVG inline por card.
- Teste de contrato do payload atualizado NA MESMA change.

## Impact
- Specs afetadas: dashboard (Requirement "Cards por destino" e
  "Contrato deals.json")
- Código afetado: src/carioca_scout/deals.py, docs/app.js,
  tests/test_deals.py

## Open questions (resolvidas via grill-me antes do design)
- Q: 14 pontos ou 30? A: 14 — sparkline de 30 fica ilegível em card de iPad.
- Q: SVG inline ou canvas? A: SVG — zero dependências e escala nítida em Retina.
