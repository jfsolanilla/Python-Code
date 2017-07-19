# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

Angular_Steps = 0.1		# Steps in which the angular velocity is increased
Accelerate_Index = 3	# Index to get the image in which the thrusters are on
Default_Ship = [45,45]	# Position on the source image where the default ship is located
Forward_Vector = []		# Vector which points in the direction the ship is facing

# Helper function to correct the position of an "invisible" object
def correct_position(position):
    
    # Parameters: position : List. Defines the current position 
    # of the object on the canvas
    
    # Updating the horizontal position of the object taking into account the size of the canvas
    if position[0] > WIDTH or position[0] < WIDTH:
        position[0] = position[0]%WIDTH	# Updating the horizontal position of the object so that it is wrapped by the limits of the canvas
        
    # Updating the vertical position of the object taking into account the size of the canvas
    if position[1] > HEIGHT or position[1] < HEIGHT:
        position[1] = position[1]%HEIGHT	# Updating the vertical position of the object so that it is wrapped by the limits of the canvas

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo(Default_Ship, [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        # Drawing the image of the ship
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)

    #_______________________________________________________________________________________________
    def update(self):
        global Forward_Vector
        
        # Updating the position of the ship by using its velocity
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # Updating the angle of the ship by using its angular velocity
        self.angle += self.angle_vel
        
        # Vector which points in the direction the ship is facing
        Forward_Vector = angle_to_vector(self.angle)
        
        # Updating the velocity of the ship in function of the friction of the space
        self.vel[0] *= (1 - 0.01)
        self.vel[1] *= (1 - 0.01)		
        
        # If the engines of the ship are turned on, the velocity will be updated
        if self.thrust:
        
            # Updating the velocity of the ship
            self.vel[0] += Forward_Vector[0]
            self.vel[1] += Forward_Vector[1]
            
        # Updating the horizontal and vertical position of the ship taking into account the size of the canvas
        correct_position(self.pos)
                    
    #_______________________________________________________________________________________________  
    # Increasing the angular velocity in the clockwise direction
    def clockwise_velocity(self):
        global Angular_Steps	# Defining the scope of the angular steps
        self.angle_vel += Angular_Steps	# Modifying the angular velocity
    
    #_______________________________________________________________________________________________
    # Increasing the angular velocity in the counter-clockwise direction
    def counter_clockwise_velocity(self):
        global Angular_Steps	# Defining the scope of the angular steps
        self.angle_vel -= Angular_Steps	# Modifying the angular velocity

    #_______________________________________________________________________________________________
    # Thrusters on
    def thrusters_on(self):
        global Accelerate_Index,Default_Ship # Scope of the globals
        
        if not(self.thrust):
            self.thrust = True	# Turning on the thrusters
            ship_info.center[0] = Default_Ship[0]*Accelerate_Index	# Updating the image of the ship
            ship_thrust_sound.play()	# Sound of the engines of the ship
                        
#_______________________________________________________________________________________________
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        # Drawing the image of the rocks
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)		
    
    def update(self):
        global Angular_Steps
        
        # Updating the position of the rock by using its velocity
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        # Updating the velocity of the rock
        self.vel = [random.randrange(10,WIDTH),random.randrange(10,HEIGHT/2)]
        
        # Creating the rotation for the rock in angular steps
        self.angle += Angular_Steps
    
        # Updating the horizontal and vertical position of the rock taking into account the size of the canvas
        correct_position(self.pos)
        
#_______________________________________________________________________________________________
def draw(canvas):
    global time
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
            
#_______________________________________________________________________________________________
# timer handler that spawns a rock    
def rock_spawner():
    pass
    
#_______________________________________________________________________________________________
# KEYDOWN EVENT HANDLER
def keydown(key):
    global Key_Inputs

    for I_Key_Events in Key_Inputs:	# Loop over the key inputs
        if key == simplegui.KEY_MAP[I_Key_Events]:	# Verifying if the key pressed corresponds with the key map
            Key_Inputs[I_Key_Events]()	# Calling the method assigned

#_______________________________________________________________________________________________
# KEYUP EVENT HANDLER
def keyup(key):
    global Accelerate_Index
    
    # The angular velocity is zero
    my_ship.angle_vel = 0
    
    # If the engines of the ship are turned on
    if my_ship.thrust:

        my_ship.thrust = False	# Turning off the thrusters
        ship_info.center[0] = Default_Ship[0]/Accelerate_Index	# Updating the image of the ship
        ship_thrust_sound.rewind()	# The thrusters are turned off			
    
#_______________________________________________________________________________________________

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0,0], 10, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# Global for the key inputs
Key_Inputs = {"right" : my_ship.clockwise_velocity,"left" : my_ship.counter_clockwise_velocity,"up":my_ship.thrusters_on}

# register handlers
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()