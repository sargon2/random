
div_array = []

(2..ARGV[0].to_i).each do |i|
	s = Math.sqrt(i)
	isprime = true
	for j in div_array 
		break if j > s
		if i % j == 0
			isprime = false
			break
		end
	end
	if isprime
		div_array << i
		p i
	end
end
