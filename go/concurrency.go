package main

import "fmt"
import "time"

func main() {
	var num_workers = 100
	var final_count int = 0
	myChan := make(chan int)

	// Start workers
	for i := 0; i < num_workers; i++ {
		go func() {
			time.Sleep(1 * time.Second)
			final_count += 1
			myChan <- 0
		}()
	}

	// Wait for all of them to finish
	for i := 0; i < num_workers; i++ {
		<-myChan
	}

	fmt.Println(final_count)
}
