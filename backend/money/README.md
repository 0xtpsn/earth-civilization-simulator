# Money Module

Financial accounts, wallets, assets, and transactions — the accounting layer separate from macro economy.

## Structure

- **`wallets/`** — Persistent balances per agent/player
  - Currency holdings
  - Multi-currency support
  - Balance tracking

- **`assets/`** — Owned property and goods
  - Land and real estate
  - Commodities
  - Equity and shares
  - Goods inventory
  - Era-appropriate assets

- **`transactions/`** — Financial operations
  - Ledger system
  - Receipts and records
  - Fraud detection
  - Escrow mechanisms

- **`banking/`** — Financial institutions
  - Loans and credit
  - Interest calculations
  - Creditworthiness assessment
  - Era-appropriate banking (medieval vs modern)

- **`era-currency/`** — Currency systems
  - Currency definitions per era
  - Exchange rules
  - Historical currency systems
  - Inflation adjustments

## Separation from Economy

This module handles **accounts and transactions**, while `economy/` handles **macro behavior**:
- Economy: supply/demand, prices, markets
- Money: who owns what, account balances, transactions

This separation allows:
- Detailed financial tracking
- Player/NPC wealth management
- Transaction history
- Banking systems

