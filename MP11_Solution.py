import turtle
import random
import time
import P1
import P2
import copy

SLOW_DOWN=False
GRAPHICS=True
STEP=True
enforceTime = True

def drawSquare(t,color):
    t.color("black")
    t.fillcolor(color)
    t.begin_fill()
    for num in range(4):
        t.forward(1)
        t.right(90)
    t.end_fill()

def drawRow(t,color1,color2):
    for i in range(4):
        drawSquare(t,color1)
        t.forward(1)
        drawSquare(t,color2)
        t.forward(1)

def drawChecker(t,row,col,color,kingFlag):
    y=row-1
    x=col+.5
    t.color("dimgray",color)
    t.up()
    t.goto(x,y)
    t.down()
    t.begin_fill()
    t.circle(.5)
    t.end_fill()
    #draw the concentric circles in the checker
    for i in range(1,5):
        t.up()
        t.goto(x,y+(i*.1))
        t.down()
        if i==4 and kingFlag:
            t.begin_fill()
            t.color("yellow")
        t.circle(.5-(i*.1))
        if i==4 and kingFlag:
            t.end_fill()
            t.color("dimgray")

def drawBoard(bob):
    c1="gray"
    c2="red"
    for x in range(8):
        drawRow(bob,c1,c2)
        bob.up()
        bob.goto(0,x+1)
        bob.down()
        #switch c1 and c2 colors
        temp=c1
        c1=c2
        c2=temp
    drawLabels(bob)

def drawLabels(t):
    offset=0
    t.color("white")
    for line in "ABCDEFGH":
        for cell in range(0,8,2):
            t.up()
            t.goto(offset+cell+.82,ord(line)-65+.02)
            t.down()
            t.write(line+str(cell+offset))
        if offset==0:
            offset=1
        else:
            offset=0
    t.color("black")

def drawLabel(t,row,col):
    t.color("white")
    t.up()
    t.goto(col+.82,row+.02)
    t.down()
    t.write(chr(row+65)+str(col))
    t.color("black")

def printBoard(board):
    for row in range(8):
        for col in range(8):
            print("",board[row][col],end="")
        print()
    print()

def populateBoardsWithCheckers(t,board):
    offset=0
    if GRAPHICS:t.color("red")
    for row in range(0,3):
        for col  in range(0,8,2):
            if GRAPHICS:drawChecker(t,row,col+offset,"red",False)
            board[row][col+offset]="r"
        if offset==0:
            offset=1
        else:
            offset=0
    offset=1
    if GRAPHICS:t.color("black")
    for row in range(5,8):
        for col in range(0,8,2):
            if GRAPHICS:drawChecker(t,row,col+offset,"black",False)
            board[row][col+offset]="b"
        if offset==1:
            offset=0
        else:
            offset=1

def listValidMoves(board,player):
    possibleMoves=[]
    validRange=[0,1,2,3,4,5,6,7] #list(range(8))
    if player=="b":
        playerTokens=["b","B"]
        moveRowInc=-1
    else:
        playerTokens=["r","R"]
        moveRowInc=1
    kingTokens=["B","R"]
    for row in range(8): #For every row
        for col in range(8):  #For every square in a row
            if board[row][col] in playerTokens: #If the board contains either a regular or king checker of the given player
                if board[row][col] not in kingTokens: #if checker is NOT a king
                    for colInc in [-1,1]: #for each diagonal square in the correct row direction
                        if row+moveRowInc in validRange and col+colInc in validRange and board[row+moveRowInc][col+colInc] =='e':
                            possibleMoves.append(chr(row+65)+str(col)+":"+chr(row+65+moveRowInc)+str(col+colInc))
                else:  #checker is a king
                    for rowInc in [-1,1]: #for each row direction (forward and backward)
                        for colInc in [-1,1]: #for each diagonal square in each row direction
                            if row+rowInc in validRange and col+colInc in validRange and board[row+rowInc][col+colInc] =='e':
                                possibleMoves.append(chr(row+65)+str(col)+":"+chr(row+65+rowInc)+str(col+colInc))              
    return possibleMoves

def listSingleJumps(board,player):
    possibleSingleJumps=[]
    validRange=[0,1,2,3,4,5,6,7] #list(range(8))
    if player=="b":
        playerTokens=["b","B"]
        rowInc=-1
        enemyTokens=["r","R"]
    else:
        playerTokens=["r","R"]
        rowInc=1
        enemyTokens=["b","B"]
    kingTokens=["B","R"]
    for row in range(8):
        for col in range(8):
            if board[row][col] in playerTokens:
                if board[row][col] not in kingTokens:  #if checker is NOT a king
                    for colInc in [-1,1]:
                        if row+rowInc in validRange and col+colInc in validRange and board[row+rowInc][col+colInc] in enemyTokens:                        
                            colJumpInc=2 * colInc
                            rowJumpInc=2 * rowInc
                            if row+rowJumpInc in validRange and col + colJumpInc in validRange and board[row+rowJumpInc][col+colJumpInc]=="e":
                                possibleSingleJumps.append(chr(row+65)+str(col)+":"+chr(row+65+rowJumpInc)+str(col+colJumpInc))
                else: #checker is a king
                    for rowIncs in [-1,1]: #for each row direction (forward and backward)
                        for colInc in [-1,1]:
                            if row+rowIncs in validRange and col+colInc in validRange and board[row+rowIncs][col+colInc] in enemyTokens:                        
                                colJumpInc=2 * colInc
                                rowJumpInc=2 * rowIncs
                                if row+rowJumpInc in validRange and col + colJumpInc in validRange and board[row+rowJumpInc][col+colJumpInc]=="e":
                                    possibleSingleJumps.append(chr(row+65)+str(col)+":"+chr(row+65+rowJumpInc)+str(col+colJumpInc))
    return possibleSingleJumps

def listMultipleJumps(board,player,jumpsList):
    newJumps=expandJumps(board,player,jumpsList)
    while newJumps != jumpsList:
        jumpsList=newJumps[:]
        newJumps=expandJumps(board,player,jumpsList)
    return newJumps


def expandJumps(board,player,oldJumps):
    INCs=[1,-1]
    VALID_RANGE=[0,1,2,3,4,5,6,7]
    if player=="b":
        playerTokens=["b","B"]
        rowInc=-1
        opponentTokens=["r","R"]
    else:
        playerTokens=["r","R"]
        rowInc=1
        opponentTokens=["b","B"]
    newJumps=[]
    for oldJump in oldJumps:
        row=ord(oldJump[-2])-65
        col=int(oldJump[-1])
        newJumps.append(oldJump)
        startRow=ord(oldJump[0])-65
        startCol=int(oldJump[1])
        if board[startRow][startCol] not in ["R","B"]: #not a king
            for colInc in INCs:
                jumprow=row+rowInc
                jumpcol=col+colInc
                torow=row+2*rowInc
                tocol=col+2*colInc
                if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                and board[jumprow][jumpcol] in opponentTokens and board[torow][tocol]=='e':
                    newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                    if oldJump in newJumps:
                        newJumps.remove(oldJump)
        else: #is a king
            for colInc in INCs:
                for newRowInc in INCs:
                    jumprow=row+newRowInc
                    jumpcol=col+colInc
                    torow=row+2*newRowInc
                    tocol=col+2*colInc
                    if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                    and board[jumprow][jumpcol] in opponentTokens and (board[torow][tocol]=='e' or oldJump[0:2]==chr(torow+65)+str(tocol)) \
                    and ((oldJump[-2:]+":"+chr(torow+65)+str(tocol)) not in oldJump) and ((chr(torow+65)+str(tocol)+':'+oldJump[-2:] not in oldJump)) and (chr(torow+65)+str(tocol)!=oldJump[-5:-3]):
                        newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                        if oldJump in newJumps:
                            newJumps.remove(oldJump)
    return newJumps          
               
def swapPlayer(player):
    if player=="b":
        player="r"
        playerColor="red"
    else:
        player="b"
        playerColor="black"
    return player,playerColor

def setupGame(inFileName):
    #Set up graphics for game
    if GRAPHICS:
        wn=turtle.Screen()
        wn.setworldcoordinates(-2,9,10,-2)
        bob=turtle.Turtle()
        bob.hideturtle()
        wn.tracer(False)
        drawBoard(bob)
    #Set up logical and graphical checkers
    row=["e","e","e","e","e","e","e","e"]
    board=[]
    for i in range(8):
        board.append(row[:])
    if inFileName == "":
        if GRAPHICS:
            populateBoardsWithCheckers(bob,board)
        else:
            populateBoardsWithCheckers(None,board)
        if random.randint(0,1)==1:
            player="b"
        else:
            player="r"
    else:
        inFile=open(inFileName,'r')
        for rowIndex in range(8):
            line=inFile.readline()[:-1]
            for colIndex in range(8):
                if line[colIndex] in ["r","b","R","B"]:
                    board[rowIndex][colIndex]=line[colIndex]
                    if line[colIndex] in ["r","R"]:
                        if GRAPHICS:drawChecker(bob,rowIndex,colIndex,"red",line[colIndex]=="R")
                    else: #black checker
                        if GRAPHICS:drawChecker(bob,rowIndex,colIndex,"black",line[colIndex]=="B")
        player=inFile.readline()[0]
        inFile.close()
    #printBoard(board)
    if GRAPHICS:
        wn.tracer(True)
        return wn,bob,board,player
    else:
        return None,None,board,player
    
def parseMove(move):
    FROM=move[0:2]
    FROMRow=ord(FROM[0])-65
    FROMCol=int(FROM[1])  #problemChild
    TO=move[3:5]
    TORow=ord(TO[0])-65
    TOCol=int(TO[1])
    return FROMRow,FROMCol,TORow,TOCol

def removeCheckerGraphicalAndLogical(bob,FROMCol,FROMRow,board):
    if GRAPHICS:
        bob.up()
        bob.goto(FROMCol,FROMRow)
        bob.down()
        drawSquare(bob,"gray") #empty the graphical square
        drawLabel(bob,FROMRow,FROMCol) #relabel the emptied square
    playerBoardToken=board[FROMRow][FROMCol] #copy the player token from the logical board, could be "b" or "B" or "r" or "R"
    board[FROMRow][FROMCol]='e' #set the logical board location to empty
    return playerBoardToken

def placeCheckerGraphicalAndLogical(bob,TOCol,TORow,board,playerToken):
    #Logical board update first
    if playerToken == "r" and TORow==7:  #if a kinging move for red
        board[TORow][TOCol]=playerToken.upper()
    elif playerToken == "b" and TORow==0: #if a kinging move for black
        board[TORow][TOCol]=playerToken.upper()
    else: #all non-kinging moves place checker in logical board
        board[TORow][TOCol]=playerToken
    #Now graphical board update
    if GRAPHICS:
        if board[TORow][TOCol] =="b":
            drawChecker(bob,TORow,TOCol,"black",False)
        elif board[TORow][TOCol] =="B":
            drawChecker(bob,TORow,TOCol,"black",True) #True is King
        elif board[TORow][TOCol] =="r":
            drawChecker(bob,TORow,TOCol,"red",False)
        elif board[TORow][TOCol] =="R": #could have used else, but elif for reading clarity
            drawChecker(bob,TORow,TOCol,"red",True) #True is King

def win(board):
    rmove=listValidMoves(board,"r")
    rjump=listSingleJumps(board,"r")
    rjump=listMultipleJumps(board,"r",rjump)
    bmove=listValidMoves(board,"b")
    bjump=listSingleJumps(board,"b")
    bjump=listMultipleJumps(board,"b",bjump)
    if len(rmove)==0 and len(rjump)==0:
        return [True,"black"]
    if len(bmove)==0 and len(bjump)==0:
        return [True,"red"]
    return [False,""]

def saveGame(fileName,board,player):
    outFile=open(fileName,'w')
    outLine=""
    for row in board:
        for ch in row:
            outLine+=ch
        outFile.write(outLine+"\n")
        outLine=""
    outFile.write(player)
    outFile.close()
    print("Game file saved to",fileName)         

def checkersMain(inFileName,redWinCount,blackWinCount):
    wn,bob,board,player=setupGame(inFileName)
    gameOver=False
    if player=="b":
        move = P1.getValidMove(copy.deepcopy(board),player) #get the first move
    else:
        move = P2.getValidMove(copy.deepcopy(board),player) #get the first move
    print(move)
    while move.lower() != "quit" and not gameOver:   #Start alternate play
        if player=="b":
            playerColor="black"
        else:
            playerColor="red"
        if GRAPHICS:wn.tracer(False)
        if STEP:input("Press return to watch the selected move for "+playerColor+" ")
        FROMRow,FROMCol,TORow,TOCol=parseMove(move) #parse move into locations
        if abs(FROMRow-TORow)==1: #move, not a jump
            if SLOW_DOWN: time.sleep(1)
            playerToken=board[FROMRow][FROMCol] #save the player form current location (regular checker or king)
            removeCheckerGraphicalAndLogical(bob,FROMCol,FROMRow,board) #remove the checker to be moved
            if SLOW_DOWN: time.sleep(.5)
            placeCheckerGraphicalAndLogical(bob,TOCol,TORow,board,playerToken) #place the moved checker in its new location
        else: #jump, not a move
            reps=move.count(":")
            for i in range(reps):
                FROMRow,FROMCol,TORow,TOCol=parseMove(move)
                playerToken=board[FROMRow][FROMCol] #save the player form current location (regular checker or king)
                if GRAPHICS:wn.tracer(False)
                if SLOW_DOWN:
                    time.sleep(1)
                removeCheckerGraphicalAndLogical(bob,FROMCol,FROMRow,board) #remove the checker to be moved
                if SLOW_DOWN:
                    time.sleep(.5)
                placeCheckerGraphicalAndLogical(bob,TOCol,TORow,board,playerToken) #place the jumping checker in its new location
                if SLOW_DOWN:
                    wn.tracer(True)
                    time.sleep(1)
                    wn.tracer(False)
                removeCheckerGraphicalAndLogical(bob,(FROMCol+TOCol)//2,(FROMRow+TORow)//2,board) #remove the jumped checker
                if SLOW_DOWN:
                    time.sleep(.5)
                if GRAPHICS:wn.tracer(True)
                move=move[3:]
        if GRAPHICS:wn.tracer(True)
        #printBoard(board)
        player,playerColor=swapPlayer(player)
        gameOver,winningPlayer=win(board)
        if not gameOver:
            if player=="b":
                start=time.time()
                move = P1.getValidMove(copy.deepcopy(board),player) #get the first move
                stop=time.time()
            else:
                start=time.time()
                move = P2.getValidMove(copy.deepcopy(board),player) #get the first move
                stop=time.time()
        if stop-start>1.0 and enforceTime == True:
            print("Match forfeited by",playerColor)
            return redWinCount,blackWinCount        
    if move.lower() != "quit":
        #print(winningPlayer +" won the game in a smashing victory!")
        if winningPlayer=="red":
            redWinCount+=1
        else:
            blackWinCount+=1
        return redWinCount,blackWinCount
    else:
        fileName=input("Enter a file name to save the current state of the game, or just hit enter to quit without saving the game => ")
        if fileName != "":
            saveGame(fileName,board,player)   

#checkersMain("testCrowningJumpsAndMoves.txt")
#checkersMain("testSafeMoves.txt")
#checkersMain("testTakeMiddle.txt")     #heuristic 8
#checkersMain("testLongestMoves.txt")   #heuristic 9
#checkersMain("jumpKingFirst.txt")      #heuristic 10
#checkersMain("testSaveBackRow.txt")      #heuristic 11
#checkersMain("moveToSide.txt")      #heuristic 12
#checkersMain("moveBehindBuddy.txt")      #heuristic 13

            
#checkersMain("jumpBetween.txt")      #future heuristic 
redWinCount=0
blackWinCount=0
totalGames=1001
for i in range(totalGames):
    redWinCount,blackWinCount=checkersMain("",redWinCount,blackWinCount)
    print(redWinCount,blackWinCount)
print("Red wins =",redWinCount,"    Black wins =",blackWinCount)
print("%5.2f%% %5.2f%%" %((redWinCount/totalGames*100),(blackWinCount/totalGames*100)))
