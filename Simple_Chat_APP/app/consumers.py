from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer

from asgiref.sync import async_to_sync # convert method async to sync

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket Connection.......", event)
        print('Channel layer: ', self.channel_layer) # default channel layer
        print('Channel Name: ', self.channel_name) # default channel name
        # print('group-name: ', self.scope['url_route']['kwargs']['group_name'])
        print()
        ''' 
        ## group_add() -> this method add a channel to a certain group
        It takes two argument (group_name, channel_name)
        This method add this channel into the group
        It's a async method in sycConsumer we need to convert this method into sync mehtod
        '''
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name) # add a static group named 'beckar_somiti'

        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print("Websocket message received.......", event)
        async_to_sync(self.channel_layer.group_send)(self.group_name, {  # send message to group
            'type': 'chat.message', # own event, we can write any thing but we need to create handler for this event
            'message': event['text'],
        })

    def chat_message(self, event): # event: chat.message and handler will be chat_message replace "." by "_"
        '''Here sent message to client from server'''
        print("Event ....", event) 
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

        
    def websocket_disconnect(self, event):
        print("Websocket disconnected.......", event)
        print("disconnected channel layer.......", self.channel_layer)
        print("disconnected channel name.......", self.channel_name)

        '''
        ## group_discard() -> this method discard a channel from a certain group
        It takes two argument (group_name, channel_name)
        It's a async method in sycConsumer we need to convert this method into sync mehtod    
        '''

        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name) # discard this channel from this group
        raise StopConsumer()
 