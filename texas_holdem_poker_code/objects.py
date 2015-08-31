from random import shuffle
import sys
#citation: part of code from: https://github.com/omarshammas/pyPoker-Texas-HoldEm

class Player:

    def __init__(self, money, position, identity, id, state, chip, hand):

        self.position = position # the position on the table, start from 0 to number_of_player - 1
        self.identity = identity # "dealer","small blind", "big blind", "normal"
        self.money = money  #the money of the player has
        self.id = id #can be equal to "human" or "computer"
        self.state = state #"playing","out","all in", state is the state of player during the game
        self.chip = chip # the chip this game the player has already bet.
        self.hand = hand # the hand of each players( 2 cards)
        self.sidepot = 0
    
    def get_position(self):
        return self.position

    def get_side(self):
        return self.sidepot

    def change_side(self,sidepot):
        self.sidepot = sidepot

    def get_chip(self):
        return self.chip

    def get_identity(self):
        return self.identity

    def get_money(self):
        return self.money

    def get_id(self):
        return self.id

    def get_hand(self):
        return self.hand

    def get_state(self):
        return self.state

    def change_position(self,num,number_of_players):
        self.position = (self.position + num) % number_of_players

    def change_money(self, num):
        self.money = self.money + num
        if num == 0:
            self.money = 0
        if self.money < 0:
            print self.money
            print self.id," ", self.identity,"do not have enough money"
            self.state = "out"

    def change_identity(self, new_identity):
        self.identity = new_identity

    def change_chip(self, raise_money):
        if raise_money == 0:#reset the chip
            self.chip = 0
        else:
            self.chip += raise_money

    def change_hand(self, new_hand,flag):#[[],[]]
        if flag == 0:
            self.hand = []
        else:
            if len(self.hand) == 2:
                self.hand = []
                self.hand.append(new_hand)

            else:
                self.hand.append(new_hand)
    def change_state(self, new_state):
        self.state = new_state

class Card:
    def __init__(self, symbol, value):
        self.symbol = symbol
        self.value = value

    def __cmp__(self, other):
        if self.value < other.value:
            return -1
        elif self.value == other.value:
            return 0
        return 1

    def __str__(self):
        text = ""
        if self.value < 0:
            return "Joker"
        elif self.value == 11:
            text = "J"
        elif self.value == 12:
            text = "Q"
        elif self.value == 13:
            text = "K"
        elif self.value == 14:
            text = "A"
        else:
            text = str(self.value)





        if self.symbol == 0:    #D-Diamonds
            text += "D"
        elif self.symbol == 1:  #H-Hearts
            text += "H"
        elif self.symbol == 2:  #S-Spade
            text += "S"
        else:                   #C-Clubs
            text += "C"

        return text

class deck:

    #Initializes the deck
    def __init__(self, ):
        self.cards = []
        self.inplay = []

        for symbol in range(0,4):
            for value in range (2,15):
                self.cards.append( Card(symbol, value) )


        self.total_cards = 52

    #Shuffles the deck
    def shuffle(self):
        self.cards.extend( self.inplay )
        self.inplay = []
        shuffle( self.cards )

    #Cuts the deck by the amount specified
    #Returns true if the deck was cut successfully and false otherwise
    def cut(self, amount):
        if not amount or amount < 0 or amount >= len(self.cards):
            return False #returns false if cutting by a negative number or more cards than in the deck

        temp = []
        for i in range(0,amount):
            temp.append( self.cards.pop(0) )
        self.cards.extend(temp)
        return True

    #Returns a data dictionary
    def deal(self, number_of_cards):

        if(number_of_cards > len(self.cards) ):
            return False #Returns false if there are insufficient cards

        inplay = []
        for i in range(0, number_of_cards):
            inplay.append( self.cards.pop(0) )

        self.inplay.extend(inplay)
        return inplay

    def cards_left(self):
        return len(self.cards)
