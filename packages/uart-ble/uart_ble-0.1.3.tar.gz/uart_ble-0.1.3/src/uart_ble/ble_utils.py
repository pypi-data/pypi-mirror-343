"""Sample doc string."""

import asyncio

from bleak import BleakClient, BleakScanner
from loguru import logger

from uart_ble.definitions import BLE_TIMEOUT, RX_CHAR_UUID, TX_CHAR_UUID


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


class BLEDevice:
    """BLE device class."""

    def __init__(self, target_name: str):
        self.target_name: str = target_name
        self.name: str | None = None
        self.address: str | None = None
        self.client: BleakClient | None = None
        self.handler: BLEHandler | None = None

    async def find_device(self) -> bool:
        """Find the BLE device with the given name."""
        devices = await BleakScanner.discover(timeout=BLE_TIMEOUT)
        device = next(
            (d for d in devices if d.name and self.target_name in d.name), None
        )

        if not device:
            self._list_devices(devices)
            msg = f"Could not find device with name '{self.target_name}'."
            logger.error(msg)
            raise NameError(msg)

        self.address = device.address
        self.name = device.name
        logger.info(f"Found device: {self.name} — {self.address}")
        return True

    @staticmethod
    def _list_devices(devices) -> None:
        """List the found BLE devices."""
        for device in devices:
            logger.info(
                f"{device.name or 'Unnamed'} — {device.address} — RSSI: {device.rssi} dBm"
            )

    async def connect_and_subscribe(self) -> BLEHandler:
        """Connect to the BLE device and start notifications.

        :return: BLEHandler instance for receiving data.
        """
        if not self.address:
            raise ValueError("Device address not set. Call find_device() first.")

        self.client = BleakClient(self.address)
        await self.client.connect()
        logger.info("Connected!")

        self.handler = BLEHandler()
        await self.client.start_notify(TX_CHAR_UUID, self.handler.handle_rx)

        return self.handler

    async def send_command(self, command: str) -> None:
        """Send a command to the BLE device.

        :param command: The command string to send
        """
        if not self.client or not self.client.is_connected:
            raise ValueError(
                "Device not connected. Call connect_and_subscribe() first."
            )

        # Add a new line if not present
        if not command.endswith("\n"):
            command += "\n"

        # Convert string to bytes and send
        command_bytes = command.encode("utf-8")
        await self.client.write_gatt_char(RX_CHAR_UUID, command_bytes)
        logger.info(f"Sent command: {command.strip()}")

    async def send_int_command(self, command: int) -> None:
        """Send an integer command to the BLE device.

        :param command: Integer command to send.
        """
        if not self.client or not self.client.is_connected:
            raise ValueError(
                "Not connected to a device. Call connect_and_subscribe() first."
            )

        try:
            # Convert integer to bytes
            command_bytes = command.to_bytes(4, byteorder="little")
            await self.client.write_gatt_char(RX_CHAR_UUID, command_bytes)
            logger.info(f"Integer command sent: {command}")
        except Exception as e:
            logger.error(f"Failed to send integer command: {e}")
            raise

    async def disconnect(self) -> None:
        """Stop notifications and disconnect from the BLE device."""
        if self.client and self.client.is_connected:
            await self.client.stop_notify(TX_CHAR_UUID)
            await self.client.disconnect()
            logger.info("Disconnected.")
