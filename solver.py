'''
Module for solving word games on squared boards like Wordbrain in Polish.
Each letter on the board can be used only once.
Empty fields should be replaced with a space (' ').
'''
words_dictionaries = []

def upload_all(filelist):
	'''
	Upload words from filelist, using upload_words function from parseHTML.
	Then the list is returned.
	'''
	from parseHTML import upload_words
	result = []
	for f in filelist:
		words = upload_words(f)
		result.append(words)
	return result

def find_word(board, word_len, verbose = False):
	'''
	Find all words of given lenght on the board.
	'''
	results = []
	word_list = words_dictionaries[word_len]
	for x in range(0, len(board)):
		for y in range(0, len(board)):
			if(board[x][y] is not ' ' and board[x][y] is not 'ń' and board[x][y] is not 'y'):
				if verbose:
					print("coordinates: " + str(x) + " " + str(y))
				#get all words on this board that start on this field
				r = find_word_start_with(board, x, y, word_len, word_list)
				if len(r) >= 1:
					for el in r:
						results.append(el)
						if verbose:
							print("word: " + str(el))
	return results


def find_word_start_with(board, x, y, word_len, word_list):
	'''
	Find all words that start on the field of (x, y) coordinates
	'''
	# exclude a case of one-letter word
	if(word_len == 1 and board[x][y] in word_list):
		return (board[x][y], ((x, y)))
	elif word_len == 1:
		return None
	
	results = []
	#get all possible next moves from this field (coordinates)
	next_moves = get_next_moves(x, y, len(board), board)

	#we have the first letter - get all the next
	for i in range(2, word_len+1):
		#it's the last letter to fill - if there are any moves possible, for each check if the word exists in the dictionary
		if(i == word_len):
			for x in next_moves:
				word = ""
				for i in range(0, word_len):
					word += board[x[i][0]][x[i][1]] #add the last letter
				if(word in word_list):
					results.append((word, x))
			return results
		
		#we have more than one letter to fill
		new_next_moves = []
		#after adding 2 letters, check if the word exists in the dictionary - if no, stop searching that way
		check_if_word_exists = i % 2
		for x in next_moves:
			new_moves = get_next_moves(x[i-1][0], x[i-1][1], len(board), board)
			for y in new_moves:
				#check if this letter is already added to the possible solution -if no, it can be added
				if y[1] not in x:
					if check_if_word_exists is not 0 or is_this_on_list(x, y[1], word_list, board): #and-or trick: check the existence of the word or just add coordinates
						new_x = list(x)
						new_x.append(y[1])
						new_next_moves.append((tuple(new_x)))
		# no possible solution is found
		if new_next_moves == []:
			return results
		#we have new list of begining of possible solution
		next_moves = new_next_moves


def is_this_on_list(begining, end_of_begining, word_list, board):
	'''
	Check if the words with given beginning is in the dictionary
	'''
	word = ""
	for i in range(0, len(begining)):
		word += board[begining[i][0]][begining[i][1]]
	word += board[end_of_begining[0]][end_of_begining[1]]
	return any(item.startswith(word) for item in word_list)


def get_next_moves(x, y, max, board):
	'''
	Return possible neighbours of the letter (must be within the borders of the board and not be a space= an empty field)
	'''
	moves = []
	for el_x in range(x-1, x+2):
		for el_y in range(y-1, y+2):
			if(el_x >= 0 and el_x < max and el_y >= 0 and el_y < max and board[el_x][el_y] is not ' '):
				moves.append(((x, y), (el_x, el_y)))
	moves.remove(((x, y), (x, y) ))
	return moves


def solve_board(board, list_of_word_lenght, proper_solution, words_solved = [], verbose = False):
	'''
	Solve the board recursively. Lenghts of futher words must be provided.
	'''

	if len(list_of_word_lenght) < 1:
		# recursion ended
		if verbose:
			print("---SOLUTION---")
			print(words_solved)
		proper_solution.append(words_solved)
		return words_solved
	
	word_len = list_of_word_lenght[0]
	import copy
	new_list_of_word_lenght = copy.deepcopy(list_of_word_lenght)
	new_list_of_word_lenght.remove(word_len)
	words_found = find_word(board, word_len)

	if verbose:
		print("PREPARING FOR " + str(word_len))
		print("our board is like: ")
		for x in board:
			print(x)

	if len(words_found) < 1:
		if verbose:
			print("sorry, no words")
			print(words_solved)
			print("ending recursion")
		return None
	
	# for each found word - remove it from board and search for the next
	for w in words_found:
		import copy
		new_board_for_function = copy.deepcopy(board)
		new_board = remove_from_board(new_board_for_function, w[1])
		if verbose:
			for x in new_board:
				print(x)
			print("************** -> recursion started for " + w[0])
			print("appended word " + w[0])
		new_words_solved = copy.deepcopy(words_solved)
		new_words_solved.append(w)
		solve_board(new_board, new_list_of_word_lenght, proper_solution, new_words_solved)

def remove_from_board(board, list_of_indexes, verbose = False):
	'''
	Remove the given word (as a list of coordinates) from the board - for the rest of letter "gravity" works.
	'''
	#replace the word with space fields
	for x in list_of_indexes:
		el_x = x[0]
		el_y = x[1]
		board[el_x][el_y] = ' '

	if verbose:
		for x in board:
			print(x)
	
	# run through all rows from the bottom except the highest
	for i in range(len(board)-1, 0, -1):
		for m in range(0, len(board)): #run through the column
			if board[i][m] == ' ':
				if verbose:
					print("space on %d, %d" % (i, m))
				#get all of the letters above down
				all_spaces_in_column = False
				while board[i][m] == ' ' and not all_spaces_in_column:
					all_spaces_in_column = True
					for j in range(i-1, -1, -1):
						if board[j][m] is not ' ':
							all_spaces_in_column = False
						board[j+1][m] = board[j][m]
						if j == 0:
							board[0][m] = ' '
	
	return board


if __name__ == '__main__':

	#prepare dictionaries
	filelist = []
	for i in range(3, 13):
		filelist.append(str(i) + ".txt")
	words_dictionaries = [[], [], []]
	words_dictionaries.extend(upload_all(filelist))
	words_dictionaries = tuple(words_dictionaries)

	board = [	['b', 'a', 's'],
				['ó', 's', 'z'],
				['l', 'a', 'n']
		]
	solutions = []
	solve_board(board, [3, 6], solutions)
	for s in solutions:
		print(s)
