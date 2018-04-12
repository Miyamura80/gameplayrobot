import numpy as np
from random import randint, uniform
from GenerallyUsefulFunctions import findFirstElementIndex

ACTIONNUM = 9
GAMMA = 0.8

def compare1DListElement(l1,l2):
    if len(l1)!=len(l2):
        print("Different length list, invalid")
        return False
    for i in range(len(l1)):
        if l1[i]!=l2[i]:
            return False
    return True

#Sorta inefficient but oh well
#Returns the state index and rotation index
def checkRotations(board,states):
    #0: Up, 1: Right, 2: Down, 3: Left
    rotations = [board]
    rRight = board[0::3][::-1] + board[1::3][::-1] + board[2::3][::-1]
    rotations.append(rRight)
    rotations.append(board[::-1])
    rotations.append(rRight[::-1])
    for i in range(len(states)):
        for j in range(4):
            if compare1DListElement(states[i],rotations[j]):
                return i, j
    return -1,-1

def rotateBoard(board,rotation):
    if rotation==0:
        return board
    elif rotation==1:
        return (board[0::3][::-1] + board[1::3][::-1] + board[2::3][::-1])
    elif rotation==2:
        return board[::-1]
    elif rotation==3:
        return (board[0::3][::-1] + board[1::3][::-1] + board[2::3][::-1])[::-1]
    else:
        print("Invalid rotation index")


#Returns -1 if loss, 1, if win, 0 if no win/loss, 2 if draw
def checkWin(b):
    won = 0
    players = [8,7]
    for i in players:
        #Cheecking horizontal wins
        if b[0]==b[1]==b[2]==i or b[3] == b[4] == b[5] == i or b[6] == b[7] == b[8] == i:
            won = i
            break
        #Checking vertical wins
        if b[0] == b[3] == b[6] == i or b[1] == b[4] == b[7] == i or b[2] == b[5] == b[8] == i:
            won = i
            break
        if b[0] == b[4] == b[8] == i or b[2]==b[4]==b[6]==i:
            won = i
            break
    if won == 8:
        return 1
    elif won==7:
        return -1
    else:
        return 0

def getHighestQPerGivenState(Q,board, stateIndex):
    validStates = possibleNextStates(board)
    highestQ = 0
    for i in validStates:
        if Q[stateIndex][i] > highestQ:
            highestQ = Q[stateIndex][i]
    return highestQ

#Choose the Q with highest value, unless all equal
def ChooseHighestQ(Q,board,states):
    validStates = possibleNextStates(board)
    highestQ = 0
    #THIS BIT MUST DEAL WITH ALL POSSIBLE NEXT MOVES
    #THIS BIT SHOULD ALSO DEAL WITH ALL RANDOM ELEMENTS OF GAME
    for i in validStates:
        newBoard = list(board)
        newBoard[i] = 7
        index, rotation = checkRotations(board,states)

        if getHighestQPerGivenState(Q,newBoard,index) > highestQ:
            highestQ = getHighestQPerGivenState(Q,newBoard,index)
    return highestQ




def possibleNextStates(board):
    nexts = []
    for i in range(len(board)):
        if board[i]==1:
            nexts.append(i)
    return nexts

def adversarialBot(currentQ,stateIndex,board):
    board = flipBoard(board)
    board = optimalActionOnBoard(currentQ,stateIndex,board)
    board = flipBoard(board)
    return board


def rewardFunc(board):
    if checkWin(board)==1:
        return 100
    elif checkWin(board)==-1:
        return -100
    elif checkFilled(board):
        return 50
    else:
        return 0

def checkFilled(board):
    for i in board:
        if i==1:
            return False
    return True

def adversarialBotTurn(reward,Q,index,board):
    board = adversarialBot(Q, index, board)
    printBoard(board)
    reward += rewardFunc(board)
    # TODO: add function which logs the bad end here
    return board,reward

def studentBotTurn(board,Q,states,randomPerc):

    if uniform(0,1) < randomPerc:
        nexts = possibleNextStates(board)
        # Choosing the next possible action randomly
        if len(nexts) != 0:
            action = nexts[randint(0, len(nexts) - 1)]
        else:
            print("Error: no more available moves left")
        board[action] = 8
    else:
        index,rotation = checkRotations(board,states)
        board = flipBoard(board)
        board = adversarialBot(Q,index,board)
        #TODO: Fix it so it returns action

    # Identifying the index and rotation, if unrecognised added to states
    # Otherwise rotate board according to state & rotation
    index, rotation = checkRotations(board, states)
    if index == -1:
        states = appendListTo(states, board)
        index = len(states) - 1
        f = np.zeros((1, 9))
        Q = np.vstack([Q, f])
    else:
        board = rotateBoard(board, rotation)
    printBoard(board)

    return board, Q, states,index, action

def trainBotFromScratch(num,Q= np.zeros((1,ACTIONNUM)),states=0):
    board = [1,1,1,1,1,1,1,1,1]
    if states==0:
        states = [board]
    for i in range(num):
        gameFinish = False
        board = [1,1,1,1,1,1,1,1,1]
        # randomStart = randint(0,1)
        randomStart = 0
        if randomStart==1:
            index = 0
        #Everyone gets 10 points at beggining
        reward = 0
        moveCount = 0
        if i==999:
            print("hay")

        while not gameFinish:
            if randomStart==0:
                randProb = (num-i)/num
                board, Q, states,index,action = studentBotTurn(board,Q,states,randProb)

                # Bellman equation line
                reward += rewardFunc(board)
                value = reward + GAMMA * ChooseHighestQ(Q,board,states)
                Q[index][action] =  value
                if abs(reward)>40:
                    Q[index][action] = value - moveCount
                    break
                else:
                    moveCount += 1
                """
                BOT TURN
                """
                board, reward = adversarialBotTurn(reward,Q,index,board)

                if abs(reward)>40:
                    value = reward
                    Q[index][action] = value
                    gameFinish = True
                    break
            else:
                """
                BOT TURN
                """
                reward += rewardFunc(board)

        print("----------------------------------")
    return Q, states

def appendListTo(states,lst):
    k = [i for i in lst]
    states.append(k)
    return states

#Goes for a random action when optimal is unknown
def optimalActionOnBoard(Q,stateIndex,board):
    validStates = possibleNextStates(board)

    highestQ = -999
    bestActions = []
    QRow = Q[stateIndex]
    for i in range(len(validStates)):
        if Q[stateIndex][validStates[i]] >= highestQ:
            highestQ = Q[stateIndex][validStates[i]]
    for i in range(len(validStates)):
        if Q[stateIndex][validStates[i]]==highestQ:
            bestActions.append(validStates[i])

    # if len(bestActions)==0:
    #     #DUE TO CHANGE
    #     if len(validStates)==1:
    #         bestAction = validStates[0]
    #     else:
    #         bestAction = validStates[randint(0,len(validStates)-1)]


    if len(validStates)==1:
        bestAction = bestActions[0]
    else:
        if len(bestActions) == 0:
            print(Q[stateIndex])
            print(bestActions)
            print(stateIndex)
            print(board)
        print("Valid states:",validStates)
        print("bestActions:", str(bestActions))
        print("Q Row:",QRow)
        print("StateIndex:",stateIndex)
        bestAction = bestActions[randint(0,len(bestActions)-1)]

    board[bestAction] = 8
    return board

def flipBoard(board):
    for i in range(len(board)):
        k = board[i]
        if k==8:
            board[i] = 7
        elif k==7:
            board[i] = 8
    return board

def printBoard(board):
    str1 = ""
    for i in range(9):
        k = board[i]
        if k==7:
            str1 += "X"
        elif k==8:
            str1 += "O"
        else:
            str1 += "-"
        if i%3==2:
            str1 += "\n"
    print(str1)

def saveQ(Q,states):
    f = open("naughtsCrossQ.txt","w")
    qShape = Q.shape
    count = 0
    for i in range(qShape[0]):
        f.write(str(states[count]))
        f.write(":")
        for j in range(qShape[1]):
            f.write(str(Q[i][j]))
            if j!=qShape[1]-1:
                f.write(",")
        count += 1
        if i!=qShape[0]-1:
            f.write("\n")


    f.close()

def convertStrLToIntL(lst):
    k = []
    for i in lst:
        k.append(int(i))
    return k

def loadQAndStates(name):
    f = open(name,"r")
    rl = f.readlines()
    states = []
    height = len(rl)
    width = len(rl[0].split(":")[1].split(","))
    Q = np.empty((height,width),float)
    for i in range(height):
        row = rl[i].split(":")[1].split(",")
        for j in range(width):
            Q[i][j] = float(row[j])
        k = convertStrLToIntL(rl[i].split(":")[0].strip("[").strip("]").split(","))
        states.append(k)
    f.close()
    return Q, states

if __name__=="__main__":
    Q,states = loadQAndStates("naughtsCrossQ.txt")

    Q,states = trainBotFromScratch(10000,Q,states)
    move = ""
    print("-1 to quit")
    b = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    while move!=-1:
        if rewardFunc(b)!=0:
           b = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        move = int(input("enter move"))
        b[move] = 8
        index, rotation = checkRotations(b, states)
        b = rotateBoard(b,rotation)
        printBoard(b)
        if rewardFunc(b)!=0:
           b = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        b = adversarialBot(Q,index,b)
        printBoard(b)
    saveQ(Q,states)
    print("Saved successfully")




"""
Questions:
-Why does Q have values for illegal moves?
-
"""

