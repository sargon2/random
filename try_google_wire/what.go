package main

import (
	"fmt"

	"github.com/google/wire"
)

type ThingThatHasDependencies struct {
	d *Dep
}

func NewThing(d *Dep) *ThingThatHasDependencies {
	return &ThingThatHasDependencies{
		d: d,
	}
}

func (t *ThingThatHasDependencies) doStuff() {
	t.d.msg = "asdf"
	fmt.Println(t.d.msg)
}

type Dep struct {
	msg string
}

func NewDep() *Dep {
	return &Dep{}
}

func InitThing() *ThingThatHasDependencies {
	panic(wire.Build(NewDep, NewThing))
}

func main() {
	thing := InitThing()
	thing.doStuff()
}
