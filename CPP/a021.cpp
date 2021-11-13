#include <iostream>
using namespace std;

int get_calculated_result(int a, char symbol, int b){
    if(symbol == '+'){
        pass
    }else if(symbol == '+'){
        pass
    }else if(symbol == '-'){
        pass
    }else if(symbol == '*'){
        pass
    }else if(symbol == '/'){
        pass
    }else{
        cout << "unidentifiable";
    }
}

int main(){
    string a_num[25];
    string b_num[25];
    int result[25];
    string a,b;
    char calculate;
    cin >> calculate;
    cin>>a>>b;
    for(int k=0;k<25;k++){
        a_num[k]="0";
        b_num[k]="0";
        result[k]=0;
    }
    for(int i=0;i<int(a.length()/2);i++){
        swap(a[i],a[a.length()-1-i]);
    }
    for(int j=0;j<int(b.length()/2);j++){
        swap(b[j],b[b.length()-1-j]);
    }
    int length_of_a = int(a.length()), length_of_b = int(b.length());
    for (int i = 0; i < 25 - length_of_a; i++)
    {
        a += "0";
    }
    for (int i = 0; i < 25 - length_of_b; i++)
    {
        b += "0";
    }
    for(int l=0;l<25;l++){
        a_num[l]= a[l];
        b_num[l]= b[l];
    }
    system("pause");
    return 0;`
}
