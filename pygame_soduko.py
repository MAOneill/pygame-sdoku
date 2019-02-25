import pygame
import random 

#this includes the strings to draw a custom cursor that kind of looks like a pencil
from pencil_strings import pencil_strings

#this is the functiont that can read in the raw board settings
#raw board is an array of 9 arrays with 9 tuples each

random = random.randint(1, 3)   

#this works...but some of the documentation says not to use it....
exec('from board%d_raw import rawboard' % random)

class Tcell():
    def __init__(self,tinycell,x,y):
        self.set = False
        self.image = pygame.image.load('numbers/pencil_blank_diff.png' ).convert_alpha()
        self.xpos = x + ((tinycell-1) % 3) * 27
        self.ypos = y + ((tinycell-1) // 3) * 27
        self.number = tinycell
    def update_pencil_image(self):
        if self.set == True:
            # print("the pencil cell is %d" % self.number)
            self.image = pygame.image.load('numbers/%d_pencil_diff.png' % self.number).convert_alpha()
        else:  #use blank
            self.image = pygame.image.load('numbers/pencil_blank_diff.png' ).convert_alpha()

#for the possibles
# class Pcell():
#     def __init__(self,possible):
#         self.possible = possible        #one through nine
#         self.value = 0                  #can be 0 or 1

class Cell():
    #define the playing cell.  there are 81 of these in an 9x9 soduko board
    def __init__(self,row,col,value,answer=None):
        # self.start = value  #or is this in the subclass...
        # self.anser = 
        self.row = row
        self.col = col
        #  self.inner = 0  #compute thie
        # self.pencils = {}  #{} will object create this and set here

        self.guess = None       #blank to start
        self.value = value      #given in start cube
        self.answer = answer    #if loaded in answers, used for hints

        self.name = "r%dc%d" % (row,col)

        rowbox = int((row-1)//3)
        colbox = int((col-1)//3)
        self.inner = (rowbox *3 )+ colbox+ 1

        self.x_position = (col-1) * 81
        self.y_position = (row-1) * 81    

        #you can only change the image for an unknown cell or blank:
    def change_cell_image(self):
        pass

class Known_cell(Cell):
    def __init__(self,row,col,value,answer):
        super().__init__(row,col,value,answer)
        self.answer = answer  
        #known cells don't need pencils or possibles
        # self.possibles = {}  #empty    
        self.image = pygame.image.load('numbers/%d_background_transparent.png' % answer).convert_alpha()
        # self.image = pygame.image.load('numbers/%d_transparent_number.png' % value).convert_alpha()
    
class Unknown_cell(Cell):
    def __init__(self,row,col,value,answer=None):
        super().__init__(row,col,value,answer)
        self.answer = answer
        self.value = 0
        self.pencils ={}
        for tinycell in range(1,10):
            self.pencils[tinycell] = Tcell(tinycell,self.x_position,self.y_position)
        #change this to a null image
        self.image = None
    def change_cell_image(self):
        # print(self.guess)
        #changes the display image based on the GUESS value
        if self.guess == None or self.guess == 0:
            self.image = None       #undo can set it back to zero
        else:
            self.image = pygame.image.load('numbers/%d_guess.png' % self.guess).convert_alpha()

class Blank_cell(Cell):
    #used in the SOLVING part of the program, not the game play
    def __init__(self,row,col,value=0,answer=0):
        super().__init__(row,col,value,answer)
        # self.possibles = {1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9}
        self.possibles = {}
        # for p in range(1,10):
        #     self.possibles[p] = Pcell(p)
        # self.image = None
        self.image = None
    def change_cell_image(self):
    #changes the display image based on the "value"
    # if answer not none, use that.  otherwise, use value:
        if self.value == None or self.answer == None:
            self.image = None       #undo can set it back to zero
        elif self.answer != 0:
            self.image = pygame.image.load('numbers/%d_guess.png' % self.answer).convert_alpha()
        else:
            self.image = pygame.image.load('numbers/%d_guess.png' % self.value).convert_alpha()
      
def create_cell(row,col,tuple,known):
    #process to create all 81 objects AND load them into an array
    #I didn't not put this inside a function because I need the individual
    #objects accessable by their name

    newcell = {}
    if known:       #known is true
        newcell = Known_cell(row,col,tuple[0],tuple[1]) #all named 'newcell'
    else:
        newcell = Unknown_cell(row,col,tuple[0],tuple[1]) #all named 'newcell'
    return newcell     #this points to entirely new spot each time

def create_board(input_board):
    # returns an array of all 81 cells, NOT IN ROWS
    allcells = {}  #dictionary not array
    cell = {}    
    row = 0
    for eachrow in input_board:
        row += 1    #increment the row counter
        rowarray = []   #create a new instance here
        col = 0 
        for eachtuple in eachrow:
            col += 1
            
            #if the first value is KNOWN, then create a Known_cell class
            #otherwise create an Unknown_cell class        
            if eachtuple[0] == 0:  #unknown
                known = False  
            else:
                known = True
            
            cellname = "r%dc%d" % (row,col)
            # print(cellname)
            allcells[cellname] = create_cell(row,col,eachtuple,known)
            # print(cell['data'].value)
            # allcells.append(cell)   #append my object into the row array
    return allcells

def create_blank_board():
        # returns an array of all 81 cells, NOT IN ROWS
    allcells = {}  #dictionary not array
    cell = {}    
    for r in range(1,10) : 
        for c in range(1,10):
            cellname = "r%dc%d" % (r,c)
            allcells[cellname] = Blank_cell(r,c)
    return allcells

def print_grid(cube,what):  
    #function for printing my grid in python terminal
    #used for testing
    #default print is the initial values, unless you specifically ask for "answer"
    #can all print the inner cube values with "inner"
    #print first line:
    print("----"*9 + "-")      #top border  
    for i in range(1,10):
        print ("|",end='')  #first left border
        for j in range(1,10):
            if what == "answer":
                
                # print ((" %s |" % (each['data'].answer,)), end='') 
                print ((" %s |" % (cube['r%dc%d' % (i,j)].answer,)), end='') 
            elif what == "inner":
                # print ((" %s |" % (each['data'].inner,)), end='') 
                print ((" %s |" % (cube['r%dc%d' % (i,j)].inner,)), end='') 
            else:
                # print ((" %s |" % (each['data'].value,)), end='') 
                print ((" %s |" % (cube['r%dc%d' % (i,j)].value,)), end='') 

        print (" ") #new line
        print("----"*9 + "-") #separator lines and bottom border

def set_coordinates_from_click(event):
    x = event.pos[0]
    y = event.pos[1]
    if y in range(730) and x in range(730):
        board_clicked = True
        # use math to figure out what square they are in:
        row =  int(y // 81) + 1
        col = int (x // 81) + 1
        cell = 'r%dc%d' % (row,col)
        # calculate the pencil_cell
        tempcol = (x % 81) // 27
        temprow = (y % 81) // 27
        pencilplacement = temprow * 3 + tempcol + 1
        # print("the pencil cell is %d" % pencilplacement)
    else:
        board_clicked = False
        row = 0
        col = 0
        cell = ""
        pencilplacement = 0
    return row,col,cell,board_clicked,pencilplacement

def clear_coordinates():
    r = 0
    c = 0
    cl = ""
    penc = 0
    board_clicked = False
    # entry = 0   #should this be here??
    return r,c,cl,board_clicked,penc

def main_menu():
    width = 400
    height = 400

    #set some colores
    background_color = (159,209,204)   #blue
    pitch_blue_color = (83,94,126)

    main_answer = False

    pygame.init()       #should this be in each module??

    #try to change cursor
    
    font = pygame.font.Font('fonts/cmtt10.ttf', 22)    #must be after init                        
    #default cursor
    # pygame.mouse.set_cursor(*pygame.cursors.arrow)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Soduko - Choose game play mode')
    clock = pygame.time.Clock()

    while not main_answer:
        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.QUIT:
                main_answer = True

            if event.type == pygame.KEYDOWN:   
                # myentry = event.key
                choices = {97:"Play",98:"Solve",27:"Esc"}
                game_state = choices.get(event.key,None)  #don't change the state unless a valid state
                print ("game state is %s" % game_state)
                if game_state == "Esc":  #this will end the game
                    main_answer = True
                elif game_state == "Play":
                    main_answer = True
                elif game_state == "Solve":
                    main_answer = True
                


        screen.fill(background_color)

        window_text = font.render('Enter A for Play mode.', True, (pitch_blue_color))
        window_text2 = font.render('Or B for solving mode.', True, (pitch_blue_color))
        
        screen.blit(window_text, (100,100))
        screen.blit(window_text2, (100,250))

        pygame.display.update()     #internal function

        clock.tick(60)  #600 makes the fan go crazy
    
    print(__name__)
    return game_state

    # pygame.quit()   #change to return  #quit when you are out of while loop

def solve():
    board = create_blank_board()
    
    #testing
    # print(board['r4c8'].possibles[8])
    # board['r8c3'].value = 7
    # board['r3c5'].answer = 5

    # print_grid(board,"answer")
    # print_grid(board,"value")

    # if type(board['r8c3']) == Blank_cell:
    #     print("blank")
    # else:
    #     print("waht?")
    # print(board['r8c3'].value)

    # board['r8c3'].change_cell_image()
    # print (board['r8c3'].image)

    # declare the size of the canvas
    width = 730
    height = 730

    #set some colores
    blue_color = (97, 159, 182)  
    background_color = (244,237,221)  #cream
    # background_color = (216,212,182)
    # background_color = (159,209,204)   #blue


    #initalize pygame and playing window
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Soduko Solver')
    clock = pygame.time.Clock()

    #set some fonts - do AFTER pygame.init
    # font = pygame.font.Font(None, 25)                 
    # #set sytem font.  (filename, size)
    font = pygame.font.Font('fonts/cmtt10.ttf', 22)                           
    # font = pygame.font.Font('fonts/futurachapro-Regular.ttf', 25)                           

    #default images used throughout
    grid_image = pygame.image.load('numbers/big_grid_lines.png').convert_alpha()

    # Draw background
    screen.fill(background_color)
    stop_game = False

    while not stop_game:
        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.QUIT:
                stop_game = True

        #get events from user - clicks, keyboard
        if event.type == pygame.KEYDOWN:   
                # myentry = event.key
                choices = {27:"Esc"}
                game_state = choices.get(event.key,None)  #don't change the state unless a valid state
                print ("game state is %s" % game_state)
                if game_state == "Esc":  #this will end the game
                    stop_game = True

        # update the display
        # should only be done if there were changes....add this
        for thecell in board.values():
            if thecell.image != None :
                screen.blit(thecell.image, (thecell.x_position,thecell.y_position))

        screen.blit(grid_image, (0,0))
        pygame.display.update()     #internal function
        clock.tick(60)  #600 makes the fan go crazy

    pygame.quit()

def play():     #or rename this "Play"

    # declare the size of the canvas
    width = 900
    height = 810

    #set some colores
    blue_color = (97, 159, 182)  #background color
    background_color = (244,237,221)  #cream
    background_color = (216,212,182)
    # background_color = (159,209,204)   #blue
    blue_color = (97, 159, 182)  #sky_blue
    red_color = (255,0,0)
    pitch_blue_color = (83,94,126)
    red_color = (255,0,0)
    green_color = (89,162,134)
    orange_color = (224,95,20)
    sea_foam_color = (159,209,204)


    #initalize pygame and playing window
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Soduko')
    clock = pygame.time.Clock()

    #set some fonts - do AFTER pygame.init
    # font = pygame.font.Font(None, 25)                 
    # #set sytem font.  (filename, size)
    font = pygame.font.Font('fonts/cmtt10.ttf', 22)                           
    # font = pygame.font.Font('fonts/futurachapro-Regular.ttf', 25)                           

    #default images used throughout
    grid_image = pygame.image.load('numbers/big_grid_lines.png').convert_alpha()
    pencil_grid_image = pygame.image.load('numbers/litte_grid_lines.png').convert_alpha()
    # big_x_image = pygame.image.load('numbers/x.png').convert_alpha()
    big_x_image = pygame.image.load('numbers/x_diffuse.png').convert_alpha()


##################################################################################################
###everything below here is for the game play mode. ##############################################
##################################################################################################

    # Game initialization

    #create data
    board = create_board(rawboard)
    
    # for each in board.values():
    #     print(each.answer)
    #these print to the terminalo
    # print_grid(board,"value")
    # print_grid(board,"answer")
    # print_grid(board,"inner")


    #message text
    message_text = font.render('', True, (orange_color))        
    
    #set initial values to be used throughout  
    row,col,cell,pencil_box,board_clicked = clear_coordinates()      

    undo_array = []     #this holds the cells that have had value changed.  in order.  it can hold duplicates
    stop_game = False
    game_state = "Normal"  #default mode
    entry = 0       #where and why do I need this????
    any_change = True

    while not stop_game:
        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.QUIT:
                stop_game = True

            # GET USER INPUT VALUES FROM KEYBOARD AND MOUSE
            if event.type == pygame.MOUSEBUTTONDOWN:            #get board_coordinates

                # if in game board return coordinates. 
                # a click outside of the soduko board does NOTHING
                row,col,cell,board_clicked,pencil_box = set_coordinates_from_click(event)
                entry = 0
                any_change = True
            
            if event.type == pygame.KEYDOWN:            #get game_state
                # print('key down %r. game state is %s' % (event.key,game_state))
                entry = event.key
                # letter_choices = {121:"Y",115:"Solved",98:"Blank",103:"Newgame"}
                letter_choices = {110:"Normal",112:"Pencil",27:"Esc",117:"Undo",104:"Hint",101:"Error"}
                game_state = letter_choices.get(entry,game_state)  #don't change the state unless a valid state
                any_change = True
                if game_state == "Esc":  #this will end the game
                    stop_game = True
                print("game state is %s" % game_state)

                # if game_state not "Normal", a key press should reset board_clicked to false
                if game_state != "Normal":
                    board_clicked = False

            if game_state == "Pencil":
                datatuple, masktuple = pygame.cursors.compile( pencil_strings,black='.', white='X', xor='o' )
                pygame.mouse.set_cursor( (24,24), (0,0), datatuple, masktuple )
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)


            #state evaluations and GAME LOGIC
            if game_state == "Normal":
                message_text =  font.render('Click on a blank square to enter value', True, (orange_color))
            if game_state == "Error":
                message_text =  font.render('These are your mistakes', True, (orange_color))


            #we are in the "Normal" state and a key has been pressed
            #added delete key (8) to be set to zero
            if board_clicked == True and game_state == "Normal":  
                # print (entry)
                choices = {49:1,50:2,51:3,52:4,53:5,54:6,55:7,56:8,57:9,48:0,8:0}
                number = choices.get(entry, None) 
                if number != None:      #it got a value number
                    #update cell value
                    #add the current cell and its CURRENT vaue to the undo_array
                    
                    undo_pair = (cell,board[cell].guess)
                    undo_array.append(undo_pair)

                    #if user enters 0, blank out the value
                    if number == 0:
                        board[cell].guess = None
                    else:
                        board[cell].guess = number
                    print(undo_array)
                    board[cell].change_cell_image()
                    # board['r%dc%d' % (row,col)].change_cell_image()
                    #flip switches:
                    board_clicked = False
                    entry = 0  #reset entry
                    #change message
                    message_text = font.render("", True, (orange_color))  

                else:
                    message_text = font.render('You are editing row: %d / column: %d.  You can only enter numbers' % (row,col), True, (orange_color))  
            
            if game_state == "Pencil":

                message_text = font.render("click on the tiny cell to toggle-in your possible options" , True, (orange_color))

                if board_clicked == True and type(board[cell]) == Unknown_cell: 
                        #update  pencil cell value (true/false) - flip its value
                        board[cell].pencils[pencil_box].set = not board[cell].pencils[pencil_box].set
                        #updae pencil cell image
                        board[cell].pencils[pencil_box].update_pencil_image()  #self.value work?
                        #board_clicked goes back to false till a new click happens
                        board_clicked = False

            if game_state == "Undo":
                message_text = font.render("Press Undo again to revert your changes one by one." , True, (orange_color))
                
                if len(undo_array) > 0:
                    to_remove = undo_array.pop()
                    # print (to_remove)
                    #the cell is changed back to its old value
                    board[to_remove[0]].guess = to_remove[1]
                    #update the image for the cell
                    board[to_remove[0]].change_cell_image()
                

                else:
                    game_state = "Normal"
                    message_text = font.render("There are no more changes to Undo." , True, (orange_color))
                #revert screen display to Normal
                game_state = "Normal"
 
            if game_state == "Hint":
                message_text = font.render('Select the cell you want the answer to', True, (orange_color))
                
                if board_clicked == True:
                    print("my cell is within hint")
                    print(cell)
                    if board[cell].answer == 0:
                        message_text = font.render("No Hint available", True, (orange_color))
                    else :
                        
                        board[cell].guess = board[cell].answer
                        board[cell].change_cell_image()
                
                    entry = 0        
                    game_state = "Normal"  #set back to "Normal"
                    print(game_state)
                    board_clicked = False

        # Draw background
        screen.fill(background_color)

        # Game display 
        #only do this if there has been a change (any_change)

        if any_change == True:
            #set the blits for all known numbers
            for thecell in board.values():
                # if game_state == "Normal" or game_state == "Hint" or game_state == "Error":
                if thecell.image != None :
                    screen.blit(thecell.image, (thecell.x_position,thecell.y_position))
                if game_state == "Error":  #overlay the x if guess is wrong
                    if type(thecell) == Unknown_cell and thecell.guess != thecell.answer and thecell.guess != None:
                        screen.blit(big_x_image, (thecell.x_position,thecell.y_position))

                elif game_state == "Pencil":               #in pencil mode
                            # this is OVERLAYED over the guesses
                            #while we are in pencil mode,the cells that are blank (guess = None and value = None)  
                            # have their image updated with their possible values
                    if type(thecell) == Unknown_cell:
                        for z in range(1,10):
                            # this requires 9 blit values and a grid
                            screen.blit(thecell.pencils[z].image, (thecell.pencils[z].xpos,thecell.pencils[z].ypos))
                            screen.blit(pencil_grid_image, (thecell.x_position,thecell.y_position))
                    
                    # if type(thecell) == Known_cell:    #use cell value
                    #     screen.blit(thecell.image, (thecell.x_position,thecell.y_position))
                    # else:       #unknown cells
                        


            screen.blit(grid_image, (0,0))

            # update the message_text based on state values
                    
            if board_clicked == True and game_state == 'Normal':
                if type(board[cell]) == Known_cell:    #if known:
                    message_text = font.render('You cannot change this cell.  Try another', True, (orange_color))
                    row,col,cell,board_clicked,pencil_box = clear_coordinates()
                    # board_clicked = False  #change this b/c its not a valid square
                    entry = 0   #need???
                else:       #Unknown value, changeable
                    entry = 0  #clear out entry values
                    message_text = font.render('You are changing the cell at row: %d / column: %d.  Enter a number from 1 t0 9' % (row,col), True, (orange_color))
            
            if game_state == "Undo":
                message_text = font.render("Press Undo again to revert your changes one by one." , True, (orange_color))

            gen_text = font.render('Press N, then Click on a blank square to enter value', True, (pitch_blue_color))
            gen_text2 = font.render('Press P to add Pencil Values -- U to Undo your guesses -- ESC to quit', True, (pitch_blue_color))
            gen_text3 = font.render('enter 1-9 for values.  0/delete clear guesses ...', True, (pitch_blue_color))
        
            screen.blit(message_text, (3,731))
            screen.blit(gen_text, (3, 750))
            screen.blit(gen_text2, (3, 765))
            screen.blit(gen_text3, (3,780))


            
            side_text1 = font.render('N - Normal', True, (pitch_blue_color))
            screen.blit(side_text1, (730,0))
            side_text2 = font.render('P - Pencil', True, (pitch_blue_color))
            screen.blit(side_text2, (730,40))
            side_text3 = font.render('H - Hint', True, (pitch_blue_color))
            screen.blit(side_text3, (730,80))
            side_text4 = font.render('E - Errors', True, (pitch_blue_color))
            screen.blit(side_text4, (730,120))
            side_text5 = font.render('U - Undo', True, (pitch_blue_color))
            screen.blit(side_text5, (730,160))
            side_text6 = font.render('ESC - Quit', True, (pitch_blue_color))
            screen.blit(side_text6, (730,200))

            any_change = False  #after update, flip back

            pygame.display.update()     #internal function

        clock.tick(60)  #600 makes the fan go crazy

    pygame.quit()

main_state = None
print(__name__)

if __name__ == '__main__':
    # main()
    main_state = main_menu()
    print (main_state)
    if main_state == "Play":
        play()
    else:
        solve()
