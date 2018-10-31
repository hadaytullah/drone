
class MessageDispatcher:

    def __init__(self):
        self._agents = []
        self.message_uid = 1
    def broadcast(self, message):
        message.uid = self.message_uid
        #print('-- {} Broad casting for agent# {}'.format(message.uid, message.sender.uid))
        self.message_uid += 1

        for agent in self._agents:
            if agent is not message.sender:
                agent.receive(message)

    def register(self, agent):
        self._agents.append(agent)

    def unregister(self, agent):
        self._agents.remove(agent)


class Message:
    def __init__(self, sender, points, points_info):# position_of, x, y):
        self.sender = sender
        self.uid = 0
        #self.position_of = position_of
        #self.x = x
        #self.y = y

        self.points = points
        self.points_info = points_info




