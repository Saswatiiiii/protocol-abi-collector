# 📌 DeFi Protocols ABI & Events Dataset

## 🎯 Goal
We collected a dataset of **DeFi protocols → their smart contracts → and the events those contracts emit**.

This project demonstrates:
- Fetching contract addresses for multiple DeFi protocols
- Getting their **ABIs** programmatically from block explorer APIs
- Extracting **events** from the ABIs
- Structuring the data into a clean JSON dataset

---

## 📂 Project Structure
```
project_root/
│
├── protocols.csv              # Provided by DeFiLlama (all protocols & networks)
├── contracts.csv              # Manually curated subset of protocols & contracts (our sample)
├── fetch_abis.py              # Script to fetch contract ABIs programmatically
├── extract_events.py          # Script to extract events from ABI and build final dataset
├── protocols_with_abi.json    # Output from fetch_abis.py
├── final_dataset.json         # Output from extract_events.py (table-like JSON)
└── README.md                  # This file
```

---

## 🚦 Approach

### **1️⃣ Contract Address Collection**
- We were given a huge `protocols.csv` from DeFiLlama.
- Fetching every contract for every protocol programmatically would take hours and produce a massive dataset.
- **Instead, we manually curated `contracts.csv`** by selecting a few key protocols (Zerolend, Stargate, Uniswap, Aave) and adding multiple contracts per chain.
- This provides a representative dataset while keeping it manageable.

### **2️⃣ ABI Fetching**
- Used Etherscan-compatible APIs to:
  - Check if the contract is verified.
  - Download its ABI.
- Saved results into `protocols_with_abi.json`.

### **3️⃣ Event Extraction**
- Parsed each ABI.
- Extracted only `event` definitions (name + arguments).
- Converted them into human-readable strings like:
  ```
  Swap(sender address, recipient address, amount0 int256, amount1 int256)
  ```
- Saved structured output into `final_dataset.json`.

---

## 📊 Final Output
Example entry in `final_dataset.json`:
```json
{
  "protocol": "uniswap_v2",
  "network": "ethereum",
  "contract_address": "0xC0AeE478e3658e2610c5F7A4A2E1777cE9e4f2Ac",
  "verified": "yes",
  "events": "PairCreated(token0 address, token1 address, pair address, uint256)"
}
```

---

## ✅ Deliverables
- **contracts.csv** (curated contract list)
- **protocols_with_abi.json** (contracts + ABIs)
- **final_dataset.json** (contracts + extracted events, table format)
- **README.md** (this documentation)

---

## 🔑 Key Takeaways
- Demonstrates fetching and processing ABIs.
- Shows event extraction and data structuring.
- Balances completeness with practicality by curating a smaller dataset.

---