
import asyncio

from asyncio.streams import StreamReader
from asyncio.streams import StreamWriter
from asyncio import create_task

from typing import TypeVar
from typing import List

from . import common

from . import encode


gCtx={}



class Session():
    def __init__(self,r:StreamReader,w:StreamWriter):
        self.r=r
        self.w=w
        self.sessionCtx={}
        self.sessionCtx['_G']=gCtx
        self.sessionCtx['_session']=self
        self.lCtx={}
        self.running=False
    
    async def readSource(self)->str:
        bsource=await self.r.readuntil(b'\0')
        source=bsource[0:len(bsource)-1].decode(encode)
        return source

    async def writeStrPackage(self,content:str):
        self.w.write(content.encode(encode))
        self.w.write(b'\0')

    async def process(self):
        self.running=True
        while self.running:
            packageType=(await self.r.readexactly(1))[0]
            if packageType==common.PackageTypeEval :
                s=await self.readSource()
                try:
                    r=eval(s,self.sessionCtx,self.lCtx)
                    await self.writeStrPackage(repr(r))
                except Exception as e:
                    await self.writeStrPackage(repr(e))
            elif packageType==common.PackageTypeExec :
                s=await self.readSource()
                try:
                    exec(s,self.sessionCtx,self.lCtx)
                    await self.writeStrPackage(repr(None))
                except Exception as e:
                    await self.writeStrPackage(repr(e))
            elif packageType==common.PackageTypeDisconnect :
                self.running=False
                await self.close()
            else :
                await self.writeStrPackage('None')
        

    async def close(self):
        self.w.close()
        await self.w.wait_closed()
        
        

class Server():

    def __init__(self):
        self.host='localhost'
        self.port=0
        self.server:asyncio.Server=None
        self.running=False
        self.runningSession:List[Session]=[]
        self.stopFuture:asyncio.Future
    
    def sessionAdd(self,r:StreamReader,w:StreamWriter):
        s=Session(r,w)
        s.attachedServer=self
        create_task(s.process())
        self.runningSession.append(s)

    async def startServe(self,host:str,port:int):
        self.host,self.port=host,port
        self.running=True
        def fn(r,w):
            self.sessionAdd(r,w)
        self.server=await asyncio.start_server(fn,self.host,self.port)
        self.stopFuture=asyncio.Future()
        
    async def startServeAndWait(self,host:str,port:int):
        await self.startServe(host,port)
        await self.waitForStop()
    
    async def stopServe(self):
        self.running=False
        for e in self.runningSession:
            await e.close()
        self.server.close()
        self.stopFuture.set_result(True)
    
    async def waitForStop(self):
        if self.running:
            await self.stopFuture
        


