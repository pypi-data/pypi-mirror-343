import nats

class MessagingUtil:
    def __init__(self, hostAddress:str):
        self.hostAddress = hostAddress

    async def getClient(self):
        """
        Initialize and return a messaging client instance.
        Replace with actual client initialization logic.
        """
        nc = await nats.connect(self.hostAddress)
        return nc

    async def publish(self, topic, message):
        """
        Publish a message to a specific topic.
        :param topic: The topic to publish to.
        :param message: The message to send.
        """
        nc = await self.getClient()
        await nc.publish(topic, message.encode())
        await nc.close()  # Close connection after publishing

    