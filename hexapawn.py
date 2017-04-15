"""Hexapawn Solver for CS442P at Portland State

:author: Eli Cook
"""

import sys

def legal_moves(posn, turn):
	return None

def posn_value(posn, turn):
	moves = legal_moves(posn, turn)
	if moves is None:
		return -1
	max_val = -1
	for m in moves:
		posn_prime, result = m(posn)
		if result:
			val = 1
		else:
			val = - posn_value(posn_prime)
		max_val = max(max_val, val)

		if max_val == 1:
			break
	return max_val
	
def main():
	turn = None
	board = []
	
	lines = sys.stdin.readlines()
	turn = lines[0].strip('\n')

	for line in lines[1:]:
		line = line.strip('\n')
		board.append(list(line))
	print(board)


if __name__ == '__main__':
	main()