"""Example showing Home Assistant integration pattern."""

import asyncio

from aiohttp import ClientSession

from aiopulsegrow import PulsegrowClient, PulsegrowError


class PulsegrowIntegration:
    """Example Home Assistant integration class."""

    def __init__(self, api_key: str, session: ClientSession) -> None:
        """Initialize the integration.

        Args:
            api_key: Pulsegrow API key
            session: aiohttp ClientSession (managed by Home Assistant)
        """
        self.client = PulsegrowClient(api_key=api_key, session=session)
        self._devices: list[dict] = []

    async def async_setup(self) -> bool:
        """Set up the integration.

        Returns:
            True if setup was successful
        """
        try:
            # Fetch initial data
            all_devices = await self.client.get_all_devices()
            self._devices = all_devices.get("devices", [])
            return True
        except PulsegrowError as err:
            print(f"Setup failed: {err}")
            return False

    async def async_update(self) -> None:
        """Update data from Pulsegrow API."""
        try:
            all_devices = await self.client.get_all_devices()
            self._devices = all_devices.get("devices", [])
        except PulsegrowError as err:
            print(f"Update failed: {err}")

    async def async_unload(self) -> None:
        """Unload the integration."""
        # Close the client (but not the session - HA manages it)
        await self.client.close()

    @property
    def devices(self) -> list[dict]:
        """Get cached devices.

        Returns:
            List of device dictionaries
        """
        return self._devices


async def main() -> None:
    """Run example."""
    api_key = "your-api-key-here"

    # In Home Assistant, the session is created once and reused
    async with ClientSession() as session:
        integration = PulsegrowIntegration(api_key=api_key, session=session)

        # Setup
        if await integration.async_setup():
            print("Integration setup successful!")
            print(f"Found {len(integration.devices)} devices")

            # Periodic updates (in HA this would be done by the coordinator)
            for i in range(3):
                await asyncio.sleep(5)
                await integration.async_update()
                print(f"Update {i+1}: {len(integration.devices)} devices")

            # Cleanup
            await integration.async_unload()
        else:
            print("Integration setup failed!")


if __name__ == "__main__":
    asyncio.run(main())
