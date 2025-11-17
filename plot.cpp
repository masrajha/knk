#include "matplotlibcpp.h"
#include <vector>

namespace plt = matplotlibcpp;

int main() {
    std::vector<double> x = {1, 2, 3, 4, 5};
    std::vector<double> y = {2, 4, 1, 5, 3};

    plt::plot(x, y, "ro-"); // Style garis merah dengan titik bulat
    plt::xlabel("Sumbu X");
    plt::ylabel("Sumbu Y");
    plt::title("Contoh Plot dengan Matplotlib-cpp");
    plt::show();
    plt::save("./plot.png"); // Simpan sebagai gambar

    return 0;
}