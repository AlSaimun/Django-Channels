from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer

class DemoSyncConsumer(SyncConsumer):
    '''SycnConsumer'''

    # This handler is opened when the client sends a connection. 
    def websocket_connect(self, event):
        print('Websocket connected...',event)
        self.send({
            'type':'websocket.accept'
        })

    # this handler recieved data from client
    def websocket_receive(self, event):
        print('Message sent...',event)

        # response from server
        self.send({
            'type':'websocket.send',
            'text':'ki obosta'
        })

    # this handler works when disconnect the connection
    def websocket_disconnect(self, event):
        print('Websocket disconnected...',event)
        raise StopConsumer()

class DemoAsyncConsumer(AsyncConsumer):
    '''SycnConsumer'''
    async def websocket_connect(self, event):
        print('Websocket connected...',event)
        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('Message sent...',event)

    async def websocket_disconnect(self, event):
        print('Websocket disconnected...',event)
        raise StopConsumer()
        