# FOURIER CYCLE DETECTOR

**Motor central:** FOURIER GYROSCOPE  
**Mercado inicial:** WINFUT (B3)  
**Representação operacional:** Renko 30R  
**Pesquisa e referência matemática:** Python  
**Implementação operacional planejada:** NTSL / Profit Pro

## Objetivo

Desenvolver um sistema causal e verificável de análise harmônica para estimar ciclos, amplitude, fase, energia espectral, esgotamento e mudanças de regime. O sistema deve poder declarar que não existe ciclo confiável; não deve forçar uma interpretação para todo movimento.

## Estado do projeto

O repositório está em baseline documental. A FASE 0 (reconhecimento e definição inicial) foi concluída. A FASE 1 (núcleo matemático Python) é a próxima etapa. Ainda não há indicador certificado nem integração operacional.

## Princípios

- Python é a referência matemática para a futura implementação NTSL.
- Nenhum cálculo pode utilizar dados futuros.
- As estimativas são atualizadas com tijolos fechados; sinais históricos emitidos são imutáveis.
- Renko é indexado por eventos: um período de 20 tijolos não equivale a 20 minutos.
- Não assumir tamanho, reversão ou regra de construção do Renko sem evidência exportada do Profit.
- Não enviar ordens nesta fase.
- Não integrar ao BrickMaster antes da validação e aprovação específicas.
- Não usar indicadores prontos como substitutos dos componentes matemáticos próprios.

## Módulos planejados

1. FCD — Fourier Cycle Detector.
2. FHO — Fourier Harmonic Oscillator.
3. FES — Fourier Energy Spectrum.
4. FED — Fourier Exhaustion Detector.
5. FRC — Fourier Regime Classifier.
6. FGSE — Fourier Gyroscope State Engine, agregador de estado.

## Documentação

- [Arquitetura](docs/ARCHITECTURE.md)
- [Modelo matemático](docs/MATHEMATICAL_MODEL.md)
- [Especificação técnica](docs/TECHNICAL_SPECIFICATION.md)
- [Contrato de dados](docs/DATA_CONTRACT.md)
- [Estratégia de testes](docs/TEST_STRATEGY.md)
- [Roadmap](docs/ROADMAP.md)
- [Governança](GOVERNANCA/GOVERNANCE.md)

## Aviso

Este projeto é pesquisa e desenvolvimento. Resultados históricos ou sintéticos não garantem desempenho futuro. Nenhum componente está autorizado a gerar ordens reais.
