#include<bits/stdc++.h>
#include <vector>
using namespace std;

void send_to_python(const vector<int> &arr, int blue_idx, int red_idx){
    int n = arr.size();
    for(int i = 0; i < n; i++){
        cout << arr[i] << (i == n - 1 ? "" : ",");
    }
    cout << "|" << blue_idx << "," << red_idx << endl;
}

int main(int argc, char* argv[]){
    vector<int> data;
    for(int i = 1; i < argc; ++i){
        data.push_back(stoi(argv[i]));
    }
    int n = data.size();
    for(int i = 0; i < n - 1; i++){
        for(int j = 0; j < n-i-1; j++){
            if(data[j] > data[j+1]){
                swap(data[j],data[j+1]);
                send_to_python(data, j, j+1);
            }
        }
    }
    return 0;
}
