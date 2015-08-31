'''file for rules'''


from objects import *
import sys,random, copy
from copy import deepcopy
from prob import expected_value
import math
from operator import attrgetter

upperbound = 10
lowerbound = 2

def preMaker(small_blind, bet,pot,players,num):
	'''decision procedure for pre-flop'''
	hands = players[num].get_hand() # list
	if hands[0].value < hands[1].value:
		hands[0],hands[1] = hands[1],hands[0]

	card_str = str(hands[0].symbol)+str(hands[0].value)+','+str(hands[1].symbol)+str(hands[1].value)
	player_money = players[num].get_money()
	#give up the game if the hand cards are too bad
	if card_str not in expected_value:
		if players[num].get_identity() == "big blind" or players[num].get_identity() == "small blind":
			if bet <= small_blind * 2 and pot/len(players) <= 2*small_blind and bet <= 0.5 * player_money:
				return 3,0
			else:
				return 1,0
		else:
			return 1,0

	exp_val = expected_value[card_str]
	max_bet = 0
	#1:fold
	#2: raise
	#3: match
	#4: check
	if exp_val >= 0.5: #Rule 2
		max_bet =  0.7*player_money if 0.7 * player_money <= upperbound else upperbound
		if bet < max_bet and max_bet >= lowerbound and players[num].get_chip() <= 5 * small_blind:
			return 2, int(math.floor(max_bet))
		elif bet < player_money and players[num].get_chip() < 6 * small_blind:
				return 3,0
		else:
			return 1,0

	elif exp_val >= 0.1 and exp_val<0.5: #Rule 3
		max_bet = 0.7 * player_money if 0.7 * player_money <=  upperbound else upperbound
		if bet == 0 and players[num].get_chip() < small_blind:
			return 2, 2*small_blind
		elif bet > max_bet:
			return 1,0
		else:
			return 3,0

	else: #rule 4
		if bet == 0:
			return 2,2*small_blind
		elif bet <= 2*small_blind:
			return 3,0
		else:
			return 1,0

def findLargestPoker(matches):
	'''
	Find the best hand
	'''
	# find straight flush if existing
	for mat in matches:
		if mat[0] == "straight flush":
			return mat

	for mat in matches:
		if mat[0] == "four of a kind":
			return mat

	#find full house
	three = []
	twos = []
	flag = 0
	for mat in matches:
		if mat[0] == "three of a kind":
			three.append(mat[1])

	for mat in matches:
		if mat[0] == "pair":
			two = mat[1]
			for tr in three:
				if two[0].value != tr[0].value:
					return ["full house",tr+two]
			twos.append(two)

	for mat in matches:
		if mat[0] == "flush":
			return mat
	for mat in matches:
		if mat[0] == "straight":
			return mat
	if three:
		return ["three of a kind",three[0]]
	if len(twos) >= 2:
		return ["two pairs",twos[0]+twos[1]]
	return ["pair",twos[0]] if twos else []

def removeDup(ordered_cards):
	'''remove the duplicated cards with same values. <ordered_cards> is the list of ordered cards'''
	cards = [ordered_cards[0]]
	for i in range(1,len(ordered_cards)):
		if ordered_cards[i] != ordered_cards[i-1]:
			cards.append(ordered_cards[i])
	return cards

def findValueCard(cards):
	'''
	Find the good hands
	'''
	#ascending order
	value_pokers = [] # for case 1
	cards = sorted(cards,key = attrgetter("symbol"))

	# find flush
	for i in range(len(cards)-4):
		if cards[i].symbol == cards[i+1].symbol == cards[i+2].symbol == cards[i+3].symbol == cards[i+4].symbol: #flush
			card_list = [cards[i+4],cards[i+3],cards[i+2],cards[i+1],cards[i]]
			card_list = sorted(card_list,key = attrgetter("value"))

			if (card_list[0].value+1 == card_list[1].value) and (card_list[1].value+1 == card_list[2].value) and (card_list[2].value+1 == card_list[3].value) and (card_list[3].value + 1 == card_list[4].value):
				value_pokers.append(["straight flush",card_list])
			else:
				value_pokers.append(["flush",card_list])


	#get full house, four of a kind, three of a kind, and pair
	cards = sorted(cards, key = attrgetter('value')) #sort the card by value
	idx = len(cards)-1
	while idx > 0:
		if idx > 2:
			if cards[idx] == cards[idx-1] == cards[idx-2] == cards[idx-3]: # four of a kind
				value_pokers.append(["four of a kind",[cards[idx],cards[idx-1],cards[idx-2],cards[idx-3]]])
				if idx == 3:
					break # because it must be the largest one
				idx = idx - 1
				continue
		if idx > 1:
			if cards[idx].value == cards[idx-1].value ==cards[idx-2].value: # three of a kind
				value_pokers.append(["three of a kind",[cards[idx],cards[idx-1],cards[idx-2]]])
				idx = idx-1
				continue
		if idx > 0:
			if cards[idx] == cards[idx-1]:
				value_pokers.append(["pair",[cards[idx],cards[idx-1]]])
		idx = idx -1


	# find the straight
	cards = removeDup(cards)
	idx = len(cards)-1
	a_flag = -1
	while idx > 0:
		if cards[idx].value == 14:
			a_flag = idx
		if idx > 3: # for straight
			if (cards[idx].value-1 == cards[idx-1].value
					and cards[idx-1].value-1 == cards[idx-2].value
					and cards[idx-2].value-1 == cards[idx-3].value
					and cards[idx-3].value-1== cards[idx - 4].value): #doesn't consider A here. will do it later
				value_pokers.append(["straight",[cards[idx],cards[idx-1],cards[idx-2],cards[idx-3],cards[idx-4]]])

		if idx > 2:
			if cards[idx-3].value == 2 and a_flag >=0 and cards[idx-2] .value == 3 and cards[idx-1].value == 4 and cards[idx].value == 5: # straight, starting from A
				value_pokers.append(["straight",[cards[idx],cards[idx-1],cards[idx-2],cards[idx-3],cards[a_flag]]])
		idx = idx-1

	return findLargestPoker(value_pokers) # see case 1

def findExpected(cards):
	'''
	find potential good hands in the next round
	'''
	expected_matches = []
	# find future possible flush
	cards = sorted(cards, key = attrgetter("symbol"))
	for i in range(len(cards)-3):
		if (cards[i].symbol == cards[i+1].symbol == cards[i+2].symbol == cards[i+3].symbol) and \
		((i + 3 > 0 and cards[i].symbol != cards[i-4].symbol) or (i+1<len(cards) and cards[i].symbol != cards[i+1].symbol)):
			expected_matches.append(["four to flush",[cards[i+3],cards[i+2],cards[i+1],cards[i]]])

	# find future possibl straight
	cards = sorted(cards,key = attrgetter("value"))
	cards = removeDup(cards)
	idx = len(cards) - 1
	A_flag = 0
	if cards[idx].value == 14:
		A_flag = 1
	while idx >= 3:
		if cards[idx].value == 5 and A_flag:
			if (cards[idx-1].value == 4 and cards[idx-2].value == 3) or (cards[idx-1] == 4 and cards[idx-2]==2) or (cards[idx-1]==3 or cards[idx-2]==2):
				expected_mathes.append(["inside straight",[cards[idx],cards[idx-1],cards[idx-2],cards[len(cards)-1]]])
		if (cards[idx] != cards[idx-1] != cards[idx-2] != cards[idx-3] ) and (cards[idx].value - cards[idx-1].value+cards[idx-1].value-cards[idx-2].value+cards[idx-2].value-cards[idx-3].value == 4):
			expected_matches.append(["inside straight",[cards[idx],cards[idx-1],cards[idx-2],cards[idx-3]]])
		if (idx - 3 > 0 and idx < len(cards)-1) and cards[idx].value-1 == cards[idx-1].value and cards[idx-1].value -1 == cards[idx-2].value-1 and cards[idx-2].value-1 == cards[idx-3].value:
			expected_matches.append(["outside straight",[cards[idx],cards[idx-1],cards[idx-2],cards[idx-3]]])
		idx  = idx - 1

	return expected_matches

def strForVal(pokers,bet,players,num,co,small_blind):
	'''decision procedure for the case when we have some competitive poker'''
	card_no = pokers[0]
	player_money = players[num].get_money()

	max_bet = small_blind if small_blind < 0.5 * player_money else 0.4 * player_money

	if card_no == "straight flush" or card_no == "four of a kind" or card_no == "full house":
		max_bet = co * 2 * bet if co * 2 * bet <= player_money else 0.9 * player_money
	elif card_no == "flush" or card_no == "straight":
		max_bet = co * 1.5 * bet if co * 1.5 * bet <= 0.9 * player_money else co * 0.8 * player_money
	elif card_no == "three of a kind":
		max_bet = co * 1.2* bet if co * bet <= 0.9 * player_money else co * 0.7 * player_money
	elif card_no == "two pairs":
		max_bet = co * bet if co* bet <= 0.9 * player_money else co * 0.6 * player_money
	elif card_no == "pair":
		max_bet == co * bet if co * bet <= 0.9 * player_money else co * 0.5 * player_money

	max_bet = max_bet if max_bet < upperbound else upperbound
	if max_bet < bet:
		return 1,0
	elif max_bet - bet >= small_blind:
		if max_bet >= lowerbound and players[num].get_chip() - small_blind * 3 < max_bet:
			return 2, int(math.floor(max_bet))
		else:
			return 3,0
	elif bet == 0:
		return 4,0
	else:
		return 3,0

def strForExp(expected, bet, pot,players,num,small_blind,round):
	'''decision for the expected pokers.
		considering pot odd and draw odd'''
	def potOdd(bet, pot): #get pot odds
		return (pot+bet)/1.0*bet
	def handOdds(current_match,round): #get hand odds
		unseen_cards = 52 - (round-1)*3
		if current_match[0] == "four to flush":
			outs = 13 - 4
		elif current_match[0] == "inside straight":
			outs = 4
		else:
			outs = 8
		return (unseen_cards/(1.0 * outs))-1

	pot_odd = potOdd(bet, pot)
	hand_odd = 0
	for current_match in expected:
		hand_odd_tmp = handOdds(current_match,round)
		hand_odd = hand_odd_tmp if hand_odd_tmp > hand_odd else hand_odd
	if hand_odd > pot_odd + small_blind:
		val = int(math.floor(bet+small_blind)) if math.floor(bet+small_blind) <= 0.9 * players[num].get_money() else int(math.floor(0.8 * players[num].get_money()))
		if val >=2:
			return 2, val if val < upperbound else upperbound
		else:
			return 3,0
	elif bet == 0:
		return 4,0
	elif hand_odd > pot_odd:
		return 3,0
	else:
		return 1,0

def midMaker(small_blind,bet,pot,players,num,community,round):
	'''Middle step decision maker. for after flop, after ture and river'''
	cards = copy.deepcopy(players[num].get_hand())
	cards.extend(community)

	largest_match = findValueCard(cards)

	expected_matches = []
	if round < 4:
		expected_matches = findExpected(cards)


	co = 1
	if expected_matches:
		co = 1.2

	# if all cards of largest_match are in community cards
	flag = 0
	count = 0
	if largest_match:
		for card in largest_match[1]:
			if card in players[num].get_hand():
				flag = 1
				break
		if flag == 0:
			co = 0.5
	if largest_match:
		return strForVal(largest_match,bet,players,num,co,small_blind)
	elif not expected_matches and bet == 0:
		return 4,0
	elif not expected_matches and (bet > 2*small_blind or round > 3):
		return 1,0
	elif not expected_matches:
		return 3,0
	else:
		return strForExp(expected_matches, bet, pot, players,num,small_blind,round)
