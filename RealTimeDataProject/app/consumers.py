from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import string, random
import json


def generate_number(otp_size=6): 
        ''' generates 6 digits otp for password reset '''
        digits = string.digits 
        otp = ''.join([random.choice(digits) for _ in range(otp_size)])
        return otp 



class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('Connected',event)
        self.send({
            'type': 'websocket.accept',
        })

    def websocket_receive(self, event):
        print('Message sent...',event)

        for i in range(50): # send response 
            self.send({
                'type':'websocket.send',
                # 'text': generate_number() # send string data
                # when need to send dictionary type data and dumps method convert dict into string / json
                'text': json.dumps({'otp':generate_number()})
            })
            sleep(1)

    def websocket_disconnect(self, event):
        print('Websocket disconnected...',event)
        raise StopConsumer()
    
class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('Connected',event)
        await self.send({
            'type': 'websocket.accept',
        })

    async def websocket_receive(self, event):
        print('Message sent...',event)

        for i in range(10): 
            await self.send({
                'type':'websocket.send',
                'text': str(i)
            })
            await asyncio.sleep(1)

    async def websocket_disconnect(self, event):
        print('Websocket disconnected...',event)
        raise StopConsumer()