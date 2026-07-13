# Delta: dashboard

## MODIFIED Requirements

### Requirement: Cards por destino
Cada deal SHALL ser renderizado como card contendo rota, data, feriado,
preço atual, indicador visual da % de queda **e minigráfico (sparkline)
da tendência histórica (trend[], máx. 14 pontos)**.

#### Scenario: Card com histórico curto
- **GIVEN** um deal com trend de 3 pontos
- **WHEN** o card é renderizado
- **THEN** a sparkline desenha os 3 pontos sem erro
