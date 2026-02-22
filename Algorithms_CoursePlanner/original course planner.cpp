#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <vector>
#include <algorithm>

using namespace std;

// this struct will keep one course
// it has course number, title, and prerequisites
struct Crs {
    string num;
    string title;
    vector<string> pre;
};

// this function breaks a line into pieces using a comma
// for example: "CSCI100,Intro,CSCI200" -> ["CSCI100","Intro","CSCI200"]
vector<string> split(const string& s, char d) {
    vector<string> out;
    string item;
    stringstream ss(s);

    while (getline(ss, item, d)) {
        if (!item.empty())
            out.push_back(item);
    }
    return out;
}

// this function will read the csv file and load all courses
// it puts courses into a map so we can search later
void loadData(string fname, map<string, Crs>& crsMap) {
    ifstream fin(fname);
    if (!fin.is_open()) {
        cout << "error: cannot open file " << fname << endl;
        return;
    }

    string line;
    while (getline(fin, line)) {
        vector<string> parts = split(line, ',');

        if (parts.size() < 2) continue; 

        Crs c;
        c.num = parts[0];   // first thing is course number
        c.title = parts[1]; // second thing is course title

        // rest are prerequisites
        for (size_t i = 2; i < parts.size(); i++) {
            if (!parts[i].empty())
                c.pre.push_back(parts[i]);
        }

        // save course in map with course number as key
        crsMap[c.num] = c;
    }

    fin.close();
}

// this function shows all courses sorted alphabetically
// like in the sample schedule
void showList(const map<string, Crs>& crsMap) {
    vector<string> nums;
    for (auto const& p : crsMap) {
        nums.push_back(p.first);
    }
    sort(nums.begin(), nums.end());

    cout << "Here is a sample schedule:" << endl << endl;
    for (string n : nums) {
        cout << n << ", " << crsMap.at(n).title << endl;
    }
    cout << endl;
}

// this function shows info of one course
// it prints the number, title, and prerequisites
void showOne(const map<string, Crs>& crsMap, string num) {
    // making input uppercase so "csci400" works same as "CSCI400"
    transform(num.begin(), num.end(), num.begin(), ::toupper);

    auto it = crsMap.find(num);
    if (it == crsMap.end()) {
        cout << "Course " << num << " not found." << endl;
        return;
    }

    Crs c = it->second;
    cout << c.num << ", " << c.title << endl;

    if (c.pre.empty()) {
        cout << "Prerequisites: None" << endl;
    } else {
        cout << "Prerequisites: ";
        for (size_t i = 0; i < c.pre.size(); i++) {
            cout << c.pre[i];
            if (i < c.pre.size() - 1) cout << ", ";
        }
        cout << endl;
    }
    cout << endl;
}

// this function just shows the menu choices
void menu() {
    cout << endl;
    cout << "1. Load Data Structure." << endl;
    cout << "2. Print Course List." << endl;
    cout << "3. Print Course." << endl;
    cout << "9. Exit" << endl;
    cout << endl;
    cout << "What would you like to do? ";
}

int main() {
    map<string, Crs> crsMap; // this store all courses
    bool loaded = false;     // check if data is loaded or not
    int ch;                  // user choice

    cout << "Welcome to the course planner." << endl;

    do {
        menu();        // show menu
        cin >> ch;     // take user choice

        switch (ch) {
            case 1: {
                // ask user to type file name
                string fname;
                cout << "Enter file name: ";
                cin >> fname;

                // load data into map
                loadData(fname, crsMap);

                if (!crsMap.empty()) {
                    loaded = true;
                }
                break;
            }
            case 2:
                // print course list if data loaded
                if (loaded) {
                    showList(crsMap);
                } else {
                    cout << "Error: Please load course data first." << endl;
                }
                break;
            case 3:
                // print one course if data loaded
                if (loaded) {
                    string num;
                    cout << "What course do you want to know about? ";
                    cin >> num;
                    showOne(crsMap, num);
                } else {
                    cout << "Error: Please load course data first." << endl;
                }
                break;
            case 9:
                // exit program
                cout << "Thank you for using the course planner!" << endl;
                break;
            default:
                // invalid menu option
                cout << ch << " is not a valid option." << endl;
                break;
        }

    } while (ch != 9); // loop until user enters 9

    return 0;
}
