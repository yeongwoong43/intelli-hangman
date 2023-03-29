import random
import numpy as np
import pandas as pd

# 클래스로 엮는 중 (미완성)

class ModelDesignError(Exception):
    def __init__(self, msg):
        self.msg = "ModelDesignError: Why try same letter in game again?"
    
    def __str__(self):
        return self.msg

class Master:

    def __init__(self, wordList=None, MAX_LEN=64):
        if wordList == None:
            self.wordList = '''ant bias cat dog elephant fish goat horse international jetcoaster kingmaker
            legal mist niece occupation proporsal quit restriction solve telephone unfortune vector
            worker xylophone you zero'''.split()
        
        else: self.wordList=wordList

        self.MAX_LEN = MAX_LEN
        self.STATE = []
        self.time = 0

    def word_to_df(self, word, test=False): # 단어를 state꼴로 바꾸는 method
        n = len(word)

        df = pd.DataFrame(np.zeros((self.MAX_LEN, 27)))
        df.index = ['hash']+[chr(i) for i in range(97, 123)]
        df['hash'] = [1 for i in range(n)] + [0 for i in range(64-n)]
        if not test:
            for i in range(n):
                df.loc[i, word[i]] = 1
        
        return df
    

    def selectWord(self): # 단어를 랜덤하게 선택
        key = self.wordList[random.randint(1, len(self.wordList))]
        return key


    def stepNext(self, ans): # 답안하고 이전 state를 받아서 다음 state 리턴
        if self.time == 0:
            self.goal = [self.selectWord()]
            self.goal.append(self.word_to_df(self.goal))
            self.STATE.append(self.word_to_df(self.goal, test=True))
        
        else:
            if sum(self.STATE[self.time][ans]!=0) == 0: # 시도한 적 없는 글자라면
                new_state = self.STATE[self.time].copy()
                if ans in self.goal[0]:
                    new_state[ans] = self.goal[1][ans]
                    
            
            else: # 이미 한 번 했던 질문을 반복할 경우
                raise ModelDesignError


        return self.STATE[self.time]

    

    def playGame(self):

        # 답 생성
        self.goal = self.selectWord()
        self.STATE.append(self.word_to_df(self.goal))


        # while loop
        while True:

            # state 전송
            

            # model에서 ans 수신

            # 새 state 계산
