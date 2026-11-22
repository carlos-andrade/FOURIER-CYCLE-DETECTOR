# FASE 2.1 — Ficha de recolha de evidências Profit One

Estado: MODELO PARA PREENCHIMENTO — não constitui certificação dos dados.

## 1. Identificação da captura

- Data/hora da exportação:
- Versão do Profit One:
- Ativo/símbolo exatamente como aparece na plataforma:
- Vencimento/contrato:
- Provedor/fonte de dados:
- Tipo de gráfico exatamente como aparece na plataforma: 60K Trades
- Período exportado:
- Fuso horário configurado:
- Formato e opções de exportação:
- A exportação contém barras fechadas, barra em formação ou ambas?:

## 2. Configuração do gráfico

Registar os parâmetros exatamente como apresentados no Profit One. Não reinterpretar nem converter os nomes dos campos.

- Valor configurado para construção da barra:
- Unidade/critério selecionado na interface:
- Sessão/horário aplicado:
- Ajuste de contratos/série contínua:
- Opções de histórico:
- Outros parâmetros relevantes:

Anexar captura de ecrã da configuração, ocultando dados pessoais, números de conta e informação sensível.

## 3. Dicionário dos campos exportados

Preencher uma linha por coluna exportada.

| Nome exato da coluna | Descrição apresentada pela plataforma | Unidade | Exemplo | Observações |
|---|---|---|---|---|
| | | | | |

Não assumir que volume, quantidade de contratos, número de negócios e volume financeiro são equivalentes.

## 4. Semântica temporal

- A coluna Data representa: ABERTURA / FECHO / ÚLTIMO NEGÓCIO / OUTRO / NÃO SEI
- Se OUTRO, descrever:
- Precisão original do timestamp:
- Fuso horário IANA:
- Existem timestamps repetidos?:
- Como a plataforma ordena barras com o mesmo timestamp?:
- Como identificar o início e o fim de cada barra?:

Se não souber algum item, escrever UNKNOWN. Não inferir.

## 5. Construção e completude das barras

- Existe coluna explícita de número de negócios por barra?:
- Existe coluna explícita de quantidade de contratos?:
- Existe coluna explícita de volume financeiro?:
- Existe identificador/contador sequencial da barra?:
- A plataforma exporta barras parciais/incompletas?:
- Como são tratadas a primeira e a última barra da sessão?:
- Como são tratadas interrupções, leilões e sessões overnight?:

## 6. Investigação da alteração observada em 14/10/2026

A auditoria anterior encontrou uma alteração na distribuição dos preços relativamente à grelha candidata de 5 pontos. Esta grelha não foi certificada como tick oficial.

- Houve rolagem de vencimento nessa data?:
- Houve alteração do símbolo ou contrato?:
- Houve alteração do provedor/feed?:
- Houve alteração de configuração, histórico ou método de exportação?:
- Houve ajuste de série contínua?:
- Evidência documental/captura que sustenta a resposta:

Não arredondar nem corrigir OHLC para tentar eliminar a diferença.

## 7. Amostra a anexar

Preferência: exportação nativa e curta, cobrindo pelo menos:
- uma sessão completa anterior a 14/10/2026, se ainda disponível;
- uma sessão completa posterior a 14/10/2026;
- se possível, uma amostra que atravesse a rolagem de contrato.

Anexar o ficheiro original sem abrir e voltar a guardar em Excel, se isso puder alterar tipos, precisão ou timestamps. Não remover linhas duplicadas. Não reordenar. Não aplicar fórmulas nem arredondamentos.

Se houver dados proprietários ou restrições contratuais, não os publicar no GitHub. Enviar apenas nesta conversa se tiver autorização para partilhar; caso contrário, fornecer metadados e uma amostra anonimizada/autorizada.

## 8. Direitos e proveniência

- Titular/fonte dos dados:
- Modalidade de acesso (tempo real, atrasado, histórico, outro):
- Termos/licença aplicáveis:
- Permissão para análise local:
- Permissão para armazenamento:
- Permissão para redistribuição/publicação:
- Restrições relevantes:

Nunca anexar credenciais, tokens, números de conta ou dados pessoais.

## 9. Declaração de integridade

- O ficheiro é uma exportação direta do Profit One?:
- Foi alterado após a exportação?:
- Se foi alterado, descrever todas as alterações:
- SHA-256 do ficheiro original (se disponível):

---

## Regra de análise

A equipa técnica irá preservar os valores originais e separar:
1. factos diretamente observados no ficheiro;
2. metadados declarados pelo utilizador;
3. documentação oficial/provedor;
4. hipóteses ainda não verificadas.

Nenhum campo desconhecido será preenchido por inferência. A FASE 2 só poderá ser certificada após os gates de identidade do instrumento, construção 60K, semântica temporal, proveniência dos preços, sessões e direitos de uso.
