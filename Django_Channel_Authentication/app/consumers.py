from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
import json
from asgiref.sync import async_to_sync # convert method async to sync
from .models import Group, Chat
from channels.db import database_sync_to_async
from channels.db import database_sync_to_async

########################## SyncConsumer ############################
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
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print("Websocket message received.......", event)
        # print("message type", type(event['text']))
        # message = json.loads(event['text'])['msg'] # string to dict
        data = json.loads(event['text'])
        # print("message", message)
        user = self.scope['user']
        if user.is_authenticated:
            group = Group.objects.get(name = self.group_name)
            chat = Chat.objects.create(content=data['msg'], group=group, user = user) # store message in database
            data['username'] = user.username
            async_to_sync(self.channel_layer.group_send)(self.group_name, {  # send message to group
                'type': 'chat.message', # own event, we can write any thing but we need to create handler for this event
                'message': json.dumps(data),
            })
        else:
            async_to_sync(self.channel_layer.group_send)(self.group_name,{  
                'type': 'chat.message',
                'message': json.dumps({'msg': 'Log in required', 'username':'guest'}),
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
 


############################### AsyncConsumer #############################
class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Websocket Connection.......", event)
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        await self.channel_layer.group_add(self.group_name, self.channel_name) 

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print("Websocket message received.......", event)
        # print("message type", type(event['text']))
        message = json.loads(event['text'])['msg'] # string to dict
        # print("message", message)
        '''
        use database_sync_to_async because that function is a sync function 
        '''
        group = await database_sync_to_async(Group.objects.get)(name = self.group_name)
        chat = await database_sync_to_async(Chat.objects.create)(content=message, group=group) # store message in database
        print(group, chat)
        await self.channel_layer.group_send(self.group_name, {  # send message to group
            'type': 'chat.message', # own event, we can write any thing but we need to create handler for this event
            'message': event['text'],
        })

    async def chat_message(self, event): # event: chat.message and handler will be chat_message replace "." by "_"
        '''Here sent message to client from server'''
        print("Event ....", event) 
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

        
    async def websocket_disconnect(self, event):
        print("Websocket disconnected.......", event)
        print("disconnected channel layer.......", self.channel_layer)
        print("disconnected channel name.......", self.channel_name)

        '''
        ## group_discard() -> this method discard a channel from a certain group
        It takes two argument (group_name, channel_name)
        It's a async method in sycConsumer we need to convert this method into sync mehtod    
        '''

        await self.channel_layer.group_discard(self.group_name, self.channel_name) # discard this channel from this group
        raise StopConsumer()
 


'''#################### Another Option ##########################
Another way instead of using this group = database_sync_to_async(Group.objects.get)(name = self.group_name)
group = get_group_name(name)

@database_sync_to_async
def get_group_name(name):
    return Group.objects.get(name=name)

'''
