import random
import numpy as np
import pandas as pd

MAX_LEN = 64

class State:
    def __init__(self):
        self.time = 0
        self.footprint = [[]]
        self.clue = [{}]

class Instructor:

    def __init__(self, model, wordList=None, MAX_LEN = MAX_LEN):
        if wordList==None:
            self.setWordListDefault()
        else:
            self.setWordList(wordList)
        
        self.setModel(model)
        
        self.initGame()
    
    def setWordListDefault(self):
        self.wordList = "ant bias cat dog elephant fish goat horse international jetcoaster kingmaker \
                legal mist niece occupation proporsal quit restriction solve telephone unfortune vector \
                    worker xylophone you zero".split()
    
    def setWordList(self, wordList):
        self.wordList = wordList
    
    def setModel(self, model):
        self.model = model
    
    def initGame(self):
        self.initState()

        self.setKeyWord()
    
    def initState(self):
        self.State = State()
    
    def setKeyWord(self):
        self.keyWord = random.choice(self.wordList)
    


    def getState(self):
        time = self.State.time
        return self.getStateAt(time)
    
    def getStateAt(self, time):
        return (self.State.footprint[time], self.State.clue[time])

    
    
    def stepNext(self, ans):
        self.updateState(ans)

        if self.isEnded():
            self.closeGame()
                
    def isEnded(self):
        for char in self.keyWord:
            if char not in self.getState()[0]:
                return False
        return True
    
    def closeGame(self):
        print("Game Ended")
        pass

    def updateState(self, ans):
        self.State.time += 1
        if ans in self.State.footprint[self.State.time-1]:
            raise Exception("ModelDesignError: Why are you trying same letter again?")
        else:
            self.updateFootprint(ans)
            self.updateClue(ans)
        
        return self.getStateAt(self.State.time)
    
    def updateFootprint(self, ans):
        footprintPresent = self.getStateAt(self.State.time-1)[0].copy()
        footprintPresent.append(ans)
        self.State.footprint.append(footprintPresent)
    
    def updateClue(self, ans):
        cluePresent = self.getStateAt(self.State.time-1)[1].copy()
        cluePresent[ans] = self.getClue(ans)
        self.State.clue.append(cluePresent)
    
    def getClue(self, ans):
        if ans in list(self.keyWord):
            return 1
        else:
            return 0