class Vocab:
    def __init__(self, word, english, meaning):
        self.word = word
        self.english = english
        self.meaning = meaning

    def getWord(self) -> str:
        return str(self.word)

    def getEnglish(self) -> str:
        return str(self.english)

    def getMeaning(self):
        return str(self.english)
