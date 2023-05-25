#https://github.com/drewp41/Vigenere-Cipher-Breaker/
from const import english_frequences
from const import spanish_frequences
from const import french_frequences
import processing

# Returns the Index of Councidence for the "section" of ciphertext given
def get_index_c(ciphertext,dictionary):

	N = float(len(ciphertext))
	frequency_sum = 0.0
	# Using Index of Coincidence formula
	for letter in dictionary:
		frequency_sum+= ciphertext.count(letter) * (ciphertext.count(letter)-1)
	# Using Index of Coincidence formula
	if(N*(N-1) <= 0):
		ic = 0
	else:
		ic = frequency_sum/(N*(N-1))
	return ic

# Returns the key length with the highest average Index of Coincidence
def get_key_length(ciphertext, dictionary, max_guess):
	ic_table=[]

	# Splits the ciphertext into sequences based on the guessed key length from 0 until the max key length guess (20)
	# Ex. guessing a key length of 2 splits the "12345678" into "1357" and "2468"
	# This procedure of breaking ciphertext into sequences and sorting it by the Index of Coincidence
	# The guessed key length with the highest IC is the most porbable key length
	for guess_len in range(max_guess):
		ic_sum=0.0
		avg_ic=0.0
		for i in range(guess_len):
			sequence=""
			# breaks the ciphertext into sequences
			for j in range(0, len(ciphertext[i:]), guess_len):
				sequence += ciphertext[i+j]
			ic_sum+=get_index_c(sequence,dictionary)
		# obviously don't want to divide by zero
		if not guess_len==0:
			avg_ic=ic_sum/guess_len
		ic_table.append(avg_ic)

	# returns the index of the highest Index of Coincidence (most probable key length)
	best_guess = ic_table.index(sorted(ic_table, reverse = True)[0])
	if best_guess == 0:
		return best_guess
	second_best_guess = ic_table.index(sorted(ic_table, reverse = True)[1])

	# Since this program can sometimes think that a key is literally twice itself, or three times itself, 
	# it's best to return the smaller amount.
	# Ex. the actual key is "dog", but the program thinks the key is "dogdog" or "dogdogdog"
	# (The reason for this error is that the frequency distribution for the key "dog" vs "dogdog" would be nearly identical)
	if second_best_guess == 0:
		return best_guess
	if best_guess % second_best_guess == 0:
		return second_best_guess
	else:
		return best_guess

def freq_analysis(sequence, dictionary, lang):
	if(lang == "en"):
		frequences = english_frequences
	elif(lang=="es"):
		frequences = spanish_frequences
	elif(lang=="fr"):
		frequences = french_frequences
	else:
		frequences = []

	all_chi_squareds = [0] * len(dictionary)
	for i in range(len(dictionary)):
		currentLetter = dictionary[i]
		chi_squared_sum = 0.0
		#Decrypt sequence with current letter
		sequence_offset = processing.decypher(sequence.upper(), currentLetter, dictionary)
		v = [0] * len(dictionary)
		# count the numbers of each letter in the sequence_offset
		for l in range(len(sequence_offset)):
			minLetter = sequence_offset[l]
			# v[index de l in dictionary]
			v[dictionary.index(minLetter)] += 1
		# divide the array by the length of the sequence to get the frequency percentages
		for j in range(len(dictionary)):
			v[j] *= (1.0/float(len(sequence)))

		# now you can compare to the choosen frequencies
		for j in range(len(dictionary)):
			letter = dictionary[j].lower()
			chi_squared_sum+=((v[j] - float(frequences[letter]))**2)/float(frequences[letter])
		# add it to the big table of chi squareds
		all_chi_squareds[i] = chi_squared_sum

	# return the letter of the key that it needs to be shifted by
	# this is found by the smallest chi-squared statistic (smallest different between sequence distribution and 
	# choosen language distribution)
	shift = all_chi_squareds.index(min(all_chi_squareds))
	return dictionary[shift]

def get_key(ciphertext, key_length, dictionary, lang):
	key = ''

	# Calculate letter frequency table for each letter of the key
	for i in range(key_length):
		sequence=""
		# breaks the ciphertext into sequences
		for j in range(0,len(ciphertext[i:]), key_length):
			sequence+=ciphertext[i+j]
		key+=freq_analysis(sequence, dictionary,lang)

	return key