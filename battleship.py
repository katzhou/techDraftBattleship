import urllib, json

def main():
	url="https://student.people.co/api/challenge/battleship/f0965ac910a1/boards"
	response=urllib.urlopen(url)
	data=json.load(response)
	for board in data:
		if board["is_test"]:
			if board["board_id"] == "test_board_1":
				run_board(board)

def run_board(board):
	board_url=board["url"]
	if board["is_finished"]:
		print "board " + board["board_id"] + " is finished"
		return

	#time to shoot it up
	#internal matrix, 0 = unshot, 1 = miss, 2 = hit
	board_matrix=[[0 for _ in xrange(11)] for _ in xrange(11)]

	#length positions [2,3,3,4,5]
	hit_ships=[0 for _ in xrange(5)]
	
	#let's play some checkers
	cRow=1
	cCol=1
	last_hit=0

	hit_counter=0
	#dummy hit everything method for first submission
	for r in xrange(10):
		for c in xrange(10):
			shot_url="https://student.people.co/api/challenge/battleship/f0965ac910a1/boards/"+board["board_id"]+"/"+get_loc(r+1,c+1)
			print shot_url
			response=urllib.urlopen(shot_url)
			data=json.load(response)
			if data["is_finished"]:
				hit_counter=hit_counter+1
				if hit_counter==5:
					print "done"
					return
	'''
	while cRow + 2 < 11:
		while cCol + 2 < 11:
			if board_matrix[cRow][cCol]==0:
				shot_url="https://student.people.co/api/challenge/battleship/f0965ac910a1/boards/"+board["board_id"]+"/"+get_loc(cRow,cCol)
				response=urllib.urlopen(shot_url)
				data=json.load(response)
				if data["is_hit"]:
					board_matrix[cRow][cCol] = 2
					last_hit=1
				else:
					board_matrix[cRow][cCol] = 1'''

def get_loc(row,col):
	return chr(row-1 + ord('A')) + str(col)

if __name__=="__main__":
	main()