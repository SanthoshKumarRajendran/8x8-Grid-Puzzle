#!/usr/bin/python

# import pdb
from copy import copy
from pprint import pprint

class PuzzlePiece:
	def __init__(self, orientation):
		self.orientation = orientation
		self.state = self.create_puzzle_piece(orientation)

	'''
	the eight orientations that the puzzle piece can be in
	'''
	def create_puzzle_piece(self, orientation):
		if orientation == 0:
			return [[1, 0, 0], [1, 1, 1], [0, 1, 0]]
		elif orientation == 1:
			return [[0, 1, 1], [1, 1, 0], [0, 1, 0]]
		elif orientation == 2:
			return [[0, 1, 0], [1, 1, 1], [0, 0, 1]]
		elif orientation == 3:
			return [[0, 1, 0], [0, 1, 1], [1, 1, 0]]
		elif orientation == 4:
			return [[0, 1, 0], [1, 1, 1], [1, 0, 0]]
		elif orientation == 5:
			return [[1, 1, 0], [0, 1, 1], [0, 1, 0]]
		elif orientation == 6:
			return [[0, 0, 1], [1, 1, 1], [0, 1, 0]]
		else:
			return [[0, 1, 0], [1, 1, 0], [0, 1, 1]]


class PuzzleBoard:
	def __init__(self):
		self.board = self.init_board()
		self.pieces_placed = []

	def init_board(self):
		return [[0, 0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0, 0],
		        [0, 0, 0, 0, 0, 0, 0, 0]]

	'''
	override the copy method to make a deep copy of the object
	'''
	def __copy__(self):
		new_board = PuzzleBoard()
		for piece_placed in self.pieces_placed:
			new_board.pieces_placed.append(copy(piece_placed))
		new_board.board = [[0, 0, 0, 0, 0, 0, 0, 0],
		                   [0, 0, 0, 0, 0, 0, 0, 0],
		                   [0, 0, 0, 0, 0, 0, 0, 0],
		                   [0, 0, 0, 0, 0, 0, 0, 0],
		                   [0, 0, 0, 0, 0, 0, 0, 0],
		                   [0, 0, 0, 0, 0, 0, 0, 0],
		                   [0, 0, 0, 0, 0, 0, 0, 0],
		                   [0, 0, 0, 0, 0, 0, 0, 0]]
		for i in range(8):
			for j in range(8):
				new_board.board[i][j] = self.board[i][j]
		return new_board

	'''
	check if the piece fits in the location on the board
	'''
	def does_piece_fit(self, location, piece):
		x_location, y_location = location

		if (x_location > 5) or (y_location > 5):
			return False

		current_state = [self.board[x_location][y_location : y_location + 3],
		                 self.board[x_location + 1][y_location : y_location + 3],
		                 self.board[x_location + 2][y_location : y_location + 3]]

		for i in range(3):
			for j in range(3):
				if (current_state[i][j] + piece.state[i][j]) > 1:
					return False

		return True

	'''
	place the piece on the board at the specified location.
	'''
	def place_piece(self, location, piece):
		x_location, y_location = location
		# print("placing piece at {},{}".format(x_location, y_location))

		for i in range(3):
			for j in range(3):
				self.board[x_location + i][y_location + j] = self.board[x_location + i][y_location + j] + piece.state[i][j]

		self.pieces_placed.append((location, piece.orientation))


'''
get the next possible location on the board where a piece can be placed
'''
def next_location(curr):
	x_location, y_location = curr

	if (x_location == 5) and (y_location == 5):
		return (-1, -1)

	if y_location == 5:
		next_x = x_location + 1
		next_y = 0
	else:
		next_x = x_location
		next_y = y_location + 1

	# print("next computed location: {},{}".format(x_location, y_location))
	return (next_x, next_y)


'''
the main function to identify the solution
'''
def find_solution(board, location):
	# base case
	if location == (-1,-1):
		if len(board.pieces_placed) == 11:
			pprint(board.board)
			pprint(board.pieces_placed)
			exit(1)
		return

	for ornt in range(8):
		piece = PuzzlePiece(ornt)
		if board.does_piece_fit(location, piece):
			new_board = copy(board)
			new_board.place_piece(location, piece)
			find_solution(new_board, next_location(location))

	find_solution(board, next_location(location))


###############################################################################
########################### compute solution below ###########################
###############################################################################


board = PuzzleBoard()

location = (0, 0)
for ornt in range(8):
	piece = PuzzlePiece(ornt)
	if board.does_piece_fit(location, piece):
		new_board = copy(board)
		new_board.place_piece(location, piece)
		find_solution(new_board, next_location(location))
