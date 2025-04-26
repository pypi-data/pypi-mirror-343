__author__ = "Yu Hanjun"
__email__ = "yuhanjun@kersci.com"

import asyncio
from bleak import BleakClient, BleakError, BLEDevice, BleakScanner, BleakGATTCharacteristic
import re
from time import time as _now
from typing import Union as _Union, Optional as _Optional


class FindADeviceWithAddressPattern:
	def __init__(self, pattern: _Union[re.Pattern, str], timeout: float):
		if isinstance(pattern, str):
			self.pattern = re.compile(pattern)
		elif isinstance(pattern, re.Pattern):
			self.pattern = pattern
		else:
			raise TypeError('argument [pattern] must be typed str or re.Pattern.')

		self.timeout = timeout

	def __call__(self, device: BLEDevice, data):
		if re.match(self.pattern, device.address):
			return True
		return False

	async def find(self) -> _Optional[BLEDevice]:
		device = await BleakScanner.find_device_by_filter(self, self.timeout)
		return device


async def connect(device: BLEDevice, try_count: int, timeout: float = 10) -> BleakClient:
	client = BleakClient(device)
	counter = 0
	exception = None
	while counter < try_count:
		try:
			await client.connect(timeout=timeout)
			if client.is_connected:
				return client
		except Exception as e:
			exception = e
		finally:
			counter += 1

	if exception is not None:
		raise exception
	else:
		raise TimeoutError(f'Fail to connect to {device}')


class DeviceWriter:
	def __init__(
			self,
			client:
			BleakClient,
			strip_nul: bool = True,
			target_characteristics: _Optional[BleakGATTCharacteristic] = None,
			terminator: _Optional[bytes] = None,
	):
		self.client = client
		self.strip_nul = strip_nul
		self.target_characteristics = target_characteristics
		self.terminator = terminator

		self.feedbacks = []
		self.__stop_flag = False

	async def __monitor(self, characteristics: BleakGATTCharacteristic, data: bytearray):
		if self.strip_nul:
			data = data.strip(b'\x00')
		self.feedbacks.append(data)
		if self.terminator is not None and data == self.terminator:
			self.__stop_flag = True

	def clear(self):
		self.terminator = None
		self.feedbacks.clear()
		self.__stop_flag = False

	async def wait(self, timeout: float):
		deadline = _now() + timeout
		while (not self.__stop_flag) and (_now() < deadline) and self.client.is_connected:
			await asyncio.sleep(0.1)

	async def write_and_wait_for_response(self, data_to_write: bytes, timeout: float = float('inf')):
		client = self.client
		monitored_characteristics = []
		target_characteristics = []
		if self.target_characteristics is not None:
			monitored_characteristics.append(self.target_characteristics)
			target_characteristics.append(self.target_characteristics)
		else:
			for service in client.services:
				for characteristics in service.characteristics:
					if 'notify' in characteristics.properties:
						monitored_characteristics.append(characteristics)
					if 'write-without-response' in characteristics.properties:
						target_characteristics.append(characteristics)

		target_count = len(target_characteristics)
		if target_count == 0:
			raise BleakError(f'No writable (without response) characteristics found for client {client}.)')
		elif target_count > 1:
			raise BleakError(f'More than one characteristics are writable (without response), you must specify one.')

		for characteristics in monitored_characteristics:
			await client.start_notify(characteristics, self.__monitor)

		await client.write_gatt_char(target_characteristics[0], data_to_write, False)

		await self.wait(timeout)

		for characteristics in monitored_characteristics:
			if client.is_connected:
				try:
					await client.stop_notify(characteristics)
				except Exception as _e:
					# TODO: 即使之前加了条件，要在“is_connected”的前提下执行，实际中仍有可能在“stop_notify”的时候 disconnected。
					pass
			else:
				break
