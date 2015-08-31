from poker import Poker
import sys,random
from objects import Player
from bet import *
#*********************************************************
#******************determine_winner***********************
#*********************************************************

#results = lst of [score,kicker]
#kicker = lst of the final hand for each player. [hand(in des order)]
##score:
# 0 : high card;
# 1 : pair
# 2 : 2 pair
# 3 : 3 of a kind
# 4 : straight
# 5 : flush
# 6 : full house
# 7 : four of a kind
# 8 : straght flush
# 9 : royal flush

#bet_value =  the chips that each players in the final round gives in total
#total_bet = pot
#community cards: the community cards
def determine_winner(results,players,bet_value, total_bet,community_cards):
    '''
        The function returns the winner of the game.
        It disperse the pot to players too.
    '''
    print "status:"
    for i in range(len(players)):
        print "player ",i,":",players[i].get_state()

    winner_id = []
    max_res = [-1,[]]
    playing_gamer = [] # still "alive" players
    #find the winners of the game
    for idx in range(len(results)):
        if players[idx].get_state() == "out":
            continue
        playing_gamer.append(idx)
        if results[idx][0] > max_res[0]:
            max_res[0] = results[idx][0]
            max_res[1] = results[idx][1]
            winner_id = [idx]
        elif results[idx][0] == max_res[0]:
            flag = 0
            for j in range(len(max_res[1])):
                if max_res[1][j] < results[idx][1][j]:
                    max_res[1] = results[idx][1]
                    winner_id = [idx]
                    flag = -1
                    break
                if max_res[1][j] > results[idx][1][j]:
                    flag = 1
                    break
            if flag == 0:
                winner_id.append(idx)

    print "WINNER(S):"
    for id in winner_id:
        print players[id].get_id()," player ", players[id].get_position()," wins!!"
    print "=========================="

    #firstly return the bets that the winners bet to the winners
    num_of_winners = len(winner_id)
    money_added = 0
    for idx in winner_id:
        money_added = money_added + players[idx].get_chip()
        players[idx].change_money(players[idx].get_chip())

    #secondly the winners share others' chips
    pot = total_bet[0] - money_added
    money_added = 0
    for idx in winner_id:
        tmp = 0
        if players[idx].get_state() == "all in":
            tmp = int((pot * players[idx].get_side())/(total_bet[0] * num_of_winners))
            money_added = money_added+tmp
            players[idx].change_money(tmp)
        else:
            tmp = int(pot/num_of_winners)
            players[idx].change_money(tmp)
            money_added = money_added+tmp

    #thirdly, if chips left, dispense the left chips to other players
    left = pot - money_added
    if left > 0:
        num_of_losers = len(players) - len(winner_id)
        piece_left = int(1.0 * left / num_of_losers)
        for idx in range((len(players))):
            if idx not in winner_id:
                players[idx].change_money(piece_left)

    return winner_id

#*********************************************************
#**********************--showdown---**********************
#*********************************************************

#funciton that convert card symbols from english word to unicode
diamond = u'\u2666'
spade = u'\u2660'
heart = u'\u2665'
club = u'\u2663'

def convert(text):
        text1 = ""
        for char in text:
                if char == "D":
                        text1 = text1 + diamond
                elif char == "H":
                        text1 = text1 + heart
                elif char == "S":
                        text1 = text1 + spade
                elif char == "C":
                        text1 = text1 + club
                else:
                        text1 = text1 + char
        print text1

def showdown(poker,players,bet_value, total_bet,community_cards):
    while(len(community_cards) < 5):
        card = poker[0].getOne()
        if not card:
            sys.exit("*** ERROR ***: Insufficient cards to distribute.")
        community_cards.extend( card )

    #print " Community Cards"

    text = "community cards - "
    for card in community_cards:
        text += str(card) + "  "
    convert(text)
    #print text
    #-------------------------------------------------
    print "6. Determining Score"
    #try:
    results = poker[0].determine_score(community_cards, players_hands)
    #except:
    #    sys.exit("*** ERROR ***: Problem determining the score.")

    print "7. Determining Winner"

    winner = determine_winner(results,players, bet_value, total_bet, community_cards)

    #sys.exit("*** ERROR ***: Problem determining the winner.")

    #Checks to see if the hand has ended in tie and displays the appropriate message
    tie = True
    try:
        len(winner)
    except:
        tie = False

    if not tie:
        counter = 0
        print "-------- Winner has Been Determined --------"
        for hand in players_hands:
            if counter == winner:
                text = "Winner $$ "
            else:
                text = "Loser  -- "
            for c in hand:
                text += str(c) + "  "

            text += " --- " + poker[0].name_of_hand(results[counter][0])
            counter += 1
            convert(text)
    else:
        counter = 0
        print "--------- Tie has Been Determined --------"
        for hand in players_hands:
            if counter in winner:
                text = "Winner ** "
            else:
                text = "Loser  -- "
            for c in hand:
                text += str(c) + "  "

            text += " --- " + poker[0].name_of_hand(results[counter][0])
            counter += 1
            convert(text)
    print"press any key to continue the new game"
    raw_input()
#*********************************************************
#********************print_identity***********************
#*********************************************************
# print out each player's identity
def print_identity(players):
    print "--------------------------------------------------"
    for i in range(len(players)):
        if players[i].get_id() == "human":
            #print "--------------------------------------------------"
            print "* you are player", i, ", identity is ",players[i].get_identity(),", ", players[i].get_state()
            #print "--------------------------------------------------"
        else:
            print "AI player", i, ", identity is",players[i].get_identity(),", ", players[i].get_state()
    print "--------------------------------------------------"


#---------------------------------------------------------------
    # begin next round of the game, change the identity on the table,the players will take turns being the dealer
    #the number below means the position of each player on the table
#renew the information of each players and prepare for next match
def renew_round(players, dealer,round,poker):
    number_players = 0
    for i in range(len(players)):
        print "current player's money:",players[i].get_money()
        if  players[i].get_money() > 0:
            print "money"
            players[i].change_state("playing")
            number_players += 1
        else:
            players[i].change_state("out")
        players[i].change_chip(0)
        players_hands = poker[0].distribute()
        #players[i].change_hand(players_hands[0][0],0)
    # check if there are enough players qualified to play the game
    if number_players == 1:
        sys.exit("*** ERROR ***: only 1 player left, game over.")
    print "num of players:",number_players
    dealer = (dealer + 1) % number_players

    for i in range(len(players)):
        if len(players) == 2:
            if players[i].position == dealer:
                if players[i].state == "playing":
                    players[i].change_identity("small blind")
                    if players[(i+1) % 2].get_state() == "playing":
                        players[(i+1) % 2].change_identity("big blind")
                        break
                    else:
                        sys.exit(" only one player left, game over!")

        elif len(players) > 2:
            if players[i].position == dealer:
                if players[i].state == "playing":
                    players[i].change_identity("normal")
                else:
                    # for this part, we need to ignore the players who do not have enough money

                    while(1):
                        if players[i].state == "playing":
                            players[i].change_identity("normal")
                            break
                        else:
                            i = (i + 1) % len(players)
                    while(1):
                        if players[i].state == "playing":
                            players[i].change_identity("small blind")
                            break
                        else:
                            i = (i + 1) % len(players)
                    while(1):
                        if players[i].state == "playing":
                            players[i].change_identity("big blind")
                            break
                        else:
                            i = (i + 1) % len(players)
                    break
    number = 0
    for i in range(len(players)):
        if players[i].state == "playing":
            number += 1
    poker[0].change_num_of_players(number)
    round[0] += 1
    #----------------END NOTATION FOR USER-------------------------
    number_of_players = 0
    for i in range(len(players)):
        if players[i].get_state() == "playing":
            number_of_players += 1

    if number_of_players <= 1:
        print "game over, not enough player"
    if round[0] > round_amount:
        print "**************************************************"
        #print "**************************************************"
        print "game over, all the round has been finished"
        for i in range(len(players)):
            print "player ", i, "money left:", players[i].get_money()
        print "**************************************************"
        #print "**************************************************"
#******************************************************
#******************************************************
#****************** main function *********************
#******************************************************
#******************************************************
debug = False    #Set to True to see the debug statements
#-------input judgement part---------------------------
k = []
k = (raw_input("Enter number of players: "))
while(not k.isdigit()):
    print "error,you must input a number,the number of players must be between 2 and 20"

    k = raw_input("Enter number of players: ")
k = int(k)
while(k < 2 or k > 20 ):
    print ""
    print "error,you must input a number,the number of players must be between 2 and 20"
    k = raw_input("Enter number of players: ")
    if k.isdigit():
        k = int(k)
number_of_players = k
#-------------------------------------------------------
#-------input judgement part---------------------------
k = []
k = (raw_input("Enter initial money of each players(as least 20 dollars):"))
while(not k.isdigit()):
    print "error,you must input a number,the number of each round must be as least 20 dollars"

    k = raw_input("Enter number of each round: ")
k = int(k)
while(k < 20 ):
    print ""
    print "error,you must input a number,the number of each round must be as least 20 dollars"
    k = raw_input("Enter number of each round: ")
    if k.isdigit():
        k = int(k)
money_of_each_player = float(k)
#--------------------------------------------------------------
poker = []
poker.append(Poker(number_of_players, money_of_each_player,debug))
#-------input judgement part----------------------------------
k = []
k = (raw_input("Enter round of game:"))
while(not k.isdigit()):
    print "error,you must input a number,the number of players at least be 1"

    k = raw_input("Enter round of game: ")
k = int(k)
while(k < 1 ):
    print ""
    print "error,you must input a number,the number of players at least be 1"
    k = raw_input("Enter round of game: ")
    if k.isdigit():
        k = int(k)
round_amount = k
#---------------------------------
round = []
round.append(1)
print "the game is Limit Texas, good luck: "


small_blind_money = money_of_each_player / 20
big_blind_money = 2 * small_blind_money

#-----------------
# initialize each player
#players is a list contains all the players
players = []
#choose which player in the players list will be the dealer, small blind, big blind
dealer = random.randrange(0, number_of_players)
small_blind = (dealer + 1) % number_of_players
big_blind = (dealer + 2) % number_of_players
#choose which player will be the human
human = random.randrange(0, number_of_players)

for i in range(0,number_of_players) :
    if number_of_players > 2:
        if i == dealer:
            if i == human:
                player = Player(money_of_each_player, i, "normal", "human","playing", 0.0,[])
            else:
                player = Player(money_of_each_player, i, "normal", "computer","playing", 0.0,[])

        elif i == small_blind:
            if i == human:
                player = Player(money_of_each_player, i, "small blind", "human","playing", 0.0,[])
            else:
                player = Player(money_of_each_player, i, "small blind", "computer","playing", 0.0,[])

        elif i == big_blind:
            if i == human:
                player = Player(money_of_each_player, i, "big blind", "human","playing", 0.0,[])
            else:
                player = Player(money_of_each_player, i, "big blind", "computer","playing", 0.0,[])

        else:
            if i == human:
                player = Player(money_of_each_player, i, "normal", "human","playing", 0.0,[])
            else:
                player = Player(money_of_each_player, i, "normal", "computer","playing", 0.0,[])
    elif number_of_players == 2:
        if i == small_blind:
            if i == human:
                player = Player(money_of_each_player, i, "small blind", "human","playing", 0.0,[])
            else:
                player = Player(money_of_each_player, i, "small blind", "computer","playing", 0.0,[])
        elif i == big_blind:
            if i == human:
                player = Player(money_of_each_player, i, "big blind", "human","playing", 0.0,[])
            else:
                player = Player(money_of_each_player, i, "big blind", "computer","playing", 0.0,[])

    else:
        sys.exit("*** ERROR ***.")
    players.append(player)
#initialization end
#------------
    bet_value = []
    total_bet = []
    bet_value.append(0.0)       # bet_value is the money of nowadays' bet
    total_bet.append(0.0)


# begin to run the game, stop the game until only one player has enough money or all the rounds come to the end
while(number_of_players > 1 and round[0] < (round_amount + 1)):
         # the total money that all the players have bet.
    if_win = 1   # judge whether there is a winner in this round, 1 means no winner, 0 means yes
    bet_value[0] = 0.0       # bet_value is the money of nowadays' bet
    total_bet[0] = 0.0
    community_cards = []
    #print which round the game is
    print ""
    print "**************************************************"
    print "round", round[0]

    if not poker[0]:
        sys.exit("*** ERROR ***: Invalid number of players. It must be between 2 and 22.")

    print "Shuffling..."
    poker[0].shuffle()
    #print ""

    print "Cutting..."
    if not poker[0].cut(random.randint(1, 51)):
        #Cannot cut 0, or the number of cards in the deck
        sys.exit("*** ERROR ***: Invalid amount entered to cut the deck.")

    print "Distributing..."
    players_hands = poker[0].distribute()
    if not players_hands:
        sys.exit("*** ERROR ***: Insufficient cards to distribute.")
    #print ""
    #distribute the 2 cards to each player, and store the 2 cards to each "player class"
    for i in range(len(players_hands)):
        for j in range(0, 2):
            players[i].change_hand(players_hands[i][j],1)#[[],[]]

    #print "Hands:"

    #pre-flop bet round, round 1
    print "**************************************************"
    print "1.Pre-Flop Round"
    print_identity(players)
    print "small blind:",small_blind_money,",big blind: ",big_blind_money
    #print ""
    # print out the human player's first two hands
    for i in range(len(players_hands)):
        if players[i].get_id() == "human":
            hand = players[i].get_hand()
            text = "your hand - "
            for card in hand:
                text += str(card) + "  "
            convert(text)
            print "--------------------------------------------------"
            #print text
    #print ""
    if_win = bet(1, small_blind_money, big_blind_money, players, bet_value, total_bet, community_cards)

    if if_win == 0:  # if there is already a winner, end this round
        renew_round(players, dealer,round,poker)

        continue
    if if_win == 2:
        showdown(poker,players,bet_value, total_bet,community_cards)
        renew_round(players, dealer, round,poker)
        continue

    #print "**************************************************"
    #Gets and prints the community cards

    #flop round bet, round 2
    print "**************************************************"
    print "2.Flop Round"
    print_identity(players)
    #print out the human player's hand
    for i in range(len(players_hands)):
        if players[i].get_id() == "human":
            hand = players[i].get_hand()
            text = "your hand - "
            for card in hand:
                text += str(card) + "  "
            convert(text)
            #print text

    card = poker[0].getFlop()
    if not card:
        sys.exit("*** ERROR ***: Insufficient cards to distribute.")
    community_cards = card
    #print " Community Cards"

    text = "community cards - "
    for card in community_cards:
        text += str(card) + "  "
    convert(text)
    print "--------------------------------------------------"
    #print text

    if_win = bet(2, small_blind_money, big_blind_money, players, bet_value, total_bet,community_cards)
    if if_win == 0:  # if there is already a winner, end this round
        renew_round(players, dealer, round, poker)
        continue
    if if_win == 2:
        showdown(poker,players,bet_value, total_bet,community_cards)
        renew_round(players, dealer, round, poker)
        continue
    #print "**************************************************"

    #turn round bet, round 3
    print "**************************************************"
    print "3.Turn Round"
    print_identity(players)
    #print out the human player's hand
    for i in range(len(players_hands)):
        if players[i].get_id() == "human":
            hand = players[i].get_hand()
            text = "your hand - "
            for card in hand:
                text += str(card) + "  "
            convert(text)

            #print text

    card = poker[0].getOne()
    if not card:
        sys.exit("*** ERROR ***: Insufficient cards to distribute.")
    community_cards.extend( card )

    text = "community cards - "
    for card in community_cards:
        text += str(card) + "  "
    convert(text)
    print "--------------------------------------------------"
    #print text

    if_win = bet(3, small_blind_money, big_blind_money, players, bet_value, total_bet, community_cards)
    if if_win == 0:  # if there is already a winner, end this round
        renew_round(players, dealer,round, poker)
        continue
    if if_win == 2:
        showdown(poker,players,bet_value, total_bet,community_cards)
        renew_round(players, dealer, round, poker)
        continue
    #print "**************************************************"


    #river round bet, round 4
    print "**************************************************"
    print "4.River Round"
    print_identity(players)
    #print out the human player's hand
    for i in range(len(players_hands)):
        if players[i].get_id() == "human":
            hand = players[i].get_hand()
            text = "your hand - "
            for card in hand:
                text += str(card) + "  "
            convert(text)
            #print text

    card = poker[0].getOne()
    if not card:
        sys.exit("*** ERROR ***: Insufficient cards to distribute.")
    community_cards.extend( card )
    text = "community cards - "
    for card in community_cards:
        text += str(card) + "  "
    convert(text)
    print "--------------------------------------------------"
    #print text

    if_win = bet(4, small_blind_money, big_blind_money, players, bet_value, total_bet,community_cards)
    if if_win == 0:  # if there is already a winner, end this round
        renew_round(players, dealer,round, poker)
        continue
    if if_win == 2:
        showdown(poker,players,bet_value, total_bet,community_cards)
        renew_round(players, dealer, round, poker)
        continue
    #print "**************************************************"

    #Displays the Cards
    print "**************************************************"
    print "5.showdown"

    showdown(poker,players,bet_value, total_bet,community_cards)
    renew_round(players, dealer, round, poker)


    continue
