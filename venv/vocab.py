class Vocab:
    def __init__(self, word, english):
        self.word = word
        self.english = english

    def getWord(self) -> str:
        return str(self.word)

    def getEnglish(self) -> str:
        return str(self.english)


