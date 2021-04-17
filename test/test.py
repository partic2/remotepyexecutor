
import asyncio
from asyncio import create_task
import sys

from importlib import reload

# start server

from remotepyexecutor import server
from remotepyexecutor import client


async def testMain():
    print('testMain')
    rpeServ=server.Server()
    print('start server')
    await rpeServ.startServe('localhost',8112)
    print('start client')
    cli=await client.connect('localhost',8112)
    print('execute code a=22')
    print(await cli.exec('a=22'))
    print('get value of a,(should be 22)')
    print(await cli.eval('a'))
    print('close client')
    await cli.close()
    await asyncio.sleep(1)
    print('close server')
    await rpeServ.stopServe()

asyncio.run(testMain())