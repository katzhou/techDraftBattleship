import urllib, json

hit_counter=0
board_matrix=[]

def main():
	url="https://student.people.co/api/challenge/battleship/f0965ac910a1/boards"
	response=urllib.urlopen(url)
	data=json.load(response)
	for board in data:
		if board["is_finished"]==False:
			if board["is_test"]==False:
				print "Now shooting up " + board["board_id"]
				run_board(board)

def run_board(board):
	global hit_counter,board_matrix

	board_url=board["url"]
	if board["is_finished"]:
		print "board " + board["board_id"] + " is finished"
		return

	#time to shoot it up
	#internal matrix, 0 = unshot, 1 = miss, 2 = hit
	board_matrix=[[0 for _ in xrange(11)] for _ in xrange(11)]
	
	#let's play some checkers
	for row in xrange(1,11):
		#even or odd for checkerboard pattern
		if row % 2 == 0:
			col=1
		else:
			col=2

		while col + 2 < 11:
			if board_matrix[row][col]==0:
				data = shoot(row,col,board)
				populate_matrix_and_check_finish(data,row,col)

				if board_matrix[row][col]==2:
					#shoot left and right
					if col != 1:
						#check if left is hit.  If not, fiya
						if board_matrix[row][col-1]==0:
							currdata=shoot(row,col-1,board)
							populate_matrix_and_check_finish(currdata,row,col-1)
					if col+1<11:
						if board_matrix[row][col+1]==0:
							currdata=shoot(row,col+1,board)
							populate_matrix_and_check_finish(currdata,row,col+1)
					#shoot up and down
					if row != 1:
						#check if up is hit.  If not, fiya
						if board_matrix[row-1][col]==0:
							currdata=shoot(row-1,col,board)
							populate_matrix_and_check_finish(currdata,row-1,col)
					if row+1<11:
						currdata=shoot(row+1,col,board)
						populate_matrix_and_check_finish(currdata,row+1,col)
			col = col + 2

def populate_matrix_and_check_finish(data,row,col):
	global hit_counter,board_matrix
	ret = False
	if data["is_hit"]:
		if data["is_finished"]:
			hit_counter = hit_counter+1
			if hit_counter==5:
				return True
		board_matrix[row][col] = 2
	else:
		board_matrix[row][col] = 1

def shoot(row,col,board):
	loc=chr(row-1 + ord('A')) + str(col)

	print "shooting at " + loc
	shot_url="https://student.people.co/api/challenge/battleship/f0965ac910a1/boards/"+board["board_id"]+"/"+loc
	response=urllib.urlopen(shot_url)
	return json.load(response)

if __name__=="__main__":
	main()