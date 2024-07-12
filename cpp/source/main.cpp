#include "dep_injection/try_dep_injection.h"
#include "initialization.h"
#include "rvo.h"
#include <iostream>

int main(int argc, char *argv[]) {
    // std::cout << "Hello World!" << std::endl;
    // tryStructCreation();
    // tryInitializing();
    try_dep_injection();
    return 0;
}
