import json

def extract_events_from_abi(abi):
    events = []
    for item in abi:
        if item.get("type") == "event":
            name = item.get("name")
            inputs = item.get("inputs", [])
            args = ", ".join(f"{i['name']} {i['type']}" for i in inputs)
            events.append(f"{name}({args})")
    return events

def main():
    with open("protocols_with_abi.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    final_table = []
    total_contracts, verified_count, total_events = 0, 0, 0

    for entry in data:
        total_contracts += 1
        events = []
        if entry["verified"] and entry["abi"]:
            verified_count += 1
            events = extract_events_from_abi(entry["abi"])
            total_events += len(events)

        event_str = ", ".join(events) if events else "-"

        final_table.append({
            "protocol": entry["protocol"],
            "network": entry["network"],
            "contract_address": entry["contract_address"],
            "contractName": entry["contractName"],
            "role": entry.get("role", "unknown"),
            "verified": "yes" if entry["verified"] else "no",
            "events": event_str
        })

    with open("final_dataset.json", "w", encoding="utf-8") as out:
        json.dump(final_table, out, indent=2)

    print("✅ Saved final_dataset.json (flat table-like JSON)")
    print(f"📊 Summary:\n   - Total contracts: {total_contracts}\n   - Verified: {verified_count}\n   - Total events extracted: {total_events}")

if __name__ == "__main__":
    main()
