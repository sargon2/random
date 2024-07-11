#include <iostream>

using namespace std;

void tryInitializing() {
    int a;
    int b = 5;
    int c(6);
    int d{7};
    int e = {8};
    int f{};

    // cout << a << endl; // runtime error: uninitialized
    cout << b << endl;
    cout << c << endl;
    cout << d << endl;
    cout << e << endl;
    cout << f << endl;
}