#ifndef NPK_DRIVER_H
#define NPK_DRIVER_H

#include <fstream>
#include <string>

namespace npk_rec {
    class Driver {
        public:
            Driver(const std::string &filename); // Constructor to open the file
            ~Driver(); // Destructor to close the file if open
            // Writes NPK data to file, with timestamp. Returns 0 on success, non-zero on failure.
            int writeRow(const std::string &timestamp, const int N, const int P, const int K);

        private:
            std::ofstream outFile; // Output file stream
    };
}

#endif // NPK_DRIVER_H