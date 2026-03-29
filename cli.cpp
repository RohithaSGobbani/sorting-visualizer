#include<bits/stdc++.h>
// #include <iostream> // Needed for cout and endl
#include <vector>
using namespace std;

int main(int argc, char* argv[]){
    vector<int> data;
    for(int i = 1; i < argc; ++i){
        data.push_back(stoi(argv[i]));
    }
    int n = data.size();
    for(int i = 0; i < n; i++){
        cout << data[i] << " ";
    }
    cout << endl;
    return 0;
}
