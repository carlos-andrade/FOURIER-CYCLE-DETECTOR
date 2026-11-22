# Validation report

## Latest verified checkpoints

### Mathematical core
- Synthetic robustness CI: SUCCESS, run 45062469716.
- Band-limited spectral metrics CI: SUCCESS, run 45062857043.
- These runs verify the tests in their respective commits only; no real market history was tested.

### B3-aligned offline market data boundary
- Implemented typed trade events and instrument identity.
- Enforces timezone-aware event timestamp.
- Keeps OBSERVED / PROXY / UNKNOWN aggressor states separate.
- Sequence audit reports duplicates, out-of-order messages and missing sequence values.
- CSV adapter reads local user-supplied files only.
- CI run for this layer is pending at commit time of this report.

## B3 source interpretation

Reviewed private project contracts:
- `CONTRATO_DADOS_B3_V2.0.md`
- `CONTRATO_CANONICO_INGESTAO_FONTES_EXTERNAS_V2.0.md`
- `ARQUITETURA_DUAL_COTAHIST_NEGOCIOS_INTRADIARIOS_2026-11-05.md`
- `PROVEDORES_E_GRANULARIDADE.md`
- `ativos/futuros/README.md`

COTAHIST is daily consolidated data, not tick-by-tick. Trade events and order-book feeds have separate contracts and granularities. Tick direction is not treated as aggressor side. UMDF, FIX/FAST, historical replay and other channels require independent entitlement evidence.

## Not certified
- No Profit Pro export has been inspected in this repository.
- No WINFUT Renko 30R event series has been validated.
- No real-time provider connection exists.
- No acquisition, storage licence, retention right or redistribution right is inferred.
- No backtest profitability or operational performance claim is made.
- No NTSL equivalence or BrickMaster integration has been performed.
