# Spec: Holiday Calendar (ingestão de feriados e emendas)

## Purpose
Identificar as datas que valem a pena monitorar: feriados estaduais e
municipais do RJ e suas emendas (bridge days).

## Requirements

### Requirement: Fonte via endpoint de IA
O sistema SHALL consumir um endpoint de IA para obter, em JSON
estruturado, os feriados BR-RJ-state e BR-RJ-rio-municipal do ano.

### Requirement: Derivação local de emendas
As emendas SHALL ser derivadas localmente por regra determinística
(terça -> emenda segunda; quinta -> emenda sexta), nunca solicitadas à IA.

#### Scenario: Feriado numa quinta-feira
- **GIVEN** feriado em 2026-06-04 (quinta)
- **WHEN** a janela de viagem é derivada
- **THEN** a janela é qui..dom com has_bridge = true

### Requirement: Degradação graciosa
Se o endpoint de IA estiver indisponível, o sistema SHALL usar o último
calendário local válido (StaticCalendarProvider) e SHALL NOT abortar o cron.
