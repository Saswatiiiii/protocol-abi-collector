# 📌 DeFi Protocol Contract & Event Collection

## 🎯 Goal
Build a dataset of **protocols → contracts → events** across multiple blockchain networks.

---

## 📁 Project Structure
```
📂 project-root
 ├── protocols.csv           # Provided by Zeru (list of protocols & networks)
 ├── generate_contracts.csv  # Generate contract address
 ├── contracts.csv           # Programmatically curated contract addresses
 ├── fetch_abis.py           # Fetches ABIs for each contract address
 ├── extract_events.py       # Extracts events from ABIs into final dataset
 ├── protocols_with_abi.json # Output with ABIs & verification status
 ├── final_dataset.json      # Cleaned table-like JSON with events only
 ├── README.md               # Project documentation
 └── analysis.md             # Technical explanation & insights
```

---

## 🚦 Workflow

### 1️⃣ Generate Contract Addresses
We started from `protocols.csv` (provided by Zeru) and used **`generate_contracts.py`** to attempt to fetch all available contract addresses programmatically from sources like DefiLlama or protocol documentation.  
- Due to the large number of protocols (thousands), the script was slow and generated a very large file.  
- To keep the project manageable and focused on demonstrating the process, we curated a **subset** of `contracts.csv` manually after running the script partially.

### 2️⃣ Fetch ABIs
Run:
```bash
python fetch_abis.py
```
- Fetches ABIs via Etherscan/Polygonscan/etc.
- Adds `verified` status and `contractName` if available.
- Produces `protocols_with_abi.json`.

### 3️⃣ Extract Events
Run:
```bash
python extract_events.py
```
- Parses ABIs to extract only `event` definitions.
- Produces `final_dataset.json`.

### 4️⃣ Output Format
Example row from `final_dataset.json`:
```json
{
    "protocol": "insurace",
    "network": "ethereum",
    "contract_address": "0x544c42fbb96b39b21df61cf322b5edc285ee7429",
    "contractName": "AdminUpgradeabilityProxy",
    "role": "unknown",
    "verified": "yes",
    "events": "AdminChanged(previousAdmin address, newAdmin address), Upgraded(implementation address)"
  }
```

---

## ⚠️ Notes & Limitations
- Many contracts are unverified or belong to networks not supported by Etherscan APIs — these will show `"verified": "no"` and no ABI.
- The dataset focuses on representative protocols due to time/resource constraints.

---