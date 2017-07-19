# template for "Stopwatch: The Game"

#___________________________________________________________________________________
# Importing libraries
import simplegui
#___________________________________________________________________________________
# define global variables

time = 0		# Type : Integer. It will represent the time elapsed
Interval = 100	# Type : Integer. It will represent the interval in which visualization will be carried out
Attempts = 0 	# Integer. It will represent the number of attempts of the user
Goals = 0 		# Integer. Number of successful times in which the timer is stopped in the whole second.
Stopped = True # Boolean. Used to indicate that the StopWatch is stopped

#___________________________________________________________________________________


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(time):
    
    # Verifying the parameter
    if time == 0:
        
        # Updating the value to be shown
        S_Time = "0:00.0"
        
    else:
        # Taking the string value of the time
        S_Time = str(time)
        
        # Taking the tenths
        S_Tenths = S_Time[-1]
        
        # Taking the seconds. S_Time[:-1] takes from the penultimate character to the first one
        # With the modulo operator, the seconds of the  value are taken
        if S_Time[:-1] != "":
            S_Seconds = S_Time[:-1]
            
            # Taking the value
            S_Seconds = str(int(S_Seconds)%60)
            
            # Concatenating a zero on the left
            if len(S_Seconds) == 1:
                S_Seconds = "0"+S_Seconds            
        else:
            # Taking the value
            S_Seconds = "00"
        
        # Taking the minutes. S_Time[:-1] takes from the penultimate character to the first one
        # With the division operator, the minutes of the value are taken
        if S_Time[:-1] != "":
            S_Minutes = S_Time[:-1]
            
            # Taking the value
            S_Minutes = str(int(S_Minutes)/60)
   
        else:
            # Taking the value
            S_Minutes = "0"            
            
        # Updating the value
        S_Time = S_Minutes+":"+S_Seconds+"."+S_Tenths
    
    # Giving the value
    return S_Time
    
# define event handlers for buttons; "Start", "Stop", "Reset"
#___________________________________________________________________________________
# Defining the event handler for the "Start" button
def Start_StopWatch():

    # Creating a copy of the global variable
    global Stopped
    
    # The game is running
    Stopped = False
    
    # Calling the function which increments the time
    Time_Increment()
    
    # Starting the timer
    timer.start()
    
#___________________________________________________________________________________
# Defining the event handler for the "Stop" button
def Stop_StopWatch():

    # Creating a copy of the global variables
    global time,Goals,Attempts,Stopped
    
    # Verifying if the game is running. (False is running)
    if Stopped == False:
    
        # Increasing the number of attempts
        Attempts += 1
        
        # Taking the string value of the time
        S_Time = str(time)
            
        # Verifying if the timer was stopped in the whole second
        if S_Time[-1] == "0":
        
            # Increasing the number of the score
            Goals += 1
        
        # Stopping the timer
        timer.stop()
        
        # Reset the variable
        Stopped = True

#___________________________________________________________________________________
# Defining the event handler for the "Reset" button
def Reset_StopWatch():

    # Creating a copy for the original value of the time
    global time,Attempts,Goals,Stopped
    
    # Resetting the variables
    time = 0
    Attempts = 0
    Goals = 0
    
    # Stopping the timer
    timer.stop()

    # Reset the variable
    Stopped = True    
#___________________________________________________________________________________
# define event handler for timer with 0.1 sec interval
def Time_Increment():
    global time
    time += 1

#___________________________________________________________________________________
# define draw handler
def Draw_Time(Canvas):
    Canvas.draw_text(format(time), [65, 90], 30, 'White')
    Canvas.draw_text("Your score: "+str(Goals)+"/"+str(Attempts), [50, 20], 20, 'Green')

#___________________________________________________________________________________
# create frame
frame = simplegui.create_frame("StopWatch The Game",200,200)

#___________________________________________________________________________________
# register event handlers
frame.set_draw_handler(Draw_Time)			# Drawing the value of the time
frame.add_button("Start",Start_StopWatch,50)	# Creating the button for starting the stopwatch
frame.add_button("Stop",Stop_StopWatch,50)	# Creating the button for stopping the stopwatch
frame.add_button("Reset",Reset_StopWatch,50)	# Creating the button for stopping the stopwatch
timer = simplegui.create_timer(Interval, Time_Increment)

#___________________________________________________________________________________
# start frame

frame.start()

# Please remember to review the grading rubric