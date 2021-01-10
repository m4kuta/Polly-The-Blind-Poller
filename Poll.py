class Poll:
    def __init__(self, creator, question, options):
        self._id = id
        self._creator = creator
        self._question = question
        self._votes = {}

    def get_id(self):
        return self._id

    def get_creator(self):
        return self._creator

    def get_question(self):
        return self._question

    def get_votes(self):
        return self._votes

