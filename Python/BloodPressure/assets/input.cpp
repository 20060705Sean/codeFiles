#include <iostream>
#include <fstream>
#define size 10
using namespace std;
int main(){
	ifstream MyReadFile("assets/bld.csv");
	string contents;
	string myText;
	while (getline(MyReadFile, myText)){
		contents += myText + "\n";
	}
	cout << contents<<endl;
	MyReadFile.close();
	
	cin >> myText;
	ofstream MyFile("assets/bld.csv");
	MyFile << contents;
	MyFile << myText <<endl;
	MyFile.close();
	return 0;
}