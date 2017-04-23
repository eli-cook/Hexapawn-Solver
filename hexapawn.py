"""Hexapawn Solver for CS442P at Portland State

:author: Eli Cook
Collaborated with Kevin Midkiff on design strategy.
"""

import sys

# move offsets used to calculate new position
BLOCK_OFFSET = 1,0
CAPTURE_OFFSET = (1,1),(1,-1)

class Board:
	"""Definition of Board object
	"""
	def __init__(self, board, turn):
		self.board = board
		if(turn == "W"):
			self.turn = True
		else:
			self.turn = False

		# define length and width of board.	
		self.rows = len(board)
		self.cols = len(board[0])
	
	# toggles whose turn it is.
	def next_turn(self):
		self.turn = not self.turn

	# checks and finds all valid moves for a piece given its position and returns them.
	def check_place(self, row, col):
		results = []
		if self.turn:
			board_flip = -1
		else:
			board_flip = 1

		if self.turn:
			cap_piece = "p"
		else:
			cap_piece = "P"

		# using the offsets and symmetry of pawn movement, the movement can be calculated the same for each piece regardless of turn.
		# if statements check for off the board moves, collision, and capture requirements.
		right_capture = (row + (board_flip * CAPTURE_OFFSET[0][0])),(col + (board_flip * CAPTURE_OFFSET[0][1])) 
		if right_capture[0] >= 0 and right_capture[1] >= 0 and right_capture[0] < self.rows and right_capture[1] < self.cols and self.board[right_capture[0]][right_capture[1]] == cap_piece:
			results.append(right_capture)

		left_capture = (row + (board_flip * CAPTURE_OFFSET[1][0])),(col + (board_flip * CAPTURE_OFFSET[1][1])) 
		if left_capture[0] >= 0 and left_capture[1] >= 0 and left_capture[0] < self.rows and left_capture[1] < self.cols and self.board[left_capture[0]][left_capture[1]] == cap_piece:
			results.append(left_capture)

		block = (row + (board_flip * BLOCK_OFFSET[0])), (col + (board_flip * BLOCK_OFFSET[1]))
		if block[0] >= 0 and block[1] >= 0 and block[0] < self.rows and block[1] < self.cols and self.board[block[0]][block[1]] == ".":
			results.append(block)

		return results

	def move(self, current_posn, next_posn, undo=False):
		if not undo:
			#Move piece to new position
			self.board[next_posn[0]][next_posn[1]] = self.board[current_posn[0]][current_posn[1]]
			#Set previous position to empty
			self.board[current_posn[0]][current_posn[1]] = "."

			# check for win by promote and signal as needed.
			if self.turn:
				if next_posn[0] == 0:
					return True
			else:
				if next_posn[0] == self.rows - 1:
					return True
		else:
			#Undo move my moving next position back to current position
			self.board[current_posn[0]][current_posn[1]] = self.board[next_posn[0]][next_posn[1]]
			#If no diagonal move was made, then pawn just moved forward, no capture. Set position to empty
			if current_posn[1] == next_posn[1]:
				self.board[next_posn[0]][next_posn[1]] = "."
			#Set previous next position to opponents piece, as a capture took place
			else:
				if self.turn:
					piece = "p"
				else:
					piece = "P"
				self.board[next_posn[0]][next_posn[1]] = piece


def base_move(current_posn, next_posn):
	def do_move(board, undo=False):
		return board.move(current_posn, next_posn, undo)
	return do_move


def legal_moves(board):
	if board.turn:
		my_piece = "P"
	else:
		my_piece = "p"
	moves = []

	# finds each piece on the board given whose turn it is, and calls the check place function to obtain all valid moves
	# given a specific board configuration.
	for row in range(board.rows):
		for col in range(board.cols):
			if board.board[row][col] == my_piece:
				valid_posns = board.check_place(row, col)
				for next_posn in valid_posns:
					moves.append(base_move((row,col), next_posn))
	return moves

def board_value(board):
	# grab all valid moves
	moves = legal_moves(board)

	# if no moves exist, its a loss
	if not moves:
		return -1

	# assume a loss	
	max_val = -1

	# for each valid moves, recurse down the looking for the value of each move
	for m in moves:

		result = m(board)

		if result:
			val = 1
		else:
			# flip player's turn and recurse
			board.next_turn()
			# a loss for you is a win for me, use negative sign to achieve this
			val = - board_value(board)
			board.next_turn()

		# take the best solution
		max_val = max(max_val, val)

		# undo move and exit out
		m(board, undo=True)

		# win pruning
		if max_val == 1:
			break

	return max_val
	
def main():
	turn = None
	board = []
	
	# grab input from std in and set turn
	lines = sys.stdin.readlines()
	turn = lines[0].strip('\n')

	# create board from std in
	for line in lines[1:]:
		line = line.strip('\n')
		board.append(list(line))

	# create board object
	b = Board(board, turn)

	try:
		# call value function
		print(board_value(b))
	except Exception as e:
		print(e)


if __name__ == '__main__':
	main()