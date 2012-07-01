#!/usr/local/bin/ruby

puts "asdfjkl".class # "String"
puts "asdfjkl".to_s # "asdfjkl"

class String;
	def to_s
		"asdf"
	end
end

puts "asdfjkl".to_s # "asdf"
puts "asdfjkl".class # "String"
puts "asdfjkl" # "asdfjkl"
