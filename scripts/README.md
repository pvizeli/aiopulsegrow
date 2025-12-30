# Scripts

Utility scripts for development and testing.

## fetch_mock_data.py

Fetches real data from the Pulsegrow API and generates mock test fixtures.

### Usage

```bash
python scripts/fetch_mock_data.py YOUR_API_KEY
```

### What it does

1. Connects to the Pulsegrow API using your API key
2. Fetches data from all available endpoints:
   - All devices and sensors
   - Hubs
   - Recent device data
   - Device data ranges
   - Sensor details and readings
   - Timeline events
   - Triggered thresholds
   - User usage information
   - Light readings (for Pro devices)
3. Saves the data to `tests/fixtures/mock_data.py` as Python constants

### Output

The script creates realistic mock data that you can use in your tests:

```python
from tests.fixtures.mock_data import ALL_DEVICES, HUBS, SENSOR_DETAILS

# Use in your tests with aioresponses
mock.get(f"{BASE_URL}/all-devices", payload=ALL_DEVICES)
```

### Troubleshooting

If you get a `401 Unauthorized` error, check that:
- Your API key is valid and active
- You're using the correct API key (copy it exactly from your Pulsegrow account settings)

If you get `404 Not Found` errors, that's normal for endpoints that don't have data yet (like timeline events or triggered thresholds on a new account).

**Note about Light Readings**: The current mock data doesn't include light readings. To generate mock data with light readings, you need to run the script with an API key that has access to a PulsePro device (deviceType == 1 or devices with `proLightReadingPreviewDto`). The script will automatically detect Pro devices and fetch their light readings.

### Security Note

⚠️ **Important**: Use a test/development API key for this script. Never commit the generated `mock_data.py` file if it contains sensitive information. The `.gitignore` is configured to exclude `tests/fixtures/mock_data.py` by default.

### Requirements

This script requires the development dependencies to be installed:

```bash
pip install -e ".[dev]"
```
