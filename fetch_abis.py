import csv
import json
import requests
import time

API_KEYS = {
    "etherscan": "ZNBRWN5M8RVMNIV39C61MYNJ51YUSBMTIV",
    "snowscan": "ATJQERBKV1CI3GVKNSE3Q7RGEJ",
    "bscscan": "ZM8ACMJB67C2IXKKBF8URFUNSY",
    "arbiscan": "B6SVGA7K3YBJEQ69AFKJF4YHVX",
    "optimistic": "66N5FRNV1ZD4I87S7MAHCJVXFJ",   
}

# 🌐 Map network name to block explorer API base
CHAIN_API_BASE = {
    "ethereum": ("https://api.etherscan.io/api", API_KEYS.get("etherscan")),
    "snowscan": ("https://api.snowscan.xyz/api", API_KEYS.get("snowscan")),
    "bsc": ("https://api.bscscan.com/api", API_KEYS.get("bscscan")),
    "arbitrum": ("https://api.arbiscan.io/api", API_KEYS.get("arbiscan")),
    "optimism": ("https://api-optimistic.etherscan.io/api", API_KEYS.get("optimistic")),
}

def fetch_contract_info(api_base, api_key, address):
    """Fetch ABI + contract name from a block explorer."""
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": api_key
    }
    try:
        r = requests.get(api_base, params=params, timeout=15)
        data = r.json()
        if data.get("status") == "1":
            result = data["result"][0]
            abi = result.get("ABI")
            contract_name = result.get("ContractName")
            if abi and abi != "Contract source code not verified":
                return {"verified": True, "contract_name": contract_name, "abi": json.loads(abi)}
            else:
                return {"verified": False, "contract_name": contract_name, "abi": None}
    except Exception as e:
        print(f"❌ Error fetching {address}: {e}")
    return {"verified": False, "contract_name": None, "abi": None}

def main():
    output = []
    with open("contracts.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            protocol = row["protocol"]
            network = row["network"].lower()
            address = row["contract_address"]

            if network not in CHAIN_API_BASE:
                print(f"⚠️ Skipping {protocol} ({network}) — no API support")
                continue

            api_base, api_key = CHAIN_API_BASE[network]
            if not api_key:
                print(f"⚠️ No API key for {network}, skipping {address}")
                continue

            print(f"🔎 Fetching ABI for {protocol} ({address}) on {network}...")
            info = fetch_contract_info(api_base, api_key, address)

            output.append({
                "protocol": protocol,
                "network": network,
                "contract_address": address,
                "verified": info["verified"],
                "contractName": info["contract_name"],
                "abi": info["abi"]
            })

            time.sleep(0.3)  

    with open("protocols_with_abi.json", "w", encoding="utf-8") as out:
        json.dump(output, out, indent=2)

    print(f"✅ Saved protocols_with_abi.json ({len(output)} entries)")

if __name__ == "__main__":
    main()
