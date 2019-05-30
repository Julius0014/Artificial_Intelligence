SuDokuBoard = [ [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,6,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,7,0,0,1,0,0,9,0],
                [0,0,0,0,0,0,0,0,0]]
cells = [[] for i in range(SuDokuBoard.__len__())]
openspaces = 0
        
def incellLeftCenterRight(cell,num):
    for i in range(3):
        for j in range(3):
            if cell[i][j] == str(num):
                if j == 0:
                    return "left"
                elif j == 1: 
                    return "center"
                elif j == 2:
                    return "right"
    return "empyplace"
def countEmpyCells(cell):  
    count  = 0 
    for i in range(3):
        for j in range(3):
            num = cell[i][j]
            if num == str(0):
                count =  count + 1
    return count     
def incelltopmidbot(cell,num):
    for i in range(3):
        for j in range(3):
            if cell[i][j] == str(num):
                if i == 0:
                    return "top"
                elif i == 1: 
                    return "mid"
                elif i == 2:
                    return "bottom"
    return "empyplace"
def findcells(sudoB,cellNum):
    #global cells
    cell = [[0,0,0],
            [0,0,0],
            [0,0,0]]
    row = 0
    col = 0
    for length in range(cellNum):
        for i in range(3):
            for j in range(3):
                #print(sudoB[ row + i][col + j],end =" ")
                cell[i][j] = sudoB[ row + i][col + j]
        col = col + 3
        if col == sudoB.__len__():
            col = 0
            row = row + 3
    return cell        
def populateCells(cells,boardLenght = 9):
    for i in range(boardLenght):
        cells[i].append(findcells(SuDokuBoard,i+1))
def findEmpy(cell):
    for i in range(3):
            for j in range(3):
                num = cell[i][j]
                if num == str(0):
                    return [i,j]
    return -1
def isNuminCol(num,col):
    for i in range(9):
        if SuDokuBoard[i][col] == str(num):
            return True
    return False
def topBottomMidLtoR(cell,cellNum):
    cell2 = findcells(SuDokuBoard,cellNum + 1)
    cell3 = findcells(SuDokuBoard,cellNum + 2)
    for i in range(9):
        pos = incelltopmidbot(cell,i+1)
        pos2 = incelltopmidbot(cell2,i+1)
        pos3 = incelltopmidbot(cell3,i+1)
        if pos == "empyplace" and pos2 != "empyplace" and pos3 != "empyplace":
            addmissingnumber(cellNum,cell,pos2,pos3,i+1)
            updateBoard(cell,cellNum)
        if pos2 == "empyplace" and pos != "empyplace" and pos3 != "empyplace":
            addmissingnumber(cellNum + 1,cell2,pos,pos3,i+1)
            updateBoard(cell2,cellNum + 1)
        if pos3 == "empyplace" and pos2 != "empyplace" and pos != "empyplace":
            addmissingnumber(cellNum + 2,cell3,pos,pos2,i+1)
            updateBoard(cell3,cellNum+2)
def addmissingnumber(CellNum,Cell,pos1,pos2,missinNum):
    if pos1 in ["top","mid"] and pos2 in ["top","mid"]:
        msg =  insertNumber(CellNum,Cell,2,missinNum)
        printmove(msg[0],msg[1],["Bottom row",pos1,pos2,CellNum])
        if msg[0] != -1:
            printcells(SuDokuBoard)
    if pos1 in ["bottom","mid"] and pos2 in ["bottom","mid"]:
        msg = insertNumber(CellNum ,Cell,0,missinNum)
        printmove(msg[0],msg[1],["TOP row",pos1,pos2,CellNum])
        if msg[0] != -1:
            printcells(SuDokuBoard)
    if pos1 in ["bottom","top"] and pos2 in ["bottom","top"]:
        msg = insertNumber(CellNum ,Cell,1,missinNum) 
        printmove(msg[0],msg[1],["Middle row",pos1,pos2,CellNum])
        if msg[0] != -1:
            printcells(SuDokuBoard)
def insertNumber(cellNum,cell,row,mNum):
    count = 0
    Backup = [ ]
    for j in range(3):
        num = cell[row][j]
        if num == str(0):
            Trow = ch(cellNum,row,j)
            Colboolen = isNuminCol(mNum,Trow[1]) #true col in SuDokuBoard
            rowboolen = isNuminRow(mNum,Trow[0])#true row in SuDokuBoar
            if Colboolen == False and rowboolen == False:
                Backup = row,j
                count = count + 1    
    if count == 1:
        row,col = Backup
        row,col = Backup
        trueRow,trueCol = ch(cellNum,row,col)
        cell[row][col] = str(mNum)
        SuDokuBoard[trueRow][trueCol] = "*"
        return[False,mNum]
    else:
        return [-1,-1]
def ch(cellNum,row,col):
    col2 = 0
    for length in range(cellNum):
        for i in range(3):
            for j in range(3):
                if length == (cellNum - 1):    
                    return [i+row,j+col2+col]
        col2 = col2 + 3
        if col2 >= SuDokuBoard.__len__():
            col2 = 0
            row = row + 3  
def updateBoard(cell,cellNum):
    row = 0
    col = 0
    for length in range(cellNum):
        for i in range(3):
            for j in range(3):
                if length == (cellNum - 1):    
                 SuDokuBoard[ row + i][col + j] = cell[i][j];
        col = col + 3
        if col == SuDokuBoard.__len__():
            col = 0
            row = row + 3
def isNuminRow(num,row):
    for i in range(9):
        if SuDokuBoard[row][i] == str(num):
            return True
    return False
def findpossible(cell):
   possible = [1,2,3,4,5,6,7,8,9]
   for i in range(9):
        for row in cell:
            for d in row:
                if d == str(i + 1):
                   possible.remove(i + 1)
   return possible    
def printcells(sudoB):
    row = 0
    col = 0
    for length in range(9):
        print("|",end = "")
        for i in range(9):
            print(sudoB[length][i],end = "|")
            if (i + 1) in [3,6]:
                print(" ",end = "|")
        print("")    
        if (length+1) %3 == 0:
            print("\t")
def isIncell(cell,num):
    for row in cell:
        for d in row:
            if d == str(num):
                return True
    return False
def solvecell(SuDokuBoard,Cell,cn):
    empyplace = findEmpy(Cell)
    possible = findpossible(Cell)
    for num in possible:
        incell = isIncell(Cell,num)
        row,col = ch(cn,empyplace[0],empyplace[1])
        col1 = isNuminCol(num,col)
        row1= isNuminRow(num,row)
        if row1 == False and col1 == False and incell == False:
            Cell[empyplace[0]][empyplace[1]] = str(num)    
            SuDokuBoard[row][col] = "*"
            printmove("Cleanup",num,"cell")
            printcells(SuDokuBoard)
            return Cell
    return Cell
def insertNumberLtoR(cellNum,cell,col,mNum):
    count = 0
    Backup = [ ]
    for j in range(3):
        num = cell[j][col]
        if num == str(0):
            Trow = ch(cellNum,j,col)
            Colboolen = isNuminCol(mNum,Trow[1]) #true col in SuDokuBoard
            rowboolen = isNuminRow(mNum,Trow[0])#true row in SuDokuBoard
            if Colboolen == False and rowboolen == False:
                Backup = j,col
                count = count + 1
    if count == 1:
        row,col = Backup
        trueRow,trueCol = ch(cellNum,row,col)
        cell[row][col] = str(mNum)
        SuDokuBoard[trueRow][trueCol] = "*"
        return[True,mNum]
    else:
        return [-1,-1]
def addmissingnumberLtoR(CellNum,Cell,pos1,pos2,missinNum):
    if pos1 in ["left","center"] and pos2 in ["left","center"]:
        msg = insertNumberLtoR(CellNum,Cell,2,missinNum)
        printmove(msg[0],msg[1],["Right Column",pos1,pos2,CellNum])
        if msg[0] != -1:
            printcells(SuDokuBoard)
    if pos1 in ["center","right"] and pos2 in ["center","right"]:
        msg = insertNumberLtoR(CellNum ,Cell,0,missinNum)
        printmove(msg[0],msg[1],["Left Column",pos1,pos2,CellNum])
        if msg[0] != -1:
            printcells(SuDokuBoard)
    if pos1 in ["left","right"] and pos2 in ["left","right"]:
        msg = insertNumberLtoR(CellNum ,Cell,1,missinNum)
        printmove(msg[0],msg[1],["Center Column",pos1,pos2,CellNum])
        if msg[0] != -1:
            printcells(SuDokuBoard)
def LeftCenterRight(cell,cellNum):
    cell2 = findcells(SuDokuBoard,cellNum + 3)
    cell3 = findcells(SuDokuBoard,cellNum + 6)
    for i in range(9):

        pos = incellLeftCenterRight(cell,i+1)
        pos2 = incellLeftCenterRight(cell2,i+1)
        pos3 = incellLeftCenterRight(cell3,i+1)
        if pos == "empyplace" and pos2 != "empyplace" and pos3 != "empyplace":
            addmissingnumberLtoR(cellNum,cell,pos2,pos3,i+1)
            updateBoard(cell,cellNum)
            populateCells(cells)
        if pos2 == "empyplace" and pos != "empyplace" and pos3 != "empyplace":
            addmissingnumberLtoR(cellNum + 3,cell2,pos,pos3,i+1)
            updateBoard(cell2,cellNum + 3)
            populateCells(cells)
        if pos3 == "empyplace" and pos2 != "empyplace" and pos != "empyplace":
            addmissingnumberLtoR(cellNum + 6,cell3,pos,pos2,i+1)
            updateBoard(cell3,cellNum+6)
            populateCells(cells)    
def findopenspaces():
    count = 0
    for i in range(9):
        for j in range(9):
            if SuDokuBoard[i][j] == "0":
                count = count + 1
    return count
def printmove(Msg,Num,place):
    if(Msg == "Cleanup"):
        print("Cleaning up:")
        print("\tInserting "+str(Num)+" to complete the "+place)
    if(Msg == True): 
        print("Left Center Right:\n")
        if "Center" in place[0]:
            print("\tLeft Column Has an "+str(Num)) 
            print("\tRight Column Has an "+str(Num))
        
        if "Left" in place[0]:
            print("\tCenter Column Has an "+str(Num)) 
            print("\tRight Column Has an "+str(Num))
        if "Right" in place[0]:
            print("\tLeft Column Has an "+str(Num)) 
            print("\tCenter Column Has an "+str(Num))
        print("\tInserting "+str(Num)+" in cell "+str(place[3])+" to the "+place[0]+" to Complete Rules")
    if(Msg == False):
        print("Top Middle Bottom:\n\tAdding "+str(Num)+" in cell "+str(place[3])+" to the "+place[0]) 
        if "TOP" in place[0]:
            print("\tBottom Row Has an "+str(Num)) 
            print("\tMiddle Row Has an "+str(Num))
        
        if "Bottom" in place[0]:
            print("\tTop Row Has an "+str(Num)) 
            print("\tMiddle Row Has an "+str(Num))
        if "Middle" in place[0]:
            print("\tTop Row Has an "+str(Num)) 
            print("\tBottom Row Has an "+str(Num))
def finishCell():
    for i in range(9):
        cell = findcells(SuDokuBoard,i + 1)
        count = countEmpyCells(cell)
        if count < 2:
            cell = solvecell(SuDokuBoard,cell,i+1)
            updateBoard(cell,i + 1)
            populateCells(cells)
        
def finishcol():
    global SuDokuBoard
    count = 0
    possibleNumber = ["1","2","3","4","5","6","7","8","9"]
    for i in range(9):
        for j in range(9):
            num = SuDokuBoard[j][i]
            if str(num) in possibleNumber:
                count = count + 1
                possibleNumber.remove(str(num))
            else:
                pos = [j,i]
        if len(possibleNumber) == 1:
            num = possibleNumber[0]
            SuDokuBoard[pos[0]][pos[1]] = "*"
            printmove("Cleanup",num,"Column")
            printcells(SuDokuBoard)
            SuDokuBoard[pos[0]][pos[1]] = possibleNumber[0]
        possibleNumber = ["1","2","3","4","5","6","7","8","9"]
def finishrow():
    possibleNumber = ["1","2","3","4","5","6","7","8","9"]
    for i in range(9):
        for j in range(9):
            num = SuDokuBoard[i][j]
            if str(num) in possibleNumber:
                possibleNumber.remove(str(num))
            else:
                pos = [i,j]
        if len(possibleNumber) == 1:
            num = possibleNumber[0]
            SuDokuBoard[pos[0]][pos[1]] = "*"
            printmove("Cleanup",num,"Row")
            printcells(SuDokuBoard)
            SuDokuBoard[pos[0]][pos[1]] = possibleNumber[0]
        possibleNumber = ["1","2","3","4","5","6","7","8","9"]


def solvePuzzle(SuDokuBoard):
    numMoves = 1
    lastmoves = 0
    while numMoves != 0:
        cell = findcells(SuDokuBoard,1)
        topBottomMidLtoR(cell,1)
        cell = findcells(SuDokuBoard,4)
        topBottomMidLtoR(cell,4)
        cell = findcells(SuDokuBoard,7)
        topBottomMidLtoR(cell,7)
        cell = findcells(SuDokuBoard,1)
        LeftCenterRight(cell,1)
        cell = findcells(SuDokuBoard,2)
        LeftCenterRight(cell,2)
        cell = findcells(SuDokuBoard,3)
        LeftCenterRight(cell,3)
        finishCell()
        finishrow()
        finishcol()
        lastNumMoves = numMoves;
        numMoves = findopenspaces()
        if lastNumMoves == numMoves:
            lastmoves = lastmoves + 1
        if lastmoves == 40 :
            print("Error Can't Solve Puzzle")
            break;
    if lastmoves != 40:
        print("Game Solve")
        printcells(SuDokuBoard)        
#side to side #do dowun up check all most finshcells
def fileSetup(filename): 
    file = open(filename,"r")
    lineNum = 0
    i = 0
    for line in file:
        if "Grid" in line:
            print("*****"+str(line)+"*****")
            continue;
        j = 0
        for char in line.rstrip("\n"):
            SuDokuBoard[i][j] = char 
            j = j + 1
        i = i + 1

        lineNum = lineNum + 1
        if lineNum == 9:
            lineNum = 0
            i = 0
            solvePuzzle(SuDokuBoard)
fileSetup("a.txt")

