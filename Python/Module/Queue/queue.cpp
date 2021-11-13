#include <iostream>
using namespace std;

class Queue{
	public:
		int length;
		int index;
		int data;
		Queue(int L){
			length = L;
			int data[L];
		}
		void push(int number){
			data[index] = number;
			index += 1;
		}
		int pop(){
			if(index >= 0){
				result = data[index];
				index -= 1;
			}else{
				result = false;
			}
			return result;
		}
		int now(){
			return index;
		}
};

int main(){
	q Queue(15);
}