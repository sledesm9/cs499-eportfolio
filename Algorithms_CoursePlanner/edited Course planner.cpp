#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <vector>
#include <algorithm>
#include <cctype>
#include <limits>

using namespace std;

// Holds one course record
struct Crs {
    string num;
    string title;
    vector<string> pre;
};

// Trim spaces from both ends of a string
static string trim(const string& s) {
    size_t start = 0;
    while (start < s.size() && isspace(static_cast<unsigned char>(s[start]))) start++;

    size_t end = s.size();
    while (end > start && isspace(static_cast<unsigned char>(s[end - 1]))) end--;

    return s.substr(start, end - start);
}

// Uppercase a string (useful for course numbers)
static string toUpper(string s) {
    transform(s.begin(), s.end(), s.begin(),
              [](unsigned char c) { return static_cast<char>(toupper(c)); });
    return s;
}

// Split a line by delimiter
vector<string> split(const string& s, char d) {
    vector<string> out;
    string item;
    stringstream ss(s);

    while (getline(ss, item, d)) {
        item = trim(item);
        if (!item.empty()) out.push_back(item);
    }
    return out;
}

// Load courses into a map. Returns true if it loaded at least one course.
bool loadData(const string& fname, map<string, Crs>& crsMap) {
    ifstream fin(fname);
    if (!fin.is_open()) {
        cout << "Error: cannot open file " << fname << endl;
        return false;
    }

    crsMap.clear(); // if user reloads, start fresh

    string line;
    while (getline(fin, line)) {
        vector<string> parts = split(line, ',');

        // Must have at least course number + title
        if (parts.size() < 2) continue;

        Crs c;
        c.num = toUpper(parts[0]);  // normalize course number key
        c.title = parts[1];

        // Any extra fields are prerequisites
        for (size_t i = 2; i < parts.size(); i++) {
            string pre = toUpper(parts[i]);
            if (!pre.empty()) c.pre.push_back(pre);
        }

        crsMap[c.num] = c;
    }

    fin.close();

    if (crsMap.empty()) {
        cout << "Warning: file loaded but no valid course records were found." << endl;
        return false;
    }

    cout << "Data structure loaded successfully." << endl;
    return true;
}

// Print all courses in sorted order
// std::map is already ordered by key, so we can just iterate it
void showList(const map<string, Crs>& crsMap) {
    cout << "Here is a sample schedule:" << endl << endl;

    for (const auto& pair : crsMap) {
        cout << pair.first << ", " << pair.second.title << endl;
    }

    cout << endl;
}

// Print one course (title + prerequisites)
void showOne(const map<string, Crs>& crsMap, string num) {
    num = toUpper(trim(num));

    auto it = crsMap.find(num);
    if (it == crsMap.end()) {
        cout << "Course " << num << " not found." << endl << endl;
        return;
    }

    const Crs& c = it->second;
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

// Show the menu
void menu() {
    cout << endl;
    cout << "1. Load Data Structure." << endl;
    cout << "2. Print Course List." << endl;
    cout << "3. Print Course." << endl;
    cout << "9. Exit" << endl << endl;
    cout << "What would you like to do? ";
}

// Read a valid menu choice (prevents cin from getting stuck)
bool readMenuChoice(int& ch) {
    if (!(cin >> ch)) {
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        cout << "Please enter a number from the menu." << endl;
        return false;
    }

    // clear the rest of the line so getline works correctly later
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    return true;
}

int main() {
    map<string, Crs> crsMap;
    bool loaded = false;
    int ch = 0;

    cout << "Welcome to the course planner." << endl;

    do {
        menu();

        if (!readMenuChoice(ch)) {
            continue;
        }

        switch (ch) {
            case 1: {
                string fname;
                cout << "Enter file name: ";

                // allows spaces in file names (ex: "CS 499.csv")
                getline(cin, fname);
                fname = trim(fname);

                loaded = loadData(fname, crsMap);
                break;
            }

            case 2:
                if (loaded) {
                    showList(crsMap);
                } else {
                    cout << "Error: Please load course data first." << endl;
                }
                break;

            case 3:
                if (loaded) {
                    string num;
                    cout << "What course do you want to know about? ";
                    getline(cin, num);
                    showOne(crsMap, num);
                } else {
                    cout << "Error: Please load course data first." << endl;
                }
                break;

            case 9:
                cout << "Thank you for using the course planner!" << endl;
                break;

            default:
                cout << ch << " is not a valid option." << endl;
                break;
        }

    } while (ch != 9);

    return 0;
}
