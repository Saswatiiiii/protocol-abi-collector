import csv
import json
import requests
import time

# Mapping chain -> API base URL
CHAIN_API_BASE = {
    "ethereum": "https://api.etherscan.io/api",
    "polygon": "https://api.polygonscan.com/api",
    "bsc": "https://api.bscscan.com/api"
}

API_KEY = "ZNBRWN5M8RVMNIV39C61MYNJ51YUSBMTIV"  

def fetch_contract_info(api_base, address):
    """Fetch contract source + ABI + name from Etherscan-like APIs."""
    params = {
        "module": "contract",
        "action": "getsourcecode",
        "address": address,
        "apikey": API_KEY
    }
    r = requests.get(api_base, params=params, timeout=15)
    data = r.json()

    if data.get("status") == "1" and data.get("result"):
        result = data["result"][0]
        abi = result.get("ABI")
        contract_name = result.get("ContractName")
        if abi and abi != "Contract source code not verified":
            try:
                return {
                    "verified": True,
                    "abi": json.loads(abi),
                    "contract_name": contract_name
                }
            except json.JSONDecodeError:
                return {"verified": False, "abi": None, "contract_name": contract_name}
        return {"verified": False, "abi": None, "contract_name": contract_name}

    return {"verified": False, "abi": None, "contract_name": None}

def main():
    output = []
    with open("contracts.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [name.strip() for name in reader.fieldnames]  # handle extra spaces

        for row in reader:
            protocol = row["protocol"]
            network = row["network"].lower()
            address = row["contract_address"].strip()

            api_base = CHAIN_API_BASE.get(network)
            if not api_base:
                print(f"⚠️ Skipping {protocol} ({address}) - unsupported network: {network}")
                continue

            print(f"🔍 Fetching ABI for {protocol} ({address}) on {network}...")
            info = fetch_contract_info(api_base, address)

            output.append({
                "protocol": protocol,
                "network": network,
                "contract_address": address,
                "verified": info["verified"],
                "contractName": info.get("contract_name"),
                "abi": info["abi"]
            })

            time.sleep(0.3)  # avoid API rate limits

    with open("protocols_with_abi.json", "w", encoding="utf-8") as out:
        json.dump(output, out, indent=2)

    print(f"✅ Saved protocols_with_abi.json with {len(output)} contracts processed.")

if __name__ == "__main__":
    main()
