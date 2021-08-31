#include <iostream>
#include <cmath>
int main() {
    long int hours,minutes;char dumbchar;std::cin >> hours >> dumbchar >> minutes;
    float cal = abs(6*minutes - 30*hours - minutes/2);
    float rst = (cal > 180) ? 360 - cal :cal;
    std::cout<<rst;
    for(int i=1;i<=5;i++){std::cout<<i;}
}