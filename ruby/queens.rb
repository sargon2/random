class BoardState
	
	def putqueen(q, x, y)
		a = q.clone
		r = [x, y]
		a << r
		return a
	end

	def checkqueen(q, x, y)
		n = q.find { |j| hitsSquare(x, y, j[0], j[1]) }
		return false if n != nil
		return true
	end
		

	def hitsSquare(x1, y1, x2, y2)
		h = (x2 - x1).abs
		v = (y1 - y2).abs
		if x1 == x2 or y1 == y2 or h == v
			return true
		end
		return false
	end

	def printboard(q)
		board = [[]]
		(0..7).each { |i| board[i] = []; (0..7).each { |j| board[i][j] = 0 } }
		q.each do |j|
			board[j[0]][j[1]] = 1
		end
		board.each do |x|
			p x
		end
	end
	
	def initialize
		@solns = 0
	end

	def dostuff(q = [])
		if q.length == 8
			@solns += 1
			p "Solution: " + @solns.to_s
			printboard(q)
			return
		end
		x = q.length
		(0..7).each do |y|
			if(checkqueen(q, x, y))
				dostuff(putqueen(q, x, y))
			end
		end

	end

end

a = BoardState.new

a.dostuff
