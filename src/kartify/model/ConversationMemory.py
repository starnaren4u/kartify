class ConversationMemory:
    def __init__(self):
        self.history = []

    def add(self, msg:dict):
        self.history.append(msg)

    def get(self):
        return self.history

    def clear(self):
        self.history.clear

conversation_memory = ConversationMemory()