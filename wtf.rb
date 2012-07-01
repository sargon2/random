#!/usr/local/bin/ruby

puts "asdfjkl".class # "String"
puts "asdfjkl".to_s # "asdfjkl"

def String::to_s
	"asdf"
end

puts "asdfjkl".to_s # "asdfjkl"
puts "asdfjkl".class # "asdf"
puts "asdfjkl" # "asdfjkl"
