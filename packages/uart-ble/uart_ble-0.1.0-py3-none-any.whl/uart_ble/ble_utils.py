"""Sample doc string."""

import asyncio

from bleak import BleakClient, BleakError, BleakScanner
from loguru import logger

from uart_ble.definitions import BLE_TIMEOUT, TX_CHAR_UUID


async def find_device(target_name: str):
    """Find the BLE device with the given name."""
    devices = await BleakScanner.discover(timeout=BLE_TIMEOUT)
    device = next((d for d in devices if d.name and target_name in d.name), None)
    return device


def list_devices(devices) -> None:
    """List the found BLE devices."""
    if not devices:
        logger.error("No BLE devices found.")
        return

    for device in devices:
        logger.info(
            f"{device.name or 'Unnamed'} — {device.address} — RSSI: {device.rssi} dBm"
        )


class BLEHandler:
    """BLE handler that stores only the most recent line."""

    def __init__(self):
        self._buffer = b""
        self.latest_line = None
        self._new_data_event = asyncio.Event()

    def handle_rx(self, _, data):
        """Handle received data."""
        self._buffer += data
        while b"\n" in self._buffer:
            line, self._buffer = self._buffer.split(b"\n", 1)
            self.latest_line = line.decode("utf-8").strip()
            self._new_data_event.set()  # Signal that new data is available

    async def get_latest(self) -> str:
        """Wait for and return the latest line of data."""
        await self._new_data_event.wait()
        self._new_data_event.clear()
        return self.latest_line


async def list_services(client) -> None:
    """List the services of the connected device."""
    services = await client.get_services()
    for service in services:
        logger.info(f"[Service] {service.uuid}")
        for char in service.characteristics:
            logger.info(f"└─ [Characteristic] {char.uuid} — {char.properties}")


async def read_device(device_name: str):
    """Stream data from the BLE device."""
    device = await find_device(target_name=device_name)
    if not device:
        list_devices(await BleakScanner.discover(timeout=BLE_TIMEOUT))
        msg = f"Could not find device named '{device_name}'."
        logger.error(msg)
        raise Exception(msg)

    async with BleakClient(device.address) as client:
        logger.info("Connected!")
        handler = BLEHandler()
        await client.start_notify(TX_CHAR_UUID, handler.handle_rx)

        try:
            while True:
                input("Press Enter to get the latest IMU reading...")
                latest = await handler.get_latest()
                logger.info(f"📥 Latest: {latest}")
        except KeyboardInterrupt:
            logger.warning("Interrupted.")
        finally:
            await client.stop_notify(TX_CHAR_UUID)
            await client.disconnect()
            logger.info("Disconnected.")


async def stream_uart_ble(microcontroller_name: str):
    """Run the main function."""
    task = asyncio.create_task(read_device(device_name=microcontroller_name))
    try:
        await task
    except BleakError as bleak_err:
        logger.error(bleak_err)
    except KeyboardInterrupt:
        task.cancel()
        await task
