import tkinter
import random as r
from GenerallyUsefulFunctions import createGrid2,visualise2DInputGrid,print2DGridAsGrid

WIDTH = 400
HEIGHT = 400
XYGAP = 5
CONSTSTARTGAP = 5
FOURSPAWNCHANCE = 25


class Number():
    def __init__(self,value):
        self.value = value
        self.combined = False

    def combined(self):
        self.combined = True
#TODO:  Remember to revert the state

def initGUI(board):
    top = tkinter.Tk()
    canvas = tkinter.Canvas(top, width=WIDTH, height=HEIGHT)
    score = tkinter.Text(top, height=1, width=20)
    bSouth = tkinter.Button(top, text="Down", command=lambda: squishIntoDirGUIUpdate(board, dir=0,canvas=canvas,score=score))
    bWest = tkinter.Button(top, text="Left", command=lambda: squishIntoDirGUIUpdate(board, dir=1,canvas=canvas,score=score))
    bNorth = tkinter.Button(top, text="Up", command=lambda: squishIntoDirGUIUpdate(board,2,canvas,score))
    bEast = tkinter.Button(top, text="Right", command=lambda: squishIntoDirGUIUpdate(board,3,canvas,score))
    score.insert("1.0", "Score:")
    score.insert("2.0", "0000")
    canvas.grid(row=0, column=0)
    score.grid(row=1, column=0)
    bSouth.grid(row=2, column=0)
    bWest.grid(row=3, column=0)
    bNorth.grid(row=4, column=0)
    bEast.grid(row=5, column=0)
    cellWidth = (WIDTH - 5 * XYGAP) / 4
    updateBoard(canvas,board,cellWidth)
    top.mainloop()

def updateBoard(canvas,board,cellWidth):
    for x in range(4):
        for y in range(4):
            tLeftx = (x * cellWidth) + XYGAP * x + CONSTSTARTGAP
            tLefty = (y * cellWidth) + XYGAP * y + CONSTSTARTGAP
            canvas.create_rectangle(tLeftx, tLefty, tLeftx + cellWidth, tLefty + cellWidth, fill="Blue")
            midx = (tLeftx * 2 + cellWidth) / 2
            midy = (tLefty * 2 + cellWidth) / 2
            currentText = board[y][x]
            if currentText == 0:
                currentText = " "
            canvas.create_text(midx, midy, text=currentText, font=("Arial", int(cellWidth / 2.5)))
    #Maybe no returns?


def squishIntoDirGUIUpdate(board, dir, canvas,score):
    #Data manipulation
    board = squishIntoDir(board,dir)
    board = fillNewNumber(board)
    cellWidth = (WIDTH - 5 * XYGAP) / 4
    if gameOverCheck(board):
        gameOverCanvas(canvas)
    else:
        updateBoard(canvas,board,cellWidth)


def gameOverCanvas(canvas):
    canvas.create_rectangle(0,0,WIDTH,HEIGHT,fill="Red")
    gameOverText = "GAME OVER"
    canvas.create_text(WIDTH//2,HEIGHT//2,text=gameOverText, font=("Arial", int(WIDTH//len(gameOverText))))

#TODO: Implement system which prevents illegal moves

def legalMoves(board):
    pass

#Go in NESW order from 0->3
def squishIntoDir(board, dir):
    digiB = convertToBoard(board)
    for i in range(4):
        for j in range(4):
            if dir==0:
                y = i
                x = j
            elif dir==1:
                y = j
                x = 3-i
            elif dir==2:
                y = 3-i
                x = j
            elif dir==3:
                y = j
                x = i
            else:
                print("Invalid direction for squishing")


            current = board[y][x]

            if y!=3 and dir==0:
                if current==0:
                    board[y][x] = board[y+1][x]
                    board[y+1][x] = 0
                elif board[y+1][x]==current and digiB[y][x].combined==False:
                    board[y][x] *= 2
                    board[y+1][x] = 0
                    digiB[y][x].combined = True
                else:
                    pass

            elif x!=0 and dir==1:

                """Code for left"""
                if current==0:
                    board[y][x] = board[y][x-1]
                    board[y][x - 1] = 0


            elif y!=0 and dir==2:
                """Code for up"""
                if board[y-1][x]==current:
                    board[y-1][x] *= 2
                    board[y][x] = 0
                elif board[y-1][x]==0:
                    board[y-1][x]=current
                    board[y][x] = 0
            if x!=3 and dir==3:
                """code for right"""
                if board[y][x+1]==current:
                    board[y][x+1] *= 2
                    board[y][x] = 0
                elif board[y][x+1]==0:
                    board[y][x+1]=current
                    board[y][x] = 0
    return board



def fillNewNumber(board):
    free = checkFree(board)
    rIndex = r.randint(0,len(free)-1)
    fourOr2 = r.randint(0,100)
    if fourOr2 < FOURSPAWNCHANCE:
        spawn = 4
    else:
        spawn = 2
    board[rIndex//4][rIndex%4] = spawn
    return board


def gameOverCheck(board):
    for i in range(16):
        current = board[i // 4][i % 4]
        if current == 0:
            return False
    for i in range(4):
        for j in range(4):
            if i!=3:
                if board[i+1][j]==board[i][j]:
                    return False
            if j!=3:
                if board[i][j+1]==board[i][j]:
                    return False
    return True



def checkFree(board):
    free = []
    for i in range(16):
        current = board[i // 4][i % 4]
        if current == 0:
            free.append(i)
    return free

def convertToBoard(b):
    board = [Number(b[i//4][i%4]) for i in range(16)]
    return board


def checkValidMove(board):
    pass




if __name__=="__main__":
    gridExample = [[0, 0, 0, 0], [0, 0, 4, 2], [0, 2, 0, 8], [32, 16, 8, 256]]
    errorBoard = [[2, 4, 8, 1], [2, 5, 6, 7], [13, 9, 17, 19], [23, 29, 31, 37]]

    initGUI(gridExample)

    # visualise2DInputGrid(grid,"2D visualiation")

