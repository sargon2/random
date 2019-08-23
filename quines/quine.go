package main

import "fmt"

func main() {
	b := string(rune(96))
	str := `package main

import "fmt"

func main() {
	b := string(rune(96))
	str := %s
	fmt.Printf(str, b+str+b)
}
`
	fmt.Printf(str, b+str+b)
}
