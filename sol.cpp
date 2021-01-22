#include <set>
#include <stack>
#include <string>
#include <vector>
#include <cstring>
#include <iostream>
#include <algorithm>
using namespace std;
const int maxN=1e3+10;
typedef pair<int, int> pii;

struct tube {
    int len;
    string block[5]; 
    
    tube(): len(0) { for (int i=0;i<4;i++) block[i]=""; };

    int last() { return 4-len; }

    int same() {
        int cnt=1;

        for (int i=len;i>=2;i--)
            if (block[len]==block[len-1])
                cnt++;
        return cnt;
    }
    
    string pop() {  return block[len--]; }

    string top() { return block[len]; }

    void push(string x) { block[++len]=x; }
    
    void print() {
        for (int i=1;i<=len;i++)
            cout << block[i] << ' ';
        puts("");
    }

    bool empty() { return !len; }

    bool finish() {
        if (!len) return true;
        if (len && len!=4) return false;
        for (int i=1;i<=3;i++)
            if (block[i]!=block[i+1])
                return false;
        return true;
    }

    bool operator < (const tube &rhs) const {
        if (len!=rhs.len) return len<rhs.len;
        for (int i=1;i<=len;i++) {
            if (block[i]!=rhs.block[i]) {
                if (block[i].size()==rhs.block[i].size()) return block[i]<rhs.block[i];
                else return block[i].size()<rhs.block[i].size();
            }
        }
        return true;
    }
};

int n, m, idx=1;
tube tubes[maxN];
set<string> vis;
stack<pii> ans;

bool check(tube tmp[]) {
    for (int i=1;i<=idx;i++) {
        if (!tmp[i].finish())
            return false;
    }
    return true;
}

string hash_tube(tube tmp[]) {
    tube arr[maxN];
    string str;

    for (int i=1;i<=idx;i++)
        arr[i]=tmp[i];
    
    sort(arr, arr+idx+1);
 
    for (int i=1;i<=idx;i++)
        for (int j=1;j<=arr[i].len;j++)
            str+=arr[i].block[j];
    
    return str;    
}

bool dfs(tube tmp[]) {
    string _hash=hash_tube(tmp);
    
    if (vis.find(_hash)!=vis.end()) return false;
    if (check(tmp)) return true;

    vis.insert(_hash);

    for (int i=1;i<=idx;i++) {
        if (!tmp[i].empty()) {
            for (int j=1;j<=idx;j++) {
                if (i!=j) {
                    int cnt=0;

                    if ((tmp[j].empty()) || (tmp[j].last() && tmp[i].top()==tmp[j].top() && tmp[i].same()<=tmp[j].last())) {
                        while (!tmp[i].empty() && (tmp[j].empty() || (tmp[i].top()==tmp[j].top() && tmp[j].last())))
                            cnt++, tmp[j].push(tmp[i].pop());
                        
                        if (dfs(tmp)) {
                            ans.push(make_pair(i, j));
                            return true;
                        }
                        
                        while (cnt--) tmp[i].push(tmp[j].pop());
                    }
                }
            }
        }
    }
    return false;
}

int main() {
    while (cin >> n >> m) {
        if (tubes[idx].len==4) idx++;
        while (m--)
            tubes[idx].push(to_string(n));
    } idx+=2, dfs(tubes);
    
    while (!ans.empty()) {
        int x=ans.top().first, y=ans.top().second; ans.pop();
        
        if (!ans.empty()) {
            if (x==ans.top().second && y==ans.top().first) ans.pop();
            else cout << ans.top().first << ' ' << ans.top().second << '\n';
        }
    }
}
