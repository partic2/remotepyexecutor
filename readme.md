# remotepyexecutor
---

"remotepyexecutor" is a python module to execute python source code on remote host with TCP connection.

**CAUTION** There is no security measure to protecte the server side yet. Use at your own risk.

## How to install

clone this source.
```
cd $REMOTEPYEXECUTOR_SOURCE_ROOT

python setup.py install
```

## How to use

### Server side:

```
from remotepyexecutor import server
import asyncio

rpeServ=server.Server()
asyncio.run(rpeServ.startServe('localhost',8112))

# do something...

#close server
asyncio.run(rpeServ.stopServe())
```

### Client side

```
from remotepyexecutor import client

async def rpe():
	cli=await client.connect('localhost',8112)
	# return 'None' if no Exception, or repr(exception)
	print(await cli.exec('a=22'))
	# return eval result if no Exception, or repr(exception)
	print(await cli.eval('a'))
	await cli.close()

asyncio.run(rpe())
```

View source for more detail.
