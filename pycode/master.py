import random
import numpy as np
import pandas as pd

class Master:

    def __init__(self, wordList=None, MAX_LEN=64):
        if wordList == None:
            self.wordList = '''ant bias cat dog elephant fish goat horse international jetcoaster kingmaker
            legal mist niece occupation proporsal quit restriction solve telephone unfortune vector
            worker xylophone you zero'''.split()
        
        else: self.wordList=wordList

        self.MAX_LEN = MAX_LEN
        self.time = -1

    def word_to_df(self, word, test=False): # 단어를 state꼴로 바꾸는 method
        n = len(word)

        df = pd.DataFrame(np.zeros((self.MAX_LEN, 27)))
        df.columns = ['hash']+[chr(i) for i in range(97, 123)]
        df['hash'] = [1 for i in range(n)] + [0 for i in range(64-n)]
        if not test:
            for i in range(n):
                df.loc[i, word[i]] = 1
        
        return df
    

    def selectWord(self): # 단어를 랜덤하게 선택
        key = self.wordList[random.randint(1, len(self.wordList))]
        return key


    def stepNext(self, ans): # 답안하고 이전 state를 받아서 다음 state 리턴
        if self.time == -1: raise Exception("Why don't you call the method initGame() first?")
        
        elif (self.STATE[self.time] == self.goal[1]).all().all():
            return (-1, self.time) # 다 풀면 원래의 time란에 -1 대입하도록 했음

        else:
            if sum(self.STATE[self.time][ans]!=0) == 0: # 시도한 적 없는 글자라면
                new_state = self.STATE[self.time].copy()
                if ans in self.goal[0]:
                    new_state[ans] = self.goal[1][ans]
                    # 공사중
                    # def markClue(row):
                    #     if row[ans] == 1:
                    #         for char in [chr(i) for i in range(ord('a'), ord('z')+1)].remove(ans):
                    #             row[char] = -1
                    #     return row
                    new_state = new_state.apply(markClue)
                        
                
                else:
                    # 공사중
                    # def markClue(row):
                    #     if row['hash'] == 1:
                    #         row[ans] = -1
                    #     return row
                    new_state = new_state.apply(markClue)
                
                self.STATE.append(new_state)
                self.time += 1
                    
            
            else: # 이미 한 번 했던 질문을 반복할 경우
                raise Exception("ModelDesignError: Why try same letter again?")


        return (self.time, self.STATE[self.time])

    

    def initGame(self):

        # 답 생성
        goal = self.selectWord()
        self.goal = [goal, self.word_to_df(goal)]
        self.STATE = [self.word_to_df(goal, test=True)]
        self.time = 0