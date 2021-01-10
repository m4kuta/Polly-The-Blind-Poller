from Poll import Poll

class PollManager:
    def __init__(self):
        self._polls = {}
        self._pollCount = 1

    def createPoll(self, creator, question, options):
        newPoll = Poll(str(self._pollCount), creator, question, options)
        self._polls[str(self._pollCount)] = newPoll
        self._pollCount += 1 

    def addVote(self, pollId, option, voter):
        if self._polls[pollId].addVote(option, voter):
           return True
        else:
            return False

    def endPoll(self, pollId):
        if pollId in self._polls.keys():
            poll = self._polls[pollId]
            poll.deactivate()
            return poll.getVotes()
        

    
