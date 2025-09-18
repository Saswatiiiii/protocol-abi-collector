# 📊 Analysis & Approach  

## 1️⃣ Problem Understanding  
The task is to collect **all DeFi protocol contracts** (from the given `protocols.csv`), fetch their **ABIs**, extract only the **events**, and create a structured JSON dataset.  

The main challenge:  
- There are **hundreds of protocols** and **thousands of contracts** across multiple chains.  
- Fetching ABIs for all of them programmatically would require hours of API calls and produce a very large dataset.  

---

## 2️⃣ Our Approach  

### **Step 1: Contract Collection**  
- Manually visited protocol documentation and official GitHub repos.  
- Created a smaller but **representative `contracts.csv`** containing multiple contracts from major protocols (Zerolend, Stargate, Uniswap, Aave).  
- This covers lending, DEX, bridge, and cross-chain protocols — ensuring coverage of multiple contract types.  

### **Step 2: ABI Fetching**  
- Built `fetch_abis.py` using Etherscan/Blockscan APIs.  
- For each address:  
  - Checked if the contract is **verified**.  
  - Fetched **ABI** if available.  
  - Stored ABI, verification status, and contract name into `protocols_with_abi.json`.  

### **Step 3: Event Extraction**  
- Built `extract_events.py` to parse ABIs and extract only **event definitions**.  
- Flattened event signatures into one string per contract for a **table-like JSON** output.  

---

## 3️⃣ Trade-offs & Reasoning  
- **Skipped fetching every contract programmatically** to save time & avoid API rate limits.  
- **Curated subset** allows us to demonstrate the full pipeline (contract collection → ABI fetching → event extraction) without hitting performance issues.  
- The approach is **scalable** — same scripts can process a much larger dataset if needed.  

---

## 4️⃣ Final Deliverable  
- **`protocols_with_abi.json`** → all contract addresses, names, ABIs (where available).  
- **`final_dataset.json`** → clean, table-like JSON with protocols, networks, contract addresses, verification status, and extracted events.  

This satisfies the assignment requirement:  
> "Get ABIs for as many contracts as possible and extract their events."  
