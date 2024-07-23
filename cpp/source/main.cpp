#include "dep_injection/try_dep_injection.h"
#include "initialization.h"
#include "rvo.h"
#include <iostream>
#include <vector>

int main(int argc, char *argv[]) {
    // std::cout << "Hello World!" << std::endl;
    // tryStructCreation();
    // tryInitializing();
    try_dep_injection();

    int *intp;
    std::vector<int> intVector = {1, 2, 3};

    intp = intVector.data();
    return 0;
}
