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

### Server side (in coroutine):

```
from remotepyexecutor import server
import asyncio

rpeServ=server.Server()
await rpeServ.startServe('localhost',8112))

# do something...

#close server
await rpeServ.stopServe()
```

### Server side (blocked until server stopped):

```
from remotepyexecutor import server
import asyncio

serv=remotepyexecutor.server.Server()
asyncio.run(serv.startServeAndWait('0.0.0.0','8105'))
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



There are some special variable defined in execution environment:
 "_G" to storage global variable cross session. 
 "_session" to access Session on server 
 
View source for more detail.
