import pygame

#this is the functiont that can read in the raw board settings
#raw board is an array of 9 arrays with 9 tuples each
from board1_raw import rawboard

class Cell():
    #define the playing cell.  there are 81 of these in an 9x9 soduko board
    def __init__(self,row,col,value,answer=None):
        # self.start = value  #or is this in the subclass...
        # self.anser = 
        self.row = row
        self.col = col
        #  self.inner = 0  #compute thie
        self.pencils = {}  #{} will object create this and set here

        self.guess = None       #blank to start
        self.value = value      #given in start cube
        self.answer = answer    #if loaded in answers, used for hints

        self.name = "r%dc%d" % (row,col)

        rowbox = int((row-1)//3)
        colbox = int((col-1)//3)
        self.inner = (rowbox *3 )+ colbox+ 1

        self.x_position = (row-1) * 81
        self.y_position = (col-1) * 81       

    def change_cell_image(self,value):
        #not tested yet
        self.image = pygame.image.load('numbers/%d_background_transparent.png' % value).convert_alpha()
        # self.image = pygame.image.load('numbers/%d_transparent_number.png' % value).convert_alpha()

class Known_cell(Cell):
    def __init__(self,row,col,value,answer):
        super().__init__(row,col,value,answer)
        self.answer = answer  
        #known cells don't need pencils or possibles
        self.possibles = {}  #empty    
        self.image = pygame.image.load('numbers/%d_background_transparent.png' % answer).convert_alpha()
        # self.image = pygame.image.load('numbers/%d_transparent_number.png' % value).convert_alpha()
    

class Unknown_cell(Cell):
    def __init__(self,row,col,value,answer=None):
        super().__init__(row,col,value,answer)
        self.answer = answer
        self.value = 0
        self.pencil = {1:False,2:False,3:False,4:False,5:False,6:False,7:False,8:False,9:False}
        self.possibles = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
        #change this to a null image
        self.image = None

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


def main():

    # declare the size of the canvas
    width = 780
    height = 780

    # define some colors
    blue_color = (97, 159, 182)  #background color
    background_color = (244,237,221)
    blue_color = (97, 159, 182)  #sky_blue
    red_color = (255,0,0)
    pitch_blue_color = (83,94,126)
    red_color = (255,0,0)
    green_color = (89,162,134)
    orange_color = (224,95,20)

    pygame.init()
    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption('Soduko')
    clock = pygame.time.Clock()

    # Game initialization
    grid_image = pygame.image.load('numbers/big_grid_lines.png').convert_alpha()
   
    # pencil_image1 = pygame.image.load('numbers/1_pencil.png').convert_alpha()
    # pencil_image2 = pygame.image.load('numbers/2_pencil.png').convert_alpha()
    # pencil_image3 = pygame.image.load('numbers/3_pencil.png').convert_alpha()
    # pencil_image4 = pygame.image.load('numbers/4_pencil.png').convert_alpha()
    # pencil_image5 = pygame.image.load('numbers/5_pencil.png').convert_alpha()
    # pencil_image6 = pygame.image.load('numbers/6_pencil.png').convert_alpha()
    # pencil_image7 = pygame.image.load('numbers/7_pencil.png').convert_alpha()
    # pencil_image8 = pygame.image.load('numbers/8_pencil.png').convert_alpha()
    # pencil_image9 = pygame.image.load('numbers/9_pencil.png').convert_alpha()
    
    stop_game = False

    #create data
    #do this after you set images, although I guess this could be done inside..
    board = create_board(rawboard)
    
    for each in board.values():
        print(each.answer)
        
    #these print to the terminalo
    # print_grid(board,"value")
    # print_grid(board,"answer")
    # print_grid(board,"inner")

    #message text
    #this is for when a user does something - the message changes
    font = pygame.font.Font(None, 25)
    message_text = font.render('', True, (orange_color))            

    while not stop_game:
        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.QUIT:
                stop_game = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('mouse down at %d, %d' % event.pos)  #to terminal
                #change the value of the message text
                message_text = font.render('Enter a number from 1 t0 9', True, (orange_color))
                #change the text if they press in a spot
                #tell them what to do

            if event.type == pygame.KEYDOWN:
                print('key down %r' % event.key)

        # Game logic

        # Draw background
        screen.fill(background_color)

        # Game display

        #set the blits for all known numbers
        for i in range(1,10):
            for j in range(1,10):
                cell = "r%dc%d" % (i,j)
                if board[cell].image != None:
                    #need to add a test for GUESS...
                    screen.blit(board[cell].image, (board[cell].x_position,board[cell].y_position))

        screen.blit(grid_image, (0,0))
        # screen.blit(image6, (250, 250))
        # screen.blit(pencil_image9, (600,600))


        # font = pygame.font.Font(None, 25)
        # text_new = font.render('Enter a number from 1 t0 9', True, (red_color))
        # update the message_text
        screen.blit(message_text, (3,731))
           
            # pygame_popup_window()
            # value = input()
            # print(value)

        font = pygame.font.Font(None, 25)
        gen_text = font.render('Click or type and see events in the terminal', True, (pitch_blue_color))
        screen.blit(gen_text, (3, 750))


        # pygame.display.update()


        pygame.display.update()

        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
