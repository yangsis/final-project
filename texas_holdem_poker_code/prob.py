'''
expected value is the expected revenue for per unit bet.
This file is for pre-flop step
'''

expected_value = {}

for symbol in range(0,4):
	#generate pairs
	cur_card = str(symbol)+str(5)+','+str(symbol)+str(5)
	expected_value[cur_card] = 0.15
	cur_card = str(symbol)+str(6)+','+str(symbol)+str(6)
	expected_value[cur_card] = 0.23

	cur_card = str(symbol)+str(7)+','+str(symbol)+str(7)
	expected_value[cur_card] = 0.309
	cur_card = str(symbol)+str(8)+','+str(symbol)+str(8)
	expected_value[cur_card] = 0.42

	cur_card = str(symbol)+str(9)+','+str(symbol)+str(9)
	expected_value[cur_card] = 0.55
	cur_card = str(symbol)+str(10)+','+str(symbol)+str(10)
	expected_value[cur_card] = 0.74

	cur_card = str(symbol)+str(11)+','+str(symbol)+str(11)
	expected_value[cur_card] = 0.97
	cur_card = str(symbol)+str(12)+','+str(symbol)+str(12)
	expected_value[cur_card] = 1.26

	cur_card = str(symbol)+str(13)+','+str(symbol)+str(13)
	expected_value[cur_card] = 0.63
	cur_card = str(symbol)+str(14)+','+str(symbol)+str(14)
	expected_value[cur_card] = 2.10

	cur_card = str(symbol)+str(4)+','+str(symbol)+str(4)
	expected_value[cur_card] = 0.11

	cur_card = str(symbol)+str(3)+','+str(symbol)+str(3)
	expected_value[cur_card] = 0.08

	cur_card = str(symbol)+str(2)+','+str(symbol)+str(2)
	expected_value[cur_card] = 0.06

	#generated suited card
	expected_value[str(symbol)+str(5)+','+str(symbol)+str(4)] = 0.08
	expected_value[str(symbol)+str(6)+','+str(symbol)+str(5)] = 0.11
	expected_value[str(symbol)+str(6)+','+str(symbol)+str(4)] = 0.03
	expected_value[str(symbol)+str(7)+','+str(symbol)+str(6)] = 0.74

	expected_value[str(symbol)+str(7)+','+str(symbol)+str(6)] = 0.15
	expected_value[str(symbol)+str(8)+','+str(symbol)+str(5)] = 0.03

	expected_value[str(symbol)+str(8)+','+str(symbol)+str(6)] = 0.12
	expected_value[str(symbol)+str(8)+','+str(symbol)+str(7)] = 0.20

	expected_value[str(symbol)+str(9)+','+str(symbol)+str(7)] = 0.19
	expected_value[str(symbol)+str(9)+','+str(symbol)+str(6)] = 0.09
	expected_value[str(symbol)+str(9)+','+str(symbol)+str(8)] = 0.28

	expected_value[str(symbol)+str(10)+','+str(symbol)+str(6)] = 0.08
	expected_value[str(symbol)+str(10)+','+str(symbol)+str(7)] = 0.18
	expected_value[str(symbol)+str(10)+','+str(symbol)+str(8)] = 0.30

	expected_value[str(symbol)+str(10)+','+str(symbol)+str(9)] = 0.42

	expected_value[str(symbol)+str(11)+','+str(symbol)+str(7)] = 0.16

	expected_value[str(symbol)+str(11)+','+str(symbol)+str(8)] = 0.30
	expected_value[str(symbol)+str(11)+','+str(symbol)+str(9)] = 0.40

	expected_value[str(symbol)+str(11)+','+str(symbol)+str(10)] = 0.30
	expected_value[str(symbol)+str(12)+','+str(symbol)+str(2)] = 0.05
	expected_value[str(symbol)+str(12)+','+str(symbol)+str(3)] = 0.07
	expected_value[str(symbol)+str(12)+','+str(symbol)+str(4)] = 0.09
	expected_value[str(symbol)+str(12)+','+str(symbol)+str(5)] = 0.12

	expected_value[str(symbol)+str(12)+','+str(symbol)+str(6)] = 0.14

	expected_value[str(symbol)+str(12)+','+str(symbol)+str(7)] = 0.18
	expected_value[str(symbol)+str(12)+','+str(symbol)+str(8)] = 0.30

	expected_value[str(symbol)+str(12)+','+str(symbol)+str(9)] = 0.41
	expected_value[str(symbol)+str(12)+','+str(symbol)+str(10)] = 0.60

	expected_value[str(symbol)+str(12)+','+str(symbol)+str(11)] = 0.66
	expected_value[str(symbol)+str(13)+','+str(symbol)+str(2)] = 0.14

	expected_value[str(symbol)+str(13)+','+str(symbol)+str(3)] = 0.17
	expected_value[str(symbol)+str(13)+','+str(symbol)+str(4)] = 0.19

	expected_value[str(symbol)+str(13)+','+str(symbol)+str(5)] = 0.21
	expected_value[str(symbol)+str(13)+','+str(symbol)+str(6)] = 0.24

	expected_value[str(symbol)+str(13)+','+str(symbol)+str(7)] = 0.30
	expected_value[str(symbol)+str(13)+','+str(symbol)+str(8)] = 0.32

	expected_value[str(symbol)+str(13)+','+str(symbol)+str(9)] = 0.45
	expected_value[str(symbol)+str(13)+','+str(symbol)+str(10)] = 0.63

	expected_value[str(symbol)+str(13)+','+str(symbol)+str(11)] = 0.71
	expected_value[str(symbol)+str(13)+','+str(symbol)+str(12)] = 0.80

	expected_value[str(symbol)+str(14)+','+str(symbol)+str(2)] = 0.30
	expected_value[str(symbol)+str(14)+','+str(symbol)+str(3)] = 0.34

	expected_value[str(symbol)+str(14)+','+str(symbol)+str(4)] = 0.36
	expected_value[str(symbol)+str(14)+','+str(symbol)+str(5)] = 0.39

	expected_value[str(symbol)+str(14)+','+str(symbol)+str(6)] = 0.34
	expected_value[str(symbol)+str(14)+','+str(symbol)+str(7)] = 0.39

	expected_value[str(symbol)+str(14)+','+str(symbol)+str(8)] = 0.44
	expected_value[str(symbol)+str(14)+','+str(symbol)+str(9)] = 0.50

	expected_value[str(symbol)+str(14)+','+str(symbol)+str(10)] = 0.68
	expected_value[str(symbol)+str(14)+','+str(symbol)+str(11)] = 0.76

	expected_value[str(symbol)+str(14)+','+str(symbol)+str(12)] = 0.86
	expected_value[str(symbol)+str(14)+','+str(symbol)+str(13)] = 1.00


#generated unsuited cards

for s1 in range(0,4):
	for s2 in range(0,4):
		if s2 == s1:
			continue
		expected_value[str(s1)+str(10)+','+str(s2)+str(9)] = 0.13
		expected_value[str(s1)+str(11)+','+str(s2)+str(9)] = 0.11
		expected_value[str(s1)+str(11)+','+str(s2)+str(10)] = 0.58

		expected_value[str(s1)+str(12)+','+str(s2)+str(10)] = 0.30
		expected_value[str(s1)+str(12)+','+str(s2)+str(11)] = 0.38

		expected_value[str(s1)+str(13)+','+str(s2)+str(9)] = 0.14
		expected_value[str(s1)+str(13)+','+str(s2)+str(10)] = 0.33

		expected_value[str(s1)+str(13)+','+str(s2)+str(11)] = 0.42
		expected_value[str(s1)+str(13)+','+str(s2)+str(12)] = 0.53

		expected_value[str(s1)+str(14)+','+str(s2)+str(9)] = 0.18

		expected_value[str(s1)+str(14)+','+str(s2)+str(10)] = 0.37
		expected_value[str(s1)+str(14)+','+str(s2)+str(11)] = 0.46

		expected_value[str(s1)+str(14)+','+str(s2)+str(12)] = 0.58
		expected_value[str(s1)+str(14)+','+str(s2)+str(13)] = 0.73
