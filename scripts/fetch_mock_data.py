#!/usr/bin/env python3
"""Script to fetch real data from Pulsegrow API and generate mock test fixtures.

Usage:
    python scripts/fetch_mock_data.py <API_KEY>

This will fetch real data from the API and save it to tests/fixtures/mock_data.py
for use in unit tests.
"""

import asyncio
import json
import sys
from pathlib import Path

import aiohttp


async def _safe_get(
    session: aiohttp.ClientSession, url: str, params: dict | None = None
) -> tuple[int, dict | list | None]:
    """Safely fetch data from an endpoint and return status code and data."""
    try:
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                return resp.status, await resp.json()
            else:
                # Try to get error message
                try:
                    error_text = await resp.text()
                    if error_text:
                        print(f"      Error response: {error_text[:200]}")
                except Exception as e:
                    # Silently ignore if we can't read error text
                    _ = e
                return resp.status, None
    except Exception as e:
        print(f"      Exception: {e}")
        return 0, None


async def fetch_all_data(api_key: str) -> dict:
    """Fetch all available data from the Pulsegrow API."""
    base_url = "https://api.pulsegrow.com"
    headers = {"x-api-key": api_key}

    data = {}

    async with aiohttp.ClientSession(headers=headers) as session:
        print("Fetching data from Pulsegrow API...")

        # Fetch all devices
        print("  - Fetching all devices...")
        status, result = await _safe_get(session, f"{base_url}/all-devices")
        if status == 200 and result:
            data["all_devices"] = result
            print(f"    ✓ Got {len(data['all_devices'].get('deviceViewDtos', []))} devices")
        else:
            print(f"    ✗ Failed: {status}")

        # Fetch hub IDs
        print("  - Fetching hub IDs...")
        status, result = await _safe_get(session, f"{base_url}/hubs/ids")
        if status == 200 and result:
            data["hub_ids"] = result
            print(f"    ✓ Got {len(result)} hub IDs")
        else:
            print(f"    ✗ Failed: {status}")

        # If we have devices, fetch device-specific data
        if "all_devices" in data and data["all_devices"].get("deviceViewDtos"):
            device_id = data["all_devices"]["deviceViewDtos"][0]["id"]
            print(f"\n  Using device ID {device_id} for detailed queries...")

            # Recent data
            print("  - Fetching recent device data...")
            status, result = await _safe_get(session, f"{base_url}/devices/{device_id}/recent-data")
            if status == 200 and result:
                data["recent_data"] = result
                print("    ✓ Got recent data")
            else:
                print(f"    ✗ Failed: {status}")

            # Data range
            print("  - Fetching device data range...")
            status, result = await _safe_get(
                session,
                f"{base_url}/devices/{device_id}/data-range",
                {"start": "2024-01-01T00:00:00Z", "end": "2024-12-31T23:59:59Z"},
            )
            if status == 200 and result:
                data["data_range"] = result
                print(f"    ✓ Got {len(result)} data points")
            else:
                print(f"    ✗ Failed: {status}")

        # If we have sensors, fetch sensor-specific data
        if "all_devices" in data and data["all_devices"].get("universalSensorViews"):
            sensor_id = data["all_devices"]["universalSensorViews"][0]["id"]
            print(f"\n  Using sensor ID {sensor_id} for detailed queries...")

            # Sensor details
            print("  - Fetching sensor details...")
            status, result = await _safe_get(session, f"{base_url}/sensors/{sensor_id}/details")
            if status == 200 and result:
                data["sensor_details"] = result
                print("    ✓ Got sensor details")
            else:
                print(f"    ✗ Failed: {status}")

            # Sensor data range
            print("  - Fetching sensor data range...")
            status, result = await _safe_get(
                session,
                f"{base_url}/sensors/{sensor_id}/data-range",
                {
                    "start": "2024-01-01T00:00:00Z",
                    "end": "2024-12-31T23:59:59Z",
                    "limit": 10,
                },
            )
            if status == 200 and result:
                data["sensor_data"] = result
                print(f"    ✓ Got {len(result)} sensor readings")
            else:
                print(f"    ✗ Failed: {status}")

        # Timeline
        print("\n  - Fetching timeline...")
        status, result = await _safe_get(session, f"{base_url}/api/timeline")
        if status == 200 and result:
            data["timeline"] = result
            print(f"    ✓ Got {len(result)} timeline events")
        else:
            print(f"    ✗ Failed: {status}")

        # Triggered thresholds
        print("  - Fetching triggered thresholds...")
        status, result = await _safe_get(session, f"{base_url}/api/triggered-thresholds")
        if status == 200 and result:
            data["triggered_thresholds"] = result
            print(f"    ✓ Got {len(result)} triggered thresholds")
        else:
            print(f"    ✗ Failed: {status}")

        # User usage
        print("  - Fetching user usage...")
        status, result = await _safe_get(session, f"{base_url}/users")
        if status == 200 and result:
            data["user_usage"] = result
            print("    ✓ Got user usage data")
        else:
            print(f"    ✗ Failed: {status}")

        # Light readings (if available)
        if "all_devices" in data and data["all_devices"].get("deviceViewDtos"):
            for device in data["all_devices"]["deviceViewDtos"]:
                # Check if this is a Pro device (has proLightReadingPreviewDto or deviceType == 1)
                if "proLightReadingPreviewDto" in device or device.get("deviceType") == 1:
                    device_id = device["id"]
                    print(f"\n  Found Pro device {device_id}, fetching light readings...")
                    status, result = await _safe_get(
                        session,
                        f"{base_url}/api/light-readings/{device_id}",
                        {"page": 1, "limit": 10},
                    )
                    if status == 200 and result:
                        data["light_readings"] = result
                        print("    ✓ Got light readings")
                        break
                    else:
                        print(f"    ✗ Failed: {status}")

        # Fetch hub details if we got hub IDs
        if "hub_ids" in data and data["hub_ids"]:
            hub_id = data["hub_ids"][0]
            print(f"\n  Using hub ID {hub_id} for detailed query...")
            print("  - Fetching hub details...")
            status, result = await _safe_get(session, f"{base_url}/hubs/{hub_id}")
            if status == 200 and result:
                data["hub_details"] = result
                print("    ✓ Got hub details")
            else:
                print(f"    ✗ Failed: {status}")

    return data


def generate_mock_fixtures(data: dict) -> str:
    """Generate Python code for mock test fixtures."""
    code = '''"""Mock data fixtures generated from real Pulsegrow API responses.

This file contains realistic mock data for use in unit tests.
Generated by scripts/fetch_mock_data.py
"""

'''

    # Add each data type as a constant
    for key, value in data.items():
        const_name = key.upper()
        code += f"{const_name} = "
        # Use json.dumps but convert JS null/true/false to Python None/True/False
        json_str = json.dumps(value, indent=4)
        json_str = json_str.replace(": null", ": None")
        json_str = json_str.replace(": true", ": True")
        json_str = json_str.replace(": false", ": False")
        code += json_str
        code += "\n\n"

    return code


async def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python scripts/fetch_mock_data.py <API_KEY>")
        print("\nThis script will fetch real data from the Pulsegrow API")
        print("and save it to tests/fixtures/mock_data.py for use in tests.")
        sys.exit(1)

    api_key = sys.argv[1]

    # Fetch data
    data = await fetch_all_data(api_key)

    if not data:
        print("\n❌ No data was fetched. Check your API key and try again.")
        sys.exit(1)

    # Create fixtures directory if it doesn't exist
    fixtures_dir = Path(__file__).parent.parent / "tests" / "fixtures"
    fixtures_dir.mkdir(parents=True, exist_ok=True)

    # Generate and save mock data
    mock_code = generate_mock_fixtures(data)
    output_file = fixtures_dir / "mock_data.py"
    output_file.write_text(mock_code)

    print(f"\n✅ Mock data saved to {output_file}")
    print(f"   Generated {len(data)} fixture constants")
    print("\nYou can now import this data in your tests:")
    print("    from tests.fixtures.mock_data import ALL_DEVICES, HUBS, etc.")


if __name__ == "__main__":
    asyncio.run(main())
