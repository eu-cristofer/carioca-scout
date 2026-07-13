# Spec: Alerting (gatilho de 25%)

## Purpose
Disparar alerta somente quando houver queda relevante e estatisticamente
confiável de preço, evitando ruído e falsos positivos.

## Requirements

### Requirement: Gatilho de queda de 25%
O sistema SHALL marcar uma tarifa como "deal" quando o preço do dia for
igual ou inferior a 75% da média móvel dos últimos 30 registros diários.

#### Scenario: Queda exata de 25% dispara
- **GIVEN** média móvel de R$400 nos últimos 30 dias
- **WHEN** o menor preço do dia é R$300
- **THEN** o deal é registrado (fronteira inclusa: >=)

#### Scenario: Queda de 24% não dispara
- **GIVEN** média móvel de R$400
- **WHEN** o menor preço do dia é R$304
- **THEN** nenhum deal é registrado

### Requirement: Baseline por média móvel de 30 dias
O baseline SHALL ser a média aritmética dos últimos 30 mínimos diários
da rota; com menos de 30 pontos, a média usa os pontos existentes.

### Requirement: Delta contínuo
O sistema SHALL calcular o delta relativo ((atual - baseline)/baseline)
a cada execução.

### Requirement: Guarda de cold start
O sistema SHALL NOT emitir alertas para rotas com menos de 7 observações
históricas, mesmo diante de quedas superiores a 25%.

#### Scenario: Primeiro dia de monitoramento
- **GIVEN** uma rota sem histórico
- **WHEN** o primeiro preço coletado está 75% abaixo do "normal"
- **THEN** o preço é gravado mas nenhum alerta é emitido
