from objects import *
import sys,random, copy
from copy import deepcopy
from rules import preMaker,midMaker
#===============================================
#------------------Bet--------------------------
#===============================================
#for this part,doing the bet part, and calculate the money
#eg:in a game with money $1/$2(min_money=1,max_money=2), small blind bets is 0.5 and big blind bets is 1,
# in each round, the biggest raise is 2
#min_money is 1 and max_money is 2 in the example above
#players is a list contains all the players( in all the functions, players is the same)


def bet(round, small_blind_money, big_blind_money, players,bet_value, total_bet, community_cards):


    money_check(players) #check if the players have enough money before the game

    if round == 1: #pre-flop,small bet
         #position is the num of the players with dealer identity
        bet_value[0] = big_blind_money # bet_value is the money of nowadays' bet
        total_bet[0] = bet_value[0] + small_blind_money       # the total money that all the players have bet.
        result = turn(small_blind_money, big_blind_money, round, players, bet_value, total_bet, community_cards)
        print " "

    elif round == 2: #flop,small bet
        result = turn(small_blind_money, big_blind_money, round, players,bet_value, total_bet, community_cards)
        print " "

    elif round == 3: #turn,big bet
        result = turn(small_blind_money, big_blind_money, round, players,bet_value, total_bet, community_cards)
        print " "

    elif round == 4: #river,big bet
        result = turn(small_blind_money, big_blind_money, round, players,bet_value, total_bet, community_cards)
        print " "

    elif round == 5: #showdown, but actually we do not bet in this stage
        print " "

    else:
        sys.exit("system error, should not contain round more than 5")
    return result
#===============================================
#------------------turn-------------------------
#===============================================
#the players take turns betting, players is a list contains all the players


def turn(small_blind_money, big_blind_money, round, players,bet_value, total_bet, community_cards):
    #return 0 means already find the winner
    #return 1 means keep running this game
    #return 2 means someone all in and the other guy will showdown with him
    raise_time = 0 # record the raise times and decide if this round should end.
    check_time = 0 # record the continuous check times and decide if this round should end.

    while(1): # each round at most raise 3 times.
        #find the dealer, the player(jack) is the player after the dealer, and he will start the game
        #*****************************************************************************************
        #********************************** attention ********************************************
        #*****the dealer is not the real dealer, but to decide the first player of each round*****
        #*****************************************************************************************
        dealer = 0

        if len(players) == 2:# if there are only 2 players, there is no dealer anymore,only big blind and small blind
            for i in range(len(players)):
                if(players[i].get_identity() == "big blind" and players[i].get_state() == "playing"):
                    dealer = i


        if len(players) > 2:  # if there are more than 2 players, there is a dealer
            for i in range(len(players)):
                if (players[i].get_identity() == "dealer" and players[i].get_state() == "playing"):
                    dealer = i
#------------------------------------------------------------------------------------------
#************players from player (jack) to the end of list bet. players[jack: end]*********
        for j in range( (dealer + 1) % len(players), len(players)):
            #----if other players have already fold, end this round--------------
            alive = 0

            for i in range(len(players)):
                if players[i].get_state() == "playing" or players[i].get_state() == "all in":
                    alive += 1
            # if everyone has all in------------
            alive1 = 0
            for i in range(len(players)):
                if players[i].get_state() == "playing":
                    alive1 += 1
            if alive1 <= 1:
                return 2
            #------------------------------------
            if alive == 2:#all in player showdown with another player
                for i in range(len(players)):
                    if players[i].get_state() == "all in":
                        return 2

            if alive == 1:
                for i in range(len(players)):
                    if players[i].get_state() == "playing":
                        print "winner is player",players[i].get_id()," ", i
                        players[i].change_money(total_bet[0])
                        # as the winner is not the all in player, so the money he has changed to 0
                        for j in range(len(players)):
                            if players[j].get_state() == "all in":
                                players[j].change_money(0)
                                players[j].change_state("out")
                    # if the player left is all in, do not need change the money anymore
                    elif players[i].get_state() == "all in":
                        for j in range(len(players)):
                                    if players[j].get_state() == "out":
                                        players[j].change_money((total_bet[0] - players[i].get_money()) / (len(players) - 1))
                    return 0  #return 0 means already find the winner


            #-------------------------------------------------------------------
            # big blind and small blind automatically bet
            if round == 1 and players[j].get_identity() == "small blind" and players[j].get_state() == "playing" and players[j].get_chip() == 0:
                players[j].change_money(-small_blind_money)
                players[j].change_chip(small_blind_money)
                continue
            if round == 1 and players[j].get_identity() == "big blind" and players[j].get_state() == "playing" and players[j].get_chip() == 0:
                players[j].change_money(-big_blind_money)
                players[j].change_chip(big_blind_money)
                continue
            #-------------------------------------------------------------------

            choices = 0

            if players[j].get_state() == "playing":

                num = copy.deepcopy(j)
                choices = choice(small_blind_money, bet_value, total_bet, round, players,num, raise_time, community_cards)
                if choices == 2: # equal to 2 means raise
                    raise_time += 1
                    check_time = 0
                elif choices == 4 or choices == 3 or choices == 1:
                    check_time += 1
                else:
                    check_time = 0
                #get the number of player alive now
                number_on_table = 0
                for i in players:
                    if i.get_state() == "playing":
                        number_on_table += 1
                #if all the players alive check, this round will end
                if check_time >= number_on_table:
                    return 1
#------------------------------------------------------------------------------------------
#*********players from the beginning of the list to the big_blind bet. players[0: big_blind]************
        for j in range(0, dealer + 1):
            choices = 0 #intialize the choice

            # if other players have already fold, end this round-----------
            alive = 0
            for i in range(len(players)):
                if players[i].get_state() == "playing" or players[i].get_state() == "all in":
                    alive += 1

            # if everyone has all in------------
            alive1 = 0

            for i in range(len(players)):
                if players[i].get_state() == "playing":
                    alive1 += 1
            if alive1 <= 1 and alive > alive1:
                return 2
            #------------------------------------

            if alive == 2:#all in player showdown with another player
                for i in range(len(players)):
                    if players[i].get_state() == "all in":
                        return 2

            if alive == 1:
                for i in range(len(players)):
                    if players[i].get_state() == "playing":
                        print "winner is player", players[i].get_id()," ", i
                        players[i].change_money(total_bet[0])
                        # as the winner is not the all in player, so the money he has changed to 0
                        for m in range(len(players)):
                            if players[m].get_state() == "all in":
                                players[m].change_money(0)
                                players[m].change_state("out")

                    # if the player left is all in, do not need change the money anymore
                    elif players[i].get_state() == "all in":
                        for m in range(len(players)):
                                    if players[m].get_state() == "out":
                                        players[m].change_money(float(total_bet[0] - players[i].get_money()) / float(len(players) - 1))
                    return 0  #return 0 means already find the winner
            #---------------------------------------------------------------

            # big blind and small blind automatically bet
            if round == 1 and players[j].get_identity() == "small blind" and players[j].get_state() == "playing" and players[j].get_chip() == 0:
                players[j].change_money(-small_blind_money)
                players[j].change_chip(small_blind_money)
                continue
            if round == 1 and players[j].get_identity() == "big blind" and players[j].get_state() == "playing" and players[j].get_chip() == 0:
                players[j].change_money(-big_blind_money)
                players[j].change_chip(big_blind_money)
                continue
            #-------------------------------------------------------------------
            if players[j].get_state() == "playing":

                num = copy.deepcopy(j)

                #judge if the raise time up the 3
                choices = choice(small_blind_money, bet_value, total_bet, round, players,num, raise_time, community_cards)
                if choices == 2: # equal to 2 means raise
                    raise_time += 1
                    check_time = 0
                elif choices == 4 or choices == 3 or choices == 1:
                    check_time += 1
                else:
                    check_time = 0

                #get the number of player alive now
                number_on_table = 0
                for i in players:
                    if i.get_state() == "playing":
                        number_on_table += 1

                #if all the players alive check, this round will end
                if check_time >= number_on_table:
                    return 1

#===============================================
#------------------choice-----------------------
#===============================================

def choice(small_blind,bet_value, total_bet, round, players, num, raise_time, community_cards):
    #round records which round the game is, num records the label of player we want to operate
    # this version of code, we do not involve any heuristic strategies, so the AI just pick the choice randomly
    # round means Pre-flop, flop, or ..., raise_time calculate the time or raise each round(pre-flop, flop...)
    #because each round we at most raise 3 times
    #community_cards is the obvious that it is community cards, the decision of AIs is based on that.

    #*************************************************************************************
    #*****Wen Chen, your job is giving the get_choice variable the right choice***********
    #**********************************Good luck!*****************************************
    my_bet = 0
    if round == 1: #in our AI system, we do not allow fold at the beginning of the game
        if players[num].get_id() == "human":
            get_choice = human_player(round, players)
        else:
            get_choice,my_bet = preMaker(small_blind, bet_value[0]-players[num].get_chip(),total_bet[0],players,num)
    else:
        if players[num].get_id() == "human":
            get_choice = human_player(round, players)
        else:
            get_choice, my_bet = midMaker(small_blind,bet_value[0]-players[num].get_chip(),total_bet[0],players,num,community_cards,round)
    #if the raise time has already been 3, the players can not raise any more
    while(raise_time > 2 and get_choice == 2):
        if players[num].get_id() == "human":
            print "each round at most raise 3 times, we regard your choice as match"
            get_choice = 3

        else:
            get_choice = 3

    if get_choice == 1:  # fold
        player_fold(round, players, num)
        #print ""
        return 1
    if get_choice == 2:  # raise
        player_raise(bet_value, total_bet, round, players, num, my_bet)
        print ""
        return 2
    if get_choice == 3:  # match
        if players[num].get_chip() == bet_value:
            player_check(bet_value, total_bet, round, players, num)
            return 4
        else:
            if_check = player_match(bet_value, total_bet, round, players, num)
            if if_check == 1:
                return 3
            else:
                return 4

    if get_choice == 4:  # check

        if players[num].get_chip() < bet_value: # if the player can not check ,should turn to match
            player_match(bet_value, total_bet, round, players, num)
            return 3
        else:
            player_check(bet_value, total_bet, round, players, num)
            return 4

#===============================================
#------------------player fold------------------
#===============================================
# the player fold chip in the bet


def player_fold(round, players, num):

    if round > 5:
        sys.exit("system error, should not contain round more than 5")
    players[num].change_state("out")  # as the player fold, delete him or her from the list
    players[num].change_chip(0) #reset the player's chip to 0
    print "player  ", num," ", players[num].get_id(), "  fold"

#===============================================
#------------------player raise-----------------
#===============================================
# the player raise chip in the bet


def player_raise(bet_value, total_bet, round, players, num,ai_bet):

    if round > 5:
        sys.exit("system error, should not contain round more than 5")

    if players[num].get_id() == "human":
        #-------input judgement part----------------------------------
        k = []
        k = (raw_input("enter the amount of money you want to raise, 2-10 dollars is allowed: "))
        while(not k.isdigit()):
            print "error,you must input a number,the number of money 2-10 dollars is allowed"

            k = raw_input("enter the amount of money you want to raise, 2-10 dollars is allowed: ")
        k = int(k)
        while(k < 1 ):
            print ""
            print "error,you must input a number,the number of money 2-10 dollars is allowed"
            k = raw_input("enter the amount of money you want to raise: ")
            if k.isdigit():
                k = int(k)
        money_raise = k

    else:
        money_raise = ai_bet
    #------------------ all in------------------
    if float(money_raise + bet_value[0] - players[num].get_chip()) > float(players[num].get_money()):
        print "player  ", num, " ", players[num].id, "  all in, but only has money: ", players[num].money
        all_in(bet_value, total_bet, players, num)
        print "the current pot is :", total_bet[0]
        return
    #--------------------------------------------
    bet_value[0] += money_raise
    money_change = bet_value[0] - players[num].get_chip()
    players[num].change_money(-money_change) #the money the player own becomes less

    players[num].change_chip(money_change)   #the money of the player bet increase

    total_bet[0] += money_change

    money_check(players) # check if the players have enough money

    print "player  ",num, " ", players[num].id, "  raise to ", bet_value[0]
    print "the current pot is :", total_bet[0]
    return

#===============================================
#------------------player match-----------------
#===============================================
# the player choose to match chip in the bet
def player_match(bet_value, total_bet, round, players, num):

    if round > 5:
        sys.exit("system error, should not contain round more than 5")

    difference = bet_value[0] - players[num].chip
    if difference == 0:
        player_check(bet_value, total_bet, round, players, num)
        return 0
    #------------------ all in------------------
    if difference > players[num].money:
        print "player  ", num, " ", players[num].id, "  all in, but only has money: ", players[num].money
        all_in(bet_value, total_bet, players, num)
        print "the current pot is :", total_bet[0]
        return 1
    #-------------------------------------------
    #print "difference:", difference
    players[num].change_money(-difference)
    players[num].change_chip(difference)
    total_bet[0] += difference
    money_check(players)  # check if the players have enough money
    print "player  ", num, " ", players[num].id, "  match to ", bet_value[0]
    print "the current pot is :", total_bet[0]
    return 1

#===============================================
#------------------player check-----------------
#===============================================
def player_check(bet_value, total_bet, round, players, num):

    if round > 5:
        sys.exit("system error, should not contain round more than 5")
    print "player  ", num, " ", players[num].id, "  check, the chip is: ", bet_value[0]
    print "the current pot is :", total_bet[0]
    return


#===============================================
#------------------check money------------------
#===============================================
# check if the player has enough money to play the game
def money_check(players):
    for i in range(len(players)):
            if players[i].get_money() <= 0:
                if players[i].get_id() == "human":
                    print players[i].get_chip()
                    sys.exit("you do not have enough money!!!!!!!!, game over")
                elif players[i].get_id() == "computer":
                    print" players", i, "does not have enough money, he/she is out."
                    number_of_players = 0
                    for j in players:
                        if j.get_money() > 0 or j.get_state() == "all in":
                            number_of_players += 1

                    if number_of_players > 2:
                        number_of_players -= 1
                        players[i].change_state("out")

                    else:
                        print "game over, only one player left with enough money"
                        sys.exit("game over, only one player left with enough money")


#===============================================
#-------------human_player----------------------
#===============================================
#human player's action

def human_player(round, players):
    num = 0
    for i in range(len(players)):
        if players[i].get_id() == "human":
            num = i
    #print "--------------------------------------------------"
    print "----------It is your turn----------"
    #print "you are player ", num
    print "your chip left is : ", players[num].get_money()
    #print "1.fold, 2.raise, 3.match/check(enter the number of option)"
#-------input judgement part----------------------------------
    k = []
    k = raw_input("1.fold, 2.raise, 3.match/check, enter the number of option: ")
    while(not k.isdigit()):
        print "error,you must input a number,the number between 1-3 is allowed"

        k = raw_input("1.fold, 2.raise, 3.match/check, enter the number of option: ")
    k = int(k)
    while(k < 1 or k > 3 ):
        print ""
        print "error,you must input a number,the number between 1-32 is allowed"
        k = raw_input("1.fold, 2.raise, 3.match/check, enter the number of option: ")
        if k.isdigit():
            k = int(k)
    choices = k
    return choices
#===============================================
#-------------all-in judgement------------------
#===============================================
def all_in(bet_value, total_bet, players, num):

    if (players[num].get_money() + players[num].get_chip()) < bet_value:
        players[num].change_state("all in")
        total_bet[0] += players[num].get_money()
        players[num].change_side(total_bet[0])

        # if the all-in player does not win the game finally, the money value will change to 0
        players[num].change_money(total_bet[0] - (bet_value[0] - players[num].get_money()))

    print ""
