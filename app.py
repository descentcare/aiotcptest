import asyncio
from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/scan/{ip}/{begin_port:\d+}/{end_port:\d+}')
async def scan_route(request):
	target = request.match_info['ip']
	begin_port = int(request.match_info['begin_port'])
	end_port = int(request.match_info['end_port'])
	result = await asyncio.gather(*(
		asyncio.ensure_future(scan(target, port)) 
				for port in range(begin_port, end_port+1)
				))
	return web.json_response(result)

async def scan(ip, port, timeout = 5):
	state = 'open'
	try:
		await asyncio.wait_for(asyncio.open_connection(ip, port), 
				timeout = timeout)
	except (ConnectionRefusedError, asyncio.TimeoutError, OSError):
		state = 'closed'
	return {'port': port, 'state': state}

def get_app():
	app = web.Application()
	app.add_routes(routes)
	return app


if __name__ == "__main__":
	web.run_app(get_app())
