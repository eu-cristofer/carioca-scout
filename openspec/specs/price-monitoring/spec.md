# Spec: Price Monitoring (coleta e histórico)

## Purpose
Coletar diariamente o menor preço por rota/data e manter um histórico
temporal local confiável.

## Requirements

### Requirement: Rotas monitoradas
O sistema SHALL monitorar voos com origem GIG e SDU e destinos POA, FLN,
NYC e FLR. As rotas SHALL ser configuráveis em config.py sem alteração
de lógica.

### Requirement: Janela de cobertura
O sistema SHALL cobrir janelas de viagem dentro dos próximos 12 meses,
derivadas do calendário de feriados; datas passadas SHALL ser ignoradas.

### Requirement: Coleta resiliente
A ausência de cotação para uma rota/data SHALL NOT interromper a
execução diária (o provedor retorna None; o pipeline segue).

### Requirement: Mínimo diário idempotente
O sistema SHALL gravar exatamente um registro por rota por dia-calendário
em price_history.json, contendo o MENOR preço observado naquele dia.
Reexecuções no mesmo dia SHALL manter o menor valor.

#### Scenario: Cron roda duas vezes no mesmo dia
- **GIVEN** registro de R$500 para GIG-POA hoje
- **WHEN** nova execução encontra R$480
- **THEN** o registro do dia passa a R$480 (e um R$999 posterior seria ignorado)

### Requirement: Esquema versionado
price_history.json SHALL conter schema_version; versões desconhecidas
SHALL causar erro explícito, nunca migração silenciosa.
