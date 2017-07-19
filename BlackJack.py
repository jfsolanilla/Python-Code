# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome_player = "Hit or Stand?"
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

#___________________________________________________________________________________________________
# Helper function to represent a group of cards
def representation_cards(List_Cards):

        # Local variables
        S_Card = " "
        
        # Making the representation of a hand
        for I_Cards in range(len(List_Cards)):
            S_Card += str(List_Cards[I_Cards]) + " "
        return "Hand contains" + S_Card	# return a string representation of the group of cards	
#___________________________________________________________________________________________________
# Helper function to represent a new card in the hand
        
def take_card(Aux_Hand):

    # Defining the scope of globals
    global General_Deck
    
    # Verifying the value of the hand
    if Aux_Hand.Value <= 21:
        Aux_Hand.add_card(Deck.deal_card(General_Deck))
        
#___________________________________________________________________________________________________
# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
#___________________________________________________________________________________________________
        
# define hand class
class Hand:
    def __init__(self):
        self.Cards = []	# Create Hand object
        self.Value = 0	# Value of the hand
        self.Busted = False	# It indicates that the gamer has busted

    def __str__(self):
    
        # String representation of a hand
        return representation_cards(self.Cards)

    def length(self):
        # Length of the list
        return len(self.Cards)
        
    def add_card(self, card):
        self.Cards.append(card)	# add a card object to a hand
        
        # Computing the value of the cards
        self.Value = self.get_value()

        # self.Value > 21. It indicates that the gamer has busted		
        if self.Value > 21:
           self.Busted = True
    #___________________________________________________________________________________________________		
    def get_value(self):
    
        # Locals
        I_Total_Value = 0	# Type : Integer. It represents the value of the hand
        B_Ace = False			# Type : Boolean. If this flag is true, it means that there is an Ace in the hand
        
        # Loop to compute the value of the hand
        for S_Cards in self.Cards:
            
            # Changing the type of the data (Type Hand to String)
            S_Cards = str(S_Cards)
            
            # Accumulating the total
            I_Total_Value += VALUES[S_Cards[-1]]
            
            # S_Cards[-1] == "A". It means that the hand has an Ace
            if S_Cards[-1] == "A":
                B_Ace = True
         
        # Verifying if the player have not busted
        if B_Ace and I_Total_Value + 10 <= 21:
        
            # If the player have not busted, then 10 will be added to the total
            return I_Total_Value + 10
        else:
            # The computation will be done without adding ten more
            return I_Total_Value
            
    #___________________________________________________________________________________________________
   
    def draw(self, canvas, pos):
        
        # Locals
        I_Separation = 0	# Type : Integer. It represents the separation between cards
        
        # Drawing a hand on the canvas
        for S_Cards in self.Cards:
        
            # Drawing the hand on the canvas
            Card.draw(S_Cards,canvas,[pos[0] + I_Separation, pos[1]])
            
            # Adding the separation to the local variable
            I_Separation += CARD_SIZE[0] + 30

#___________________________________________________________________________________________________

# define deck class 
class Deck:
    def __init__(self):
        global SUITS,RANKS
        
        # create a Deck object
        self.Deck_Cards = [(Card(I_Suits,I_Ranks)) for I_Suits in SUITS for I_Ranks in RANKS]

    def shuffle(self):
        # Shuffling the deck
        random.shuffle(self.Deck_Cards)
        
    def deal_card(self):
            
        # Dealing the last card from the deck
        return (self.Deck_Cards).pop(-1)
                
    def __str__(self):
            
        # String representation of the deck
        return representation_cards(self.Deck_Cards)

#___________________________________________________________________________________________________

#define event handlers for buttons
def deal():
    global outcome, in_play, General_Deck, Player_Hand, Dealer_Hand
     
    # Shuffling the deck
    General_Deck.shuffle()
    
    # Dealing a card to the player
    Player_Hand.add_card(Deck.deal_card(General_Deck))

    # Dealing a card to the dealer
    Dealer_Hand.add_card(Deck.deal_card(General_Deck))
                        
    in_play = True
#___________________________________________________________________________________________________

def hit():
    
    # Taking a new card
    take_card(Player_Hand)
    
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
#___________________________________________________________________________________________________

def stand():
    
    # Player_Hand.Busted. Indicates that the user has busted
    if Player_Hand.Busted:
    
		# Updating the message used for the player
        outcome_player = "Remember that you have busted!!!"
    else:
        
        # The dealer will receive cards until get to 17
        while Dealer_Hand.Value < 17:
        
            # Taking a new card
            take_card(Dealer_Hand)

	#___________________________________________________________________________________________________			
    # Verifying the winner
    
    # Player wins when she has not busted and her value is greater than dealer's value.
    # Player could also win when she has not busted and dealer's value is greater than player's, but dealer has busted.
    if not(Player_Hand.Busted) and ((Dealer_Hand.Value <  Player_Hand.Value) or (Dealer_Hand.Value >= Player_Hand.Value and Dealer_Hand.Busted)):
    
        print "Player has won. Score of the dealer: " + str(Dealer_Hand.Value) + ". Score of the player: " + str(Player_Hand.Value)
        print "Dealers Hand: " + str(Dealer_Hand) + "Players Hand: " + str(Player_Hand)
        
    # Dealer wins when she has not busted and her value is greater than player's value.
    # Dealer could also win when she has not busted and player's value is greater than dealer's, but player has busted.
    elif not(Dealer_Hand.Busted) and ((Dealer_Hand.Value >= Player_Hand.Value) or (Dealer_Hand.Value <  Player_Hand.Value and Player_Hand.Busted)):
    
        print "Dealer has won. Score of the Dealer: " + str(Dealer_Hand.Value) + ". Score of the player: " + str(Player_Hand.Value)
        print "Dealers Hand: " + str(Dealer_Hand) + "Players Hand: " + str(Player_Hand)
        
    else:
        print "There is no winner"
        print "Score of the dealer: " + str(Dealer_Hand.Value) + ". Score of the player: " + str(Player_Hand.Value)
        
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score
#___________________________________________________________________________________________________
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    Player_Hand.draw(canvas, [30, 400])
    canvas.draw_text("Blackjack! Welcome to Las Vegas!",(15,40),40,"Yellow")
    canvas.draw_text("Player",(30,380),40,"Yellow")
    canvas.draw_text(outcome_player,(200,380),40,"Yellow")
#___________________________________________________________________________________________________

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

#___________________________________________________________________________________________________
# Player's hand (list of objects type card)
Player_Hand = Hand()

# Dealer's hand (list of objects type card)
Dealer_Hand = Hand()

# Shuffling the general deck
General_Deck = Deck()
#___________________________________________________________________________________________________

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric