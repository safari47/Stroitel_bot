from config.config import broker

@broker.subscriber(channel='broadcast_message')
async def broadcast_message(data):
    pass