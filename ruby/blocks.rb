# Exploring why the Ruby guys decided to make blocks anonymous parameters instead of normal parameters...

# Blocks as anonymous parameters with special syntax:
def asdf(n)
	p yield(n)
end
asdf(3) { |x| x*2 }

# Blocks as named anonymous parameters (actually a copy of the anonymous parameter):
def asdf2(n, &foo)
	p foo.call(n)
end
asdf2(3) { |x| x*2 }

# Blocks as normal parameters:
def asdf3(n, foo)
	p foo.call(n)
end
# We would like to do this:
#asdf2(3, { |x| x*2 })
# But, that doesn't parse.. instead, we have to do this:
asdf3(3, lambda { |x| x*2 })


# Nested blocks:
def asdf4(n)
	yield(n)
end
p asdf4(3) { |x| asdf4(x) { |y| y*2 }}
# Or, expanded...
p(asdf4(3) do |x|
	asdf4(x) do |y|
		y*2
	end
end)

# vs..
def asdf5(n, foo)
	foo.call(n);
end

p asdf5(3, lambda { |x| asdf5(x, lambda { |y| y*2 }) })
p asdf5(3, lambda do |x|
	asdf5(x, lambda do |y|
		y*2
	end)
end)
#Should be:
#asdf5(3, { |x| asdf5(x, { |y| y*2 }) })
#asdf5(3, { |x|
#	asdf5(x, { |y|
#		y*2
#	})
#})

# Or, with 3..
p asdf4(3) { |x| asdf4(x) { |y| asdf4(y) { |z| z*2 } } }

#asdf5(3, { |x| asdf5(x, { |y| asdf5(y, { |z| z*2 }) }) })
p asdf5(3, lambda { |x| asdf5(x, lambda { |y| asdf5(y, lambda { |z| z*2 }) }) })

# It is important to note that the only syntax being saved is the commas -- there are the same number of () and {} in each
