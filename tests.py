import json
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

class AppTestCase(AioHTTPTestCase):
	async def get_application(self):
		from .app import get_app
		return get_app()

	async def test_json_output_format(self):
		async with self.client.request("GET", "/scan/127.0.0.1/1/10") as resp:
			self.assertEqual(resp.status, 200)
			output = json.loads(await resp.text())
		self.assertIsInstance(output, list)
		self.assertEqual(len(output), 10)
		self.assertIn("port", output[0].keys())
		self.assertIn("state", output[0].keys())
	
	async def test_empty_port_range(self):
		async with self.client.request("GET", "/scan/127.0.0.1/10/9") as resp:
			self.assertEqual(resp.status, 200)
			output = json.loads(await resp.text())
		self.assertEqual(len(output), 0)
	
	async def test_negative_begin_port(self):
		async with self.client.request("GET", "/scan/127.0.0.1/-10/9") as resp:
			self.assertEqual(resp.status, 404)

	async def test_negative_end_port(self):
		async with self.client.request("GET", "/scan/127.0.0.1/10/-9") as resp:
			self.assertEqual(resp.status, 404)
	
	async def test_one_port(self):
		async with self.client.request("GET", "/scan/127.0.0.1/100/100") as resp:
			self.assertEqual(resp.status, 200)
			output = json.loads(await resp.text())
		self.assertEqual(len(output), 1)
		self.assertEqual(output[0]["port"], 100)
	
	async def test_thousand_ports(self):
		async with self.client.request("GET", "/scan/127.0.0.1/4000/4999") as resp:
			self.assertEqual(resp.status, 200)
			output = json.loads(await resp.text())
		self.assertEqual(len(output), 1000)

	async def test_five_thousand_ports(self):
		async with self.client.request("GET", "/scan/127.0.0.1/0/4999") as resp:
			self.assertEqual(resp.status, 200)
			output = json.loads(await resp.text())
		self.assertEqual(len(output), 5000)
	
	async def test_not_number_begin_port(self):
		async with self.client.request("GET", "/scan/127.0.0.1/0x1/10") as resp:
			self.assertEqual(resp.status, 404)

	async def test_not_number_end_port(self):
		async with self.client.request("GET", "/scan/127.0.0.1/0/0x10") as resp:
			self.assertEqual(resp.status, 404)
