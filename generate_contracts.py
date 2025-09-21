import csv
import requests
import time

INPUT_FILE = "protocols.csv"
OUTPUT_FILE = "contracts.csv"

def fetch_protocol_info(protocol_slug):
    url = f"https://api.llama.fi/protocol/{protocol_slug}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception as e:
        print(f"Error fetching {protocol_slug}: {e}")
        return None

def main():
    contracts = []
    missing_protocols = []

    with open(INPUT_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            protocol = row['protocol']
            network = row['network']

            print(f"🔎 Fetching {protocol} ({network})...")
            data = fetch_protocol_info(protocol)

            if not data:
                missing_protocols.append(protocol)
                continue

            # Parse addresses if available
            addresses = []
            if 'address' in data:
                if isinstance(data['address'], dict):
                    addresses = data['address'].get(network, [])
                elif isinstance(data['address'], list):
                    addresses = data['address']
                elif isinstance(data['address'], str):
                    addresses = [data['address']]

            if addresses:
                for addr in addresses:
                    contracts.append({
                        "protocol": protocol,
                        "network": network,
                        "contract_address": addr,
                        "role": ""  # fill later if known
                    })
            else:
                missing_protocols.append(protocol)

            time.sleep(0.5)  # avoid rate limit

    # Save contracts.csv
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["protocol", "network", "contract_address", "role"])
        writer.writeheader()
        writer.writerows(contracts)

    print(f"✅ Saved {len(contracts)} contracts to {OUTPUT_FILE}")
    if missing_protocols:
        print("⚠️ Missing protocols:", set(missing_protocols))

if __name__ == "__main__":
    main()
