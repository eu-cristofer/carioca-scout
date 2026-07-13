# Spec: Dashboard (camada de apresentação)

## Purpose
Exibir os deals em um dashboard read-only, estático, hospedado no
GitHub Pages, otimizado para navegador de iPad.

## Requirements

### Requirement: Stack estática
O dashboard SHALL usar apenas HTML, CSS e JavaScript puro, sem build
step e sem dependências externas de runtime.

### Requirement: Contrato deals.json
O dashboard SHALL consumir exclusivamente docs/deals.json com o shape:
{generated_at, deals[{origin, dest, travel_date, holiday, price_brl,
baseline_brl, drop_pct, trend[]}]}. Qualquer mudança de shape SHALL
passar por proposta OpenSpec e atualizar backend + frontend + teste
de contrato na MESMA change.

### Requirement: Cards por destino
Cada deal SHALL ser renderizado como card contendo rota, data, feriado,
preço atual, indicador visual da % de queda e minigráfico (sparkline)
da tendência histórica (trend[], máx. 14 pontos).

### Requirement: iPad-first
Layout SHALL ser confortável em Safari/iPad (touch targets >= 44pt,
grid responsivo 1-3 colunas, sem interações hover-only).

#### Scenario: deals.json vazio
- **GIVEN** payload com deals = []
- **WHEN** a página carrega
- **THEN** exibe estado vazio amigável ("nenhuma promoção hoje"), sem erro
