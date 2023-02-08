#include "reader.h"
#include <vector>

vector<pair<int,int>> convertToHandLandmarks(string stringLandmarks) {
    vector<pair<int,int>> landmarks(5);
    landmarks.reserve(5);

    size_t pos = 0;
    for (int i = 0; i < 5; i++) {
        size_t startX = stringLandmarks.find("X",pos) + 2;
        size_t endX = stringLandmarks.find("Y",startX) - 1;
        size_t startY = endX + 3;
        size_t endY = stringLandmarks.find("\n",startY);

        int x = stoi(stringLandmarks.substr(startX, endX-startX));
        int y = stoi(stringLandmarks.substr(startY, endY-startY));

        landmarks[i] = make_pair(x,y);

        pos = stringLandmarks.find("\t", endY + 2);
    }
    return landmarks;
}

int main(int argc, char **argv) {
    HandProcessor processor;

    while (1) {
    cout << "" << endl;
        auto start = chrono::high_resolution_clock::now();
        fstream file("../SharedMem.txt");
        string result;
        string buf;
        if (file.is_open()) {
            // keep reopening file since it's getting modified
            // get all 7 lines
            for (int i = 0; i < 7; i++) {
                getline(file, buf);
                result += buf + "\n";
            }
            file.close();
        }

        vector<pair<int,int>> landmarks;
        try {
            serial_data(10,5);
            landmarks = convertToHandLandmarks(result);
            processor.processHandLandmarks(landmarks);
        } catch (exception e) {
            cout << "Error: " << e.what() << endl;
            continue;
        }
    }
    return 0;
}