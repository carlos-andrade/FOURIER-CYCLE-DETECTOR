# Roadmap

## FASE 0 — Reconhecimento e baseline
Estado: CONCLUÍDA. Repositório reconhecido; licença MIT e commit inicial preservados; escopo e princípios registrados.

## FASE 1 — Núcleo matemático Python
Estado: EM IMPLEMENTAÇÃO. Primitivas FFT, regressão harmônica, fase, amplitude, energia e entropia implementadas. Baterias inicial e ampliada aprovadas no CI.

### FASE 1.1 — Robustez sintética
Estado: CONCLUÍDA EM TESTES SINTÉTICOS.
- Multi-frequência.
- Ruído.
- Modulação de amplitude.
- Frequência variável.
- Mudança de regime.
- Sensibilidade à janela.

### FASE 1.2 — Métricas espectrais por banda
Estado: IMPLEMENTADA; CI pendente.
- Restringir energia, entropia e concentração à banda efetivamente analisada.
- Validar limites de frequência e degenerescência.
- Não converter concentração/entropia em veredito automático de ciclo.

Critério de saída: CI verde e documentação das limitações.

## FASE 2 — Dados WINFUT Renko 30R
Criar adaptador e validar contrato com exportações reais do Profit; documentar regra Renko, timestamps, volume e origem.

Critério: histórico real validado e reproduzível.

## FASE 3 — Indicadores e FGSE
Implementar FCD, FHO, FES, FED, FRC e agregador FGSE.

Critério: integração e estados reproduzíveis.

## FASE 4 — Validação estatística
Causalidade, estabilidade, walk-forward, falsos positivos e análise econômica com custos.

Critério: relatório fora da amostra e limitações documentadas.

## FASE 5 — NTSL
Portar componentes viáveis; comparar NTSL com referência Python e validar no Profit Pro.

Critério: tolerâncias numéricas previamente definidas e testes operacionais aprovados.

## FASE 6 — Integração controlada com BrickMaster
Somente após certificação; inicialmente modo observacional/simulação, sem envio de ordens.

Critério: interface validada e aprovação específica da integração.
