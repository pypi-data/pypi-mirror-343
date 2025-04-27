#!/usr/bin/env python3

import os
import sys
import subprocess
import venv
import argparse
import csv

def ensure_venv():
    """Create venv if not present, and install required packages."""
    venv_dir = os.path.join(os.path.dirname(__file__), 'venv')
    python_executable = os.path.join(venv_dir, 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(venv_dir, 'bin', 'python')

    if not os.path.isdir(venv_dir):
        print("Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)

    # Install packages if needed
    try:
        subprocess.run([python_executable, "-c", "import requests"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Installing 'requests' and 'rich' inside virtual environment...")
        subprocess.check_call([python_executable, "-m", "pip", "install", "requests", "rich"])

    return python_executable

def get_dmr_ids(callsign):
    """Query DMR IDs by callsign."""
    import requests

    url = f"https://www.radioid.net/api/dmr/user/?callsign={callsign.upper().strip()}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            return []

        return [{"callsign": record["callsign"], "dmr_id": record["id"]} for record in data["results"]]

    except requests.RequestException as e:
        print(f"Error querying {callsign}: {e}")
        return []

def pretty_print(results):
    """Pretty print results using rich."""
    from rich.table import Table
    from rich.console import Console

    console = Console()
    table = Table(title="📡 DMR ID Lookup Results 📡")

    table.add_column("Callsign", style="cyan", no_wrap=True)
    table.add_column("DMR ID", style="magenta")

    for result in results:
        table.add_row(result['callsign'], str(result['dmr_id']))

    console.print(table)

def save_to_csv(results, filename):
    """Save results to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["callsign", "dmr_id"])
        writer.writeheader()
        writer.writerows(results)
    print(f"✅ Saved results to {filename}")

def main():
    if sys.prefix == sys.base_prefix:
        python_executable = ensure_venv()
        subprocess.check_call([python_executable] + sys.argv)
        sys.exit(0)

    parser = argparse.ArgumentParser(description="Lookup DMR ID(s) by callsign(s).")
    parser.add_argument("callsigns", nargs="+", help="One or more callsigns to lookup")
    parser.add_argument("--pretty", action="store_true", help="Pretty print results as a table")
    parser.add_argument("--save", metavar="FILENAME", help="Save results to a CSV file")

    args = parser.parse_args()

    all_results = []
    for callsign in args.callsigns:
        results = get_dmr_ids(callsign)
        if not results:
            print(f"❌ No DMR IDs found for {callsign.upper()}")
        else:
            all_results.extend(results)

    if not all_results:
        print("No results found. Exiting.")
        sys.exit(1)

    if args.pretty:
        pretty_print(all_results)
    else:
        for entry in all_results:
            print(f"📡 {entry['callsign']}: {entry['dmr_id']}")

    if args.save:
        save_to_csv(all_results, args.save)

if __name__ == "__main__":
    main()

