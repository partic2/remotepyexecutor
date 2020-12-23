

from asyncio import StreamReader
from asyncio import StreamWriter
from asyncio import open_connection

from . import common

from . import encode


class Session():
    def __init__(self,r:StreamReader,w:StreamWriter):
        self.r=r
        self.w=w

    async def eval(self,source:str)->str:
        self.w.write(bytes([common.PackageTypeEval]))
        self.w.write(source.encode(encode))
        self.w.write(b'\0')
        resp=await self.r.readuntil(b'\0')
        resp=resp[0:len(resp)-1]
        return resp.decode(encode)

    async def exec(self,source:str)->str:
        self.w.write(bytes([common.PackageTypeExec]))
        self.w.write(source.encode(encode))
        self.w.write(b'\0')
        resp=await self.r.readuntil(b'\0')
        resp=resp[0:len(resp)-1]
        return resp.decode(encode)

    async def close(self):
        self.w.write(bytes([common.PackageTypeDisconnect]))
        self.w.close()


async def connect(rhost:str,rport:int)->Session:
    r,w=await open_connection(rhost,rport)
    return Session(r,w)
