# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

# Defining libraries
import random
import simplegui
import math

# Defining global variables
Secret_Number = 0	# Number that will be guessed by the user
Upper_Limit = 0			# Upper limit of the random range 
Limit_of_Guesses = 0# Limit of guesses available

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    
    # Defining the value of the secret number
    global Secret_Number
    Secret_Number = random.randrange(0,Upper_Limit)

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    
    # Assigning the upper value
    global Upper_Limit,Limit_of_Guesses
    Upper_Limit = 100
    Limit_of_Guesses = math.ceil(math.log(Upper_Limit + 1,2))

    # Welcome message of a new game
    print "                                                                           "
    print "Guess the number!!! This game will be in the 0-100 range. You will have",Limit_of_Guesses,"chances. Good luck!!!"
    
    # Running a new game
    new_game()
    
def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    
    # Assigning the upper value
    global Upper_Limit,Limit_of_Guesses
    Upper_Limit = 1000
    Limit_of_Guesses = math.ceil(math.log(Upper_Limit + 1,2))
    
    # Welcome message of a new game
    print "                                                                           "
    print "Guess the number!!! This game will be in the 0-1000 range. You will have",Limit_of_Guesses,"chances. Good luck!!!"
    
    # Running a new game
    new_game()
    
def input_guess(guess):
    # main game logic goes here
    
    # Updating the value in order to do comparisons between integers
    guess = int(guess)
    
    # Defining a copy of the variable
    global Limit_of_Guesses,Upper_Limit
    
     #________________________________________________________________________________
     # Verifying if the number is correct
     
    # Printing the guess of the user
    print "                                                                           "
    print "Guess was",guess
        
    # The guess is higher than the secret number
    if Secret_Number > guess:
    
        # Updating the limit of guesses
        Limit_of_Guesses -= 1	
        
        # Printing the clue
        print "Higher"
        print Limit_of_Guesses,"guesses remaining"
            
    # The guess is lower than the secret number
    elif Secret_Number < guess:
    
        # Updating the limit of guesses
        Limit_of_Guesses -= 1	
        
        # Printing the clue	
        print "Lower"
        print Limit_of_Guesses,"guesses remaining"
            
    # The guess is equal than the secret number
    else:
        
        print "Correct"
                
        # Defining the number of guesses
        Limit_of_Guesses = math.ceil(math.log(Upper_Limit + 1,2))
        
        # The user have won
        print "                                                                           "
        print "You have won!!! A new game in the range 0 -",Upper_Limit," have started. You will have",Limit_of_Guesses,"chances. Good luck!!!"
		
        # Starting a new game
        new_game()
        
        return			
        
  #________________________________________________________________________________
    
    # Verifying the limit of guesses
    if Limit_of_Guesses == 0:
           
        # Defining the number of guesses
        Limit_of_Guesses = math.ceil(math.log(Upper_Limit + 1,2))
    
       # The user have lost
        print "                                                                           "
        print "You have lost, the correct answer was",Secret_Number,". Don't Worry!!! A new game in the range 0 -",Upper_Limit," have started. You will have",Limit_of_Guesses,"chances. Good luck!!!"
     
        # Starting a new game
        new_game()
        
        return
    
    #________________________________________________________________________________
        
# create frame
frame = simplegui.create_frame('Guess the Number', 300,300)

#________________________________________________________________________________
# register event handlers for control elements and start frame

# Adding an input
frame.add_input("Enter the Guess",input_guess,70)

# Adding two buttons  in order to start a new game
frame.add_button("Range: 0 - 100",range100)		# Range 0 - 100
frame.add_button("Range: 0 - 1000",range1000)	# Range 0 - 1000

# Starts the frame
frame.start
#________________________________________________________________________________
# STARTING THE FIRST GAME. THIS GAME STARTS IN THE 0-100 RANGE

# Defining the upper limit
Upper_Limit = 100

# Defining the limit of guesses
Limit_of_Guesses = math.ceil(math.log(Upper_Limit + 1,2))

# Welcome message
print "Guess the number!!! The first game will start in the 0-100 range. You will have",Limit_of_Guesses,"chances. Good luck!!!"

# Running the first game
new_game()

# always remember to check your completed program against the grading rubric