#include<bits/stdc++.h>
using namespace std;

int main(){
    int a_num[25];
    int b_num[25];
    int sum[25];
    int start;
    int carry = 0;
    int i;
    string a,b;
    char calculate;
    cin>>a>>b;
    for(int k=0;k<25;k++){
        a_num[k]=0;
        b_num[k]=0;
        sum[k]=0;
    }
    for(int i=0;i<(int)a.length()/2;i++){
        swap(a[i],a[a.length()-1-i]);
    }
    for(int j=0;j<(int)b.length()/2;j++){
        swap(b[j],b[b.length()-1-j]);
    }
    for(int l=0;l<a.length();l++){
        a_num[l]= a[l]-'0';
    }
    for(int l=0;l<b.length();l++){
        b_num[l]= b[l]-'0';
    }
    for(int i;i<25;i++){
        sum[i]=a_num[i]+b_num[i]+carry;
        if(sum[i]>=10){
            carry = 1;
            sum[i]-=10;
        }else{
            carry = 0;
        }
    }/*
    for(int i=0;i<=24;i++){
        if(sum[i] !=  0){
            start = i;
            break;
        }
    }*/
    cout<<i<<endl;
    for(int i=start;i>=0;i--){
        cout<<sum[i];
    }
    return 0;
}
