"""Example usage of the aiopulsegrow client."""

import asyncio
from datetime import datetime, timedelta, timezone

from aiohttp import ClientSession

from aiopulsegrow import PulsegrowClient, PulsegrowError


async def main() -> None:
    """Run example usage."""
    # Replace with your actual API key
    api_key = "your-api-key-here"

    async with ClientSession() as session:
        client = PulsegrowClient(api_key=api_key, session=session)

        try:
            # Get all devices
            print("Fetching all devices...")
            all_devices = await client.get_all_devices()
            print(f"Found {len(all_devices.get('devices', []))} devices")
            print(f"Found {len(all_devices.get('sensors', []))} sensors")

            # Get device IDs
            print("\nFetching device IDs...")
            device_ids = await client.get_device_ids()
            print(f"Device IDs: {device_ids}")

            if device_ids:
                device_id = device_ids[0]
                print(f"\nGetting recent data for device {device_id}...")
                recent_data = await client.get_device_recent_data(device_id)
                print(f"Recent data: {recent_data}")

                # Get data range for last 24 hours
                print(f"\nGetting 24-hour data range for device {device_id}...")
                end_time = datetime.now(timezone.utc)
                start_time = end_time - timedelta(days=1)
                data_range = await client.get_device_data_range(
                    device_id, start_time, end_time
                )
                print(f"Found {len(data_range)} data points in the last 24 hours")

            # Get sensor IDs
            print("\nFetching sensor IDs...")
            sensor_ids = await client.get_sensor_ids()
            print(f"Sensor IDs: {sensor_ids}")

            if sensor_ids:
                sensor_id = sensor_ids[0]
                print(f"\nGetting recent data for sensor {sensor_id}...")
                sensor_data = await client.get_sensor_recent_data(sensor_id)
                print(f"Sensor data: {sensor_data}")

                print(f"\nGetting sensor details for sensor {sensor_id}...")
                sensor_details = await client.get_sensor_details(sensor_id)
                print(f"Sensor details: {sensor_details}")

            # Get hub IDs
            print("\nFetching hub IDs...")
            hub_ids = await client.get_hub_ids()
            print(f"Hub IDs: {hub_ids}")

            if hub_ids:
                hub_id = hub_ids[0]
                print(f"\nGetting details for hub {hub_id}...")
                hub_details = await client.get_hub_details(hub_id)
                print(f"Hub details: {hub_details}")

            # Get timeline events
            print("\nFetching timeline events...")
            timeline = await client.get_timeline(count=5)
            print(f"Timeline: {timeline}")

            # Get triggered thresholds
            print("\nFetching triggered thresholds...")
            thresholds = await client.get_triggered_thresholds()
            print(f"Found {len(thresholds)} triggered thresholds")

            # Get user information
            print("\nFetching user information...")
            users = await client.get_users()
            print(f"Users: {users}")

        except PulsegrowError as err:
            print(f"Error: {err}")


if __name__ == "__main__":
    asyncio.run(main())
