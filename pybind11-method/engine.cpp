#include<pybind11/pybind11.h>
#include <pybind11/stl.h>
#include<pybind11/functional.h>
#include<vector>
#include<algorithm>
#include <functional>

using namespace std;
namespace py = pybind11;

vector<int> bubble_sort_bind(vector<int> arr, const function<void(vector<int>,int,int)>& callback){
    int n = arr.size();
    for(int i = 0; i < n-1; i++){
        for(int j = 0; j < n - i - 1; j++){
            if(arr[j] > arr[j+1]){
                swap(arr[j],arr[j+1]);

                callback(arr,j,j+1);
            }
        }
    }
    return arr;
}


vector<int> selection_sort_bind(vector<int> arr, const function<void(vector<int>,int,int)> &callback){
    int n = arr.size();
    for(int i = 0; i < n; i++){
        int min_idx = i;
        for(int j = i+1; j < n; j++){
            if(arr[j] < arr[min_idx]){
                min_idx = j;
            }
        }
        if(min_idx != i){
            swap(arr[i], arr[min_idx]);
            callback(arr,i,min_idx);
        }
    }
    return arr;
}

vector<int> insertion_sort_bind(vector<int> arr, const function<void(vector<int>,int,int)>& callback){
    int n = arr.size();
    for(int i = 0; i < n; i++){
        int j = i;
        while(j > 0 && arr[j-1] > arr[j]){
            swap(arr[j-1], arr[j]);
            callback(arr,j-1,j);
            j--;
        }
    }
    return arr;
}

void merge(vector<int> &arr, int low, int mid, int high,const function<void(vector<int>,int,int)>& callback){
    vector<int> temp;
    int left = low;
    int right = mid + 1;
    while(left <= mid && right <= high){
        if(arr[left] <= arr[right]){
            temp.push_back(arr[left]);
            left++;
        }else{
            temp.push_back(arr[right]);
            right++;
        }
    }
    while(left <= mid){
        temp.push_back(arr[left]);
        left++;
    }
    while(right <= high){
        temp.push_back(arr[right]);
        right++;
    }
    for(int i = low; i <= high; i++){
        arr[i] = temp[i - low];
        callback(arr, i , -1);
    }
}

void mergeSort(vector<int> &arr, int low, int high, const function<void(vector<int>,int,int)>& callback){
    if(low == high) return;
    int mid = (low + high)/ 2;
    mergeSort(arr, low, mid, callback);
    mergeSort(arr, mid+1, high, callback);
    merge(arr, low, mid, high, callback);
}

vector<int> merge_sort_bind(vector<int> arr, const function<void(vector<int>,int,int)>& callback) {
    mergeSort(arr, 0, arr.size() - 1, callback);
    return arr;
}

//quicksort
int partitionF(vector<int> &arr, int low, int high,const function<void(vector<int>,int,int)>& callback){
    int pivot = arr[low];
    int i = low;
    int j = high;
    while(i < j){
        while(arr[i] <= pivot && i <= high){
            i++;
        }
        while(arr[j] > pivot && j >= low){
            j--;
        }
        if(i < j){
            swap(arr[i], arr[j]);
            callback(arr,i,j);
        }
    }
    swap(arr[low], arr[j]);
    return j;
}


void quickSort(vector<int> &arr, int low, int high, const function<void(vector<int>,int,int)>& callback){
    if(low < high){
        int partition = partitionF(arr, low, high,callback);
        quickSort(arr, low, partition-1, callback);
        quickSort(arr, partition+1, high, callback);
    }
}

vector<int> quick_sort_bind(vector<int> arr, const function<void(vector<int>,int,int)>& callback){
    quickSort(arr,0,arr.size()-1,callback);
    return arr;
}

PYBIND11_MODULE(sorting_engine, m){
    m.def("bubble_sort", &bubble_sort_bind,"A bubble sort with a Python callback");
    m.def("selection_sort", &selection_sort_bind, "Selection Sort");
    m.def("insertion_sort", &insertion_sort_bind, "Insertion Sort");
    m.def("merge_sort", &merge_sort_bind, "Merge Sort");
    m.def("quick_sort", &quick_sort_bind, "Quick Sort");
}
