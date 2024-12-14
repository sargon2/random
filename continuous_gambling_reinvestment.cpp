#include <cstdio>
#include <cstdlib>
#include <time.h>
#include <iostream>

int main(int argc, char** argv) {
    srand (time(NULL));
    int num_wins = 0;
    int num_losses = 0;
    while(true) {
        double a = 1.0;

        while(true) {
            double wager_size = a/100;

            if(std::rand() % 2 == 0) {
                // Win
                a += wager_size;
            } else {
                // Lose
                a -= wager_size;
            }
            if(a <= 1e-300) {
                num_losses++;
                goto NEXT;
            }
            if(a >= 2.0) {
                num_wins++;
                goto NEXT;
            }
        }
NEXT:
        std::cout << "num_wins: " << num_wins << ", num_losses: " << num_losses << std::endl;
    }
}
