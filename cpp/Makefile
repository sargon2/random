
.PHONY: *

default-target: all

%: build/%.cmake
	cmake -P "build/$@.cmake"
