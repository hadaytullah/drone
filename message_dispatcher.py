

class MessageDispatcher:

    def __init__(self):
        self._agents = []
        self.message_uid = 1
    def broadcast(self, message):
        message.uid = self.message_uid
        print('-- {} Broad casting for agent# {}'.format(message.uid, message.sender.uid))
        self.message_uid += 1

        for agent in self._agents:
            if agent is not message.sender:
                agent.receive(message)

    def register(self, agent):
        self._agents.append(agent)

    def unregister(self, agent):
        self._agents.remove(agent)

