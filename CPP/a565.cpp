#include<bits/stdc++.h>
using namespace std;

int main()
{
	int pairs;
	int inputs;
	string situation;
	int waitingLine = 0;
	cin >> inputs;
	for (int i = 0; i < inputs; ++i)
	{	
		pairs = 0;
		waitingLine = 0;
		cin >> situation;
		for (int j = 0; j < situation.length(); ++j)
		{
			char nowChar = situation[j];
			if (nowChar == '.'){
				continue;
			} else if (nowChar == 'p'){
				waitingLine += 1;
			} else if (nowChar == 'q' and waitingLine != 0){
				waitingLine -= 1;
				pairs += 1;
			}
		}
		cout << pairs << endl;
	}
	return 0;
}