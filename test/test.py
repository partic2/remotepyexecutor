
from asyncio import create_task

from importlib import reload

# start server

from remotepyexecutor import server
from remotepyexecutor import client


reload(server)
reload(client)

async def testMain():
	rpeServ=server.Server()
	await rpeServ.startServe('localhost',8112)
	cli=await client.connect('localhost',8112)
	print(await cli.exec('a=22'))
	print(await cli.eval('a'))
	await cli.close()
	await rpeServ.stopServe()
