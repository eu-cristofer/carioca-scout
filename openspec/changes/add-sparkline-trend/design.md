# Design: add-sparkline-trend

## Decisão
Sparkline como `<svg viewBox="0 0 100 28">` com um único `<polyline>`,
normalizando a série trend[] para o viewBox no JS (função pura
`sparklinePoints(series)` em app.js, testável no console).

## Alternativas rejeitadas
- Chart.js: dependência externa viola o Requirement "Stack estática".
- Unicode braille sparkline: acessibilidade ruim, rendering irregular no iPad.

## Contrato
trend[] SEMPRE presente (pode ser lista curta no início do histórico);
frontend não assume length fixa.
