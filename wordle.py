import random

def help_message() -> None:
	print("/help for help\n" +
			"/im-dumb for the helper\n" +
			"/i-cant-do-this for the answer, now you can feel good about yourself")

def wordle_bot_helper() -> None:
	print("if help is needed and any time (this is unintuitive), type /help")
	xs = None
	while (not xs):
		xs = input("enter string: ")
		if xs == '/help':
			print("type in all of the 'green' letters, with a space if the letter in that position is not known\n")
			xs = None
		elif len(xs) != 5:
			print("5 characters (including spaces) required")
			xs = None
	file = open('words_alpha.txt', 'r')
	available_answers = []
	initial_available_answers = [line.replace('\n', '') for line in file if len(line.replace('\n', '')) == 5]
	
	file.close()
	for i, x in enumerate(xs):
		if x != ' ':
			initial_available_answers = [word for word in initial_available_answers if x == word[i] and word in initial_available_answers]
	number_of_lines = None
	while(not number_of_lines):
		number_of_lines = input('how many yellow letters: ')
		if number_of_lines == '/help':
			print("type in the number of unique 'yellow' letters\n")
		elif number_of_lines and number_of_lines.isdigit():
			number_of_lines = int(number_of_lines)
		else:
			print("please enter a number")
			number_of_lines = None
	for pl in range(number_of_lines):
		separate_available_answers = [[],[],[],[],[]]
		ys = None
		while (not ys):
			ys = input('possible places for letter: ')
			if ys == '/help':
				print("for each letter, put each possible position for the letter, with a space where the letter can not be, only have one unique letter per input, for example, 'aa a ' means there could be an a in the first 2 or 4th position")
				ys = None
			elif len(ys) != 5:
				print("5 characters (including spaces) required")
				ys = None
		for i, y in enumerate(ys):
			if y != ' ' and ys != xs[i]:
				separate_available_answers[i] = [word for word in initial_available_answers if y == word[i] and word in initial_available_answers and word not in available_answers]
		initial_available_answers = separate_available_answers[0] + separate_available_answers[1] + separate_available_answers[2] + separate_available_answers[3] + separate_available_answers[4]
	zs = None
	while (not zs):
		zs = input("disallowed letters: ")
		if zs == '/help':
			print("give every letter that can not be in the answer\n")
			zs = None
	for i in range(3): #For loop fixes sometimes apparently, still does not work perfectly, may not remove some words, this code sucks
		for z in zs:
			for word in initial_available_answers:
				if z in word:
					initial_available_answers.remove(word)

	print(f'Possible Answers Are: \n{initial_available_answers}')

def command(command_input) -> None:
	print()
	if command_input == "help":
		help_message()
	elif command_input == "im-dumb":
		wordle_bot_helper()
	elif command_input == "i-cant-do-this":
		return 'This guy sucks'
	else:
		print("Not a valid command")
	print()

def player_guess(word_list: list[str]) -> str:
	guess = ""
	while not guess:
		guess = input("Put your 5 letter word in: \n")
		if guess:
			if guess[0] == "/":
				com = command(guess[1::])
				if com == 'This guy sucks':
					return 'He really does'
				return
			else:	
				if not guess.isalpha():
					print("Please type valid characters only")
					guess = ""
				elif guess not in word_list:
					print("Not a real word")
					guess = ""
				return guess
		

def game_state() -> int:
	file = open('words_alpha.txt')
	possible_words = [line.replace('\n', '') for line in file if len(line.replace('\n', '')) == 5]
	file.close()
	current_word = possible_words[random.randint(0, len(possible_words))]
	bad_letters = []
	attempt = 0
	while attempt < 6:
		guess = player_guess(possible_words)
		if guess == 'He really does':
			attempt = 6
			guess = None
		if guess:
			if guess == current_word:
				return attempt, current_word
			else:
				clue = ""
				for letter in range(5):
					if guess[letter] == current_word[letter]:
						clue_add = guess[letter]
					elif guess[letter] in current_word:
						clue_add = f'{guess[letter]}*'
						if (clue+clue_add).count(guess[letter]) > current_word.count(guess[letter]):
							clue_add = ' '
					else:
						if guess[letter] not in bad_letters:
							bad_letters.append(guess[letter])
						clue_add = ' '
					clue += f'[{clue_add}]'
				print(clue)
				print(f'Bad Letters: {bad_letters}')	
				print(f'{5-attempt} attempts left')
			attempt += 1
	return 0, current_word

def main() -> None:
	game, word = game_state()
	if game:
		print(f"You won in {game+1} turns")
	else:
		print(f"You lost.\nThe word was {word}")

if __name__ == "__main__":
	main()
