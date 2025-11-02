import asyncio
import requests
import sqlite3
from pakakumi_analyzer.app.config import DB_PATH

async def run_collector_loop():
    print("🕸️ Collector loop started — waiting for rounds...")

    while True:
        try:
            # Example: Replace this URL with your real game data source endpoint
            url = "https://api.pakakumi.io/api/rounds/latest"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()

                # Extract a fake field for now (adjust to your real API shape)
                latest_round = data.get("round", None)
                if latest_round:
                    print(f"💾 Saving round {latest_round} to DB...")
                    conn = sqlite3.connect(DB_PATH)
                    c = conn.cursor()
                    c.execute(
                        "INSERT INTO rounds (round_number, crash_point) VALUES (?, ?)",
                        (latest_round, float(data.get("crashPoint", 1.0))),
                    )
                    conn.commit()
                    conn.close()
                else:
                    print("⚠️ No new round data available.")
            else:
                print(f"⚠️ Request failed: {response.status_code}")

        except Exception as e:
            print(f"❌ Collector error: {e}")

        # Wait before next fetch
        await asyncio.sleep(15)
