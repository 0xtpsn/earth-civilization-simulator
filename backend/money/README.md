# Money Module

Financial accounts, wallets, assets, and transactions — the accounting layer separate from macro economy.

## Structure

- **`wallets/`** — Persistent balances per agent/player
- **`assets/`** — Owned property and goods
- **`transactions/`** — Financial operations
- **`banking/`** — Financial institutions
- **`era-currency/`** — Currency systems

## Separation from Economy

This module handles **accounts and transactions**, while `economy/` handles **macro behavior**:
- Economy: supply/demand, prices, markets
- Money: who owns what, account balances, transactions

