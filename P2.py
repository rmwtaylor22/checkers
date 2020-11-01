import random
import copy
import time

timeRestriction = True
startTime = 0
#row is the letter and goes sideways
#col is the num and goes up and down

def removeCheckerLogical(FROMCol,FROMRow,board):
    FromCol = int(FROMCol)
    FromRow = ord(FROMRow)-65 
    playerBoardToken=board[FromRow][FromCol] #copy the player token from the logical board, could be "b" or "B" or "r" or "R"
    board[FromRow][FromCol]='e' #set the logical board location to empty
    return playerBoardToken

def placeCheckerLogical(TOCol,TORow,board,playerToken):
    ToCol = int(TOCol)
    ToRow = ord(TORow)-65
    #print(type(ToCol), type(ToRow))
    #Logical board update first
    if playerToken == "r" and ToCol==7:  #if a kinging move for red
        board[ToRow][ToCol]=playerToken.upper()
    elif playerToken == "b" and ToCol==0: #if a kinging move for black
        board[ToRow][ToCol]=playerToken.upper()
    else: #all non-kinging moves place checker in logical board
        #print(type(ToCol), type(ToRow))
        board[ToRow][ToCol]=playerToken



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

def takeTheMiddle(board,player,movesList):      #heuristic 8, moves checker to the middle to gain control
    takeCenterList = []
    if board[4][4] == "e" and board[4][2] == "e" and board[3][3] == "e" and board[3][5] == "e":
        if player == "b":
            for move in movesList:
                if move[-2:] == "E4":
                    takeCenterList.append(move)
                elif move[-2:] == "E2":
                    takeCenterList.append(move)
        else:
            for move in movesList:
                if move[-2:] == "D3":
                    takeCenterList.append(move)
                elif move[-2:] == "D5":
                    takeCenterList.append(move)
    return takeCenterList

def chooseLongestMove(theList):                 #heuristic 9, chooses the longest move to take
    longestMove = theList[0]
    #print(longestMove)
    for move in theList:
        if len(move) > len(longestMove):
            #print("True")
            longestMove = move
            #print(longestMove)
            #print("True?")
    return longestMove

        
def jumpKingFirst(board,possibleJumps,player):  #heuristic 10, jumps a king player first
    #print(possibleJumps)
    kingJumpsLst = []
    if player == "b":
        opponentKingToken = "R"
    else:
        opponentKingToken = "B"
    for jump in possibleJumps:
        #print(jump)
        toRow=ord(jump[-2])-65          #putting it in terms where I can check the board
        toCol=int(jump[-1])
        fromRow=ord(jump[0])-65
        fromCol=int(jump[1])
        if board[(toRow+fromRow)//2][(toCol+fromCol)//2] == opponentKingToken:        #has a king between them
            kingJumpsLst.append(jump)
    return kingJumpsLst

def holdBackRow(movesList,player):      #heuristic 11, perserves the back row as long as possible
    nonBackRowCheckers = []
    if player == "b":
        backRowLetter = "H"
    else:
        backRowLetter = "A"
    for move in movesList:
        #print("here are the moves in movesList:", move)
        if move[0] != backRowLetter:
            #print("this move was deemed not in the back row")
            nonBackRowCheckers.append(move)
    if nonBackRowCheckers != []:
        #print(nonBackRowCheckers)
        return nonBackRowCheckers
    else:
        return movesList

##def tweenerList(board,player,movesList):      #heuristic 12, moves or jumps between opponent peices to protect themselves and block opponent
##    tweenerList=[]
##    for move in movesList:
##        toRow=ord(move[-2])-65          #putting it in terms where I can check the board
##        toCol=int(move[-1])
##        fromRow=ord(move[0])-65
##        fromCol=int(move[1])
##        if player == "r":
##            if board[toRow+1][toCol+1] == "b" and board[toRow+1][toCol-1] == "b":
##                    tweenerList.append(move)
##        else:
##            if board[toRow-1][toCol-1] == "r" and board[toRow-1][toCol+1] == "r":
##                tweenerList.append(move)
##    return tweenerList


def moveBehindBuddy(board,player,movesList):
    takeUpTheRear = []
    for move in movesList:
        toRow=ord(move[-2])-65          #putting it in terms where I can check the board
        toCol=int(move[-1])
        fromRow=ord(move[0])-65
        fromCol=int(move[1])
        if player == "r" and (toCol+1) in range(0,8) and (toRow+1) in range(0,8):
            if board[toRow+1][toCol+1] == "r" or board[toRow+1][toCol+1] == "r":
                takeUpTheRear.append(move)
        elif player == "b" and (toCol-1) in range(0,8) and (toRow-1) in range(0,8):
            if board[toRow-1][toCol-1] == "b" or board[toRow-1][toCol+1] == "b":
                takeUpTheRear.append(move)

    return takeUpTheRear

def moveToTheSide(movesList):             #heuristic 12, moves checkers up the side
    sideList = []
    for move in movesList:
        if move[-1] == 0 or move[-1] == 7:
            sideList.append(move)
    return sideList
                  


        
def findCrownRowMovesOrJumps(board,player,movesList):
    kingingList=[]
    for move in movesList:
        FROM=move[0:2]
        FROMRow=ord(FROM[0])-65
        FROMCol=int(FROM[1])
        TO=move[-2:]
        TORow=TO[0]
        if player=="r":
            kingRow="H"
        else:
            kingRow="A"
        if board[FROMRow][FROMCol]==player and TORow==kingRow:
            kingingList.append(move)
            movesList=movesList[:movesList.index(move)]+movesList[movesList.index(move)+1:]
    return kingingList    # later have this remove kinging list moves from valid moves

def theValidMovez(board,player):
    movesList=listValidMoves(board,player)
    jumpsList=listSingleJumps(board,player)
    jumpsList=listMultipleJumps(board,player,jumpsList) #add heuristics by order
    if jumpsList != []:
        return jumpsList
    else:
        return movesList
def clock():
    global startTime
    return time.time() - startTime


##    crowningJumps, jumpsList =findCrownRowMovesOrJumps(board,player,jumpsList)
##    crowningMoves, movesList =findCrownRowMovesOrJumps(board,player,movesList)

    if jumpsList != []:             # if crowningJumps + jumpsList != []:  
        return jumpsList
    else:
        return movesList    # if crowningMoves + movessList != []:  

##    takeMiddle = takeTheMiddle(board,player,movesList)
##    jumpOppKing = jumpKingFirst(board,jumpsList,player)
##    moveBtwnOpp = tweenerList(board,player,movesList)
##    jumpBtwnOpp = tweenerList(board,player,jumpsList)
##    moveBehindSelf = moveBehindBuddy(board,player,movesList)
##    moveToSide = moveToTheSide(movesList)
##    if player=="r":
##        player="b"
##    else:
##        player="r"
##    opposingMovesList=listValidMoves(board,player)
##    opposingJumpsList=listSingleJumps(board,player)
##    opposingJumpsList=listMultipleJumps(board,player,opposingJumpsList)
##    opposingCrowningJumps=findCrownRowMovesOrJumps(board,player,opposingJumpsList)
##    opposingCrowningMoves=findCrownRowMovesOrJumps(board,player,opposingMovesList)



##    if player == "r":
##        player="b"
##    else:
##        player="r"
##    #heuristics bois
##        #jumps first!
##    if opposingCrowningJumps != []:
##        for oppJump in opposingCrowningJumps:
##            for move in jumpsList:
##                possibleMoves = []
##                thisWorks = False
##                if move[-2:] == oppJump[-2:]:
##                    thisWorks = True
##                    possibleMoves.append(move)
##                if thisWorks == True:
##                    saveBackR = holdBackRow(possibleMoves,player)    #heuristic 11, preserves the back row for as long as possible
##                    longestMove = chooseLongestMove(saveBackR) #heuristic 9, chooses the longest move to take
##                    return longestMove
##    if opposingCrowningMoves != []:
##        for oppMove in opposingCrowningMoves:
##            for move in jumpsList:
##                possibleMoves = []
##                thisWorks = False
##                if move[-2:] == oppMove[-2:]:
##                    thisWorks = True
##                    possibleMoves.append(move)
##                if thisWorks == True:
##                    saveBackR = holdBackRow(possibleMoves,player)    #heuristic 11, preserves the back row for as long as possible
##                    longestMove = chooseLongestMove(saveBackR) #heuristic 9, chooses the longest move to take
##                    return longestMove
##    if opposingJumpsList != []:
##        for oppMove in opposingJumpsList:
##            for move in jumpsList:
##                possibleMoves = []
##                thisWorks = False
##                if move[-2:] == oppMove[-2:]:
##                    thisWorks = True
##                    possibleMoves.append(move)
##                if thisWorks == True:
##                    saveBackR = holdBackRow(possibleMoves,player)    #heuristic 11, preserves the back row for as long as possible
##                    longestMove = chooseLongestMove(saveBackR) #heuristic 9, chooses the longest move to take
##                    return longestMove
##
##    if crowningJumps != []:  #if
##        longestMove = chooseLongestMove(crowningJumps) #heuristic 9, chooses the longest move to take
##        return longestMove
##    if jumpsList != []:
##        if jumpOppKing != []:               #heuristic 10, jumps a king player first
##            return jumpOppKing[0]
####        if jumpBtwnOpp != []:
####            return jumpBtwnOpp[0]
##        else:
##            saveBackR = holdBackRow(jumpsList,player)    #heuristic 11, preserves the back row for as long as possible
##            longestMove = chooseLongestMove(saveBackR) #heuristic 9, chooses the longest move to take
##            return longestMove
##        
###### MOVES
##    if opposingCrowningJumps != []:   
##        for oppJump in opposingCrowningJumps:
##            for move in movesList:
##                possibleMoves = []
##                thisWorks = False
##                if move[-2:] == oppJump[-2:]:
##                    thisWorks = True
##                    possibleMoves.append(move)
##                if thisWorks == True:
##                    saveBackR = holdBackRow(possibleMoves,player)    #heuristic 11, preserves the back row for as long as possible
##                    longestMove = chooseLongestMove(saveBackR) #heuristic 9, chooses the longest move to take
##                    return longestMove
##    if opposingCrowningMoves != []:      
##        for oppMove in opposingCrowningMoves:
##            for move in movesList:
##                possibleMoves = []
##                thisWorks = False
##                if move[-2:] == oppMove[-2:]:
##                    thisWorks = True
##                    possibleMoves.append(move)
##                if thisWorks == True:
##                    saveBackR = holdBackRow(possibleMoves,player)    #heuristic 11, preserves the back row for as long as possible
##                    longestMove = chooseLongestMove(saveBackR) #heuristic 9, chooses the longest move to take
##                    return longestMove
##    if opposingJumpsList != []:      
##        for oppMove in opposingJumpsList:
##            for move in movesList:
##                possibleMoves = []
##                thisWorks = False
##                if move[-2:] == oppMove[-2:]:
##                    thisWorks = True
##                    possibleMoves.append(move)
##                if thisWorks == True:
##                    saveBackR = holdBackRow(possibleMoves,player)    #heuristic 11, preserves the back row for as long as possible
##                    longestMove = chooseLongestMove(saveBackR) #heuristic 9, chooses the longest move to take
##                    return longestMove
##    if crowningMoves != []:
##        longestMove = chooseLongestMove(crowningMoves) #heuristic 9, chooses the longest move to take
##        return longestMove
####    if moveBtwnOpp != []:
####        return moveBtwnOpp[0]
##    if moveBehindSelf != []:                          #heuristic 13, moves behind other same-color player to protect it
##        return moveBehindSelf[0]
##    if takeMiddle != []: # heuristic 8, moves checker to the middle to gain control
##        #print("We got to takeMiddle!")
##        longestMove = chooseLongestMove(takeMiddle) #heuristic 9, chooses the longest move to take
##        return longestMove
##    if moveToSide != []:                            #heuristic 12, moves checkers up the side
##        return moveToSide[0]
##        
##    else: # movesList != []:
##        #print("We got to movesList!")
##        saveBackR = holdBackRow(movesList,player)
##        if saveBackR != []:
##            return saveBackR[0]                        #heuristic 11, preserves the back row for as long as possible
##        else:    
##            return movesList[0]
#######################################################################################################################################################################################
def getValidMove(board,player):
    global startTime
    startTime = time.time()
    val,move = lookAhead(board,4,player)
    print(clock())
    return move
def calculateScore(board,player):
    redScore = 0.0
    blackScore = 0.0

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == "r":
                redScore += 1.0
            elif board[i][j] == "R":
                redScore += 2.0
            elif board[i][j] == "b":
                blackScore += 1.0
            elif board[i][j] == "B":
                blackScore += 2.0

                # add heuistic that adds percentage of how close it is to kinging
                # add advantage for home row kept
    
    if blackScore < 1:
        return 1999/(10-idx)  # prioritizes wins that happen sooner
    if redScore < 1:
        return -1999/(10-idx)  # prioritizes wins that happen sooner
                
    return redScore - blackScore



            
def lookAhead(board,recIdx,player):
    if recIdx < 1:
        return calculateScore(board,player),""            
        #algorithm for assigning a score to the moves
    else:
        if player == "r":
            otherPlayer = "b"
            sign = 1
        else:
            otherPlayer = "r"
            sign = -1
            
        if clock() > .9:
            print("timeout")
            return -1000*sign,""
        
        newBoard = copy.deepcopy(board)
        validMoves = theValidMovez(copy.deepcopy(board),player)
        if validMoves == []:
            return -1000*sign, ""      #this happens when it's the end of  game
        highscore = -1000*sign
        bestMove = validMoves[0]
        for move in validMoves:
            if clock() > .9 and timeRestriction:
                print("timeout")
                break
            #updateBoard
            placeCheckerLogical(move[-1],move[-2],copy.deepcopy(board),player)
            removeCheckerLogical(move[1],move[0],copy.deepcopy(board))
            score,aMove = lookAhead(copy.deepcopy(board),recIdx-1,otherPlayer)
            if player == "r":
                if score > highscore:
                    highscore = score
                    bestMove = move
            else:
                if score < highscore:
                    highscore = score
                    bestMove = move
    return highscore,bestMove                        #looks at opposite player's move and point value, multiplies it by -1 to get our own point value to evaluate.
            









    
