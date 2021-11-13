#include<iostream>
using namespace std;

int rome_number_to_number(string x){
	int result = 0;
	int len = x.length();
	for(int i = 0;i <= len;i++){
		char now = x[i];
		if(now == 'M'){
			result += 1000;
		}else if(now == 'C'){
			if(i + 1 == len){
				result += 100;
			}else if(x[i + 1] == 'M'){
				result -= 100;
			}else if(x[i + 1] == 'D'){
				result -= 100;
			}else{
				result += 100;
			}
		}else if(now == 'X'){
			if(i + 1 == len){
				result += 10;
			}else if(x[i + 1] == 'C'){
				result -= 10;
			}else if(x[i + 1] == 'L'){
				result -= 10;
			}else{
				result += 10;
			}
		}else if(now == 'I'){
			if(i + 1 == len){
				result += 1;
			}else if(x[i + 1] == 'X'){
				result -	= 1;
			}else if(x[i + 1] == 'V'){
				result -= 1;
			}else{
				result += 1;
			}
		}else if(now == 'D'){
			result += 500;
		}else if(now == 'C'){
			result += 100;
		}else if(now == 'L'){
			result += 50;
		}else if(now == 'X'){
			result += 10;
		}else if(now == 'V'){
			result += 5;
		}else if(now == 'I'){
			result += 1;
		}
	}
	return result;
}

string number_to_rome_number(int a){
	string result;
	while(a > 0){
		if(a-1000 >= 0){
			a-=1000;
			result+="M";
		}else if(to_string(a)[0] == '9'){
			int len = to_string(a).length();
			switch(len){
				case 1:
					a-=9;
					result+="IX";
					break;
				case 2:
					a-=90;
					result+="XC";
					break;
				case 3:
					a-=900;
					result+="CM";
					break;
				}
		}else if(to_string(a)[0] == '4'){
			int len = to_string(a).length();
			switch(len){
				case 1:
					a-=4;
					result+="IV";
					break;
				case 2:
					a-=40;
					result+="XL";
					break;
				case 3:
					a-=400;
					result+="CD";
					break;
				}
		}else if(a - 500 >= 0){
			a-=500;
			result+="D";
		}else if(a - 100 >= 0){
			a-=100;
			result+="C";
		}else if(a - 50 >= 0){
			a-=50;
			result+="L";
		}else if(a - 10 >= 0){
			a-=10;
			result+="X";
		}else if(a - 5 >= 0){
			a-=5;
			result+="V";
		}else if(a - 1 >= 0){
			a-=1;
			result+="I";
		}
	}
	return result;
}

int main(){
	string a, b;
	cin >> a >> b;
	int A = rome_number_to_number(a);
	int B = rome_number_to_number(b);
	int C = A - B;
	if (C == 0){
		cout << "ZERO";
	}else{
		cout << number_to_rome_number(C);
	}
	system("pause");
	return 0;
}