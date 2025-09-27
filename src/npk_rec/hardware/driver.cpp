#include "driver.h"

namespace npk_rec {
    Driver::Driver(const std::string &filename) : outFile()
    {
        outFile.open(filename, std::ios::app);
        // Note: caller can check stream state by attempting a write and checking return code
    }

    Driver::~Driver() {
        if (outFile.is_open()) {
            outFile.close();
        }
    }

    int Driver::writeRow(const std::string &timestamp, const int N, const int P, const int K) {
        if (!outFile.is_open()) {
            return 1; // File not open
        }

        outFile << timestamp << "," << N << "," << P << "," << K << "\n";

        if (outFile.fail()) {
            return 2; // Write failed
        }

        return 0; // Success
    }

} // namespace npk_rec