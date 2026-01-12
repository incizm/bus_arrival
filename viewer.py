import requests
from datetime import datetime, timezone
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

load_dotenv()
# ---------- Formatting helpers ----------

def format_time(iso_time: str) -> str:
    dt = datetime.fromisoformat(iso_time)
    return dt.strftime("%I:%M %p").lstrip("0")  # Windows-safe


def timing_description(iso_time: str) -> str:
    now = datetime.now(tz=timezone.utc)
    arrival = datetime.fromisoformat(iso_time)
    diff_min = round((arrival - now).total_seconds() / 60)

    if diff_min < 0:
        return "Already passed / data delay"
    elif diff_min == 0:
        return "Arriving now"
    else:
        return f"In {diff_min} min"


def decode_bus(bus: Dict[str, Any], label: str):
    if not bus or "time" not in bus:
        return None

    return {
        "label": label,
        "time": format_time(bus["time"]),
        "timing": timing_description(bus["time"]),
        "crowd": "Seats available" if bus.get("load") == "SEA" else bus.get("load"),
        "wheelchair_accessible": bus.get("feature") == "WAB",
        "live_tracking": bus.get("monitored") == 1,
    }


def deconstruct_bus_response(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    services_out = []

    for service in data.get("services", []):
        arrivals = list(filter(None, [
            decode_bus(service.get("next"), "Next bus"),
            decode_bus(service.get("subsequent"), "Following bus"),
            decode_bus(service.get("next3"), "Subsequent bus"),
        ]))

        services_out.append({
            "service_no": service["no"],
            "operator": service["operator"],
            "arrivals": arrivals
        })

    return services_out


# ---------- Main execution ----------

def main():

    bus_stop = input("Ënter bus stop code:")
    if bus_stop == "":
        bus_stop = 73019 
    URL = f"http://127.0.0.1:3000/?id={bus_stop}"

    try:
        response = requests.get(URL, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print("❌ Failed to fetch bus data:", e)
        return

    data = response.json()
    result = deconstruct_bus_response(data)

    for service in result:
        print(f"\n🚌 Bus {service['service_no']} ({service['operator']})")
        for a in service["arrivals"]:
            print(
                f"- {a['label']}: {a['time']} ({a['timing']}) | "
                f"{a['crowd']} | "
                f"{'WAB' if a['wheelchair_accessible'] else 'Non-WAB'} | "
                f"{'Live GPS' if a['live_tracking'] else 'No GPS'}"
            )


if __name__ == "__main__":
    main()
