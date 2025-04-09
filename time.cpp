#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <random>
#include <string>
#include <ctime>

// Function to test nested loops performance (0 to 10000)
void testNestedLoops() {
    std::cout << "Testing nested loops performance..." << std::endl;
    
    
    // Start timing
    auto start = std::chrono::high_resolution_clock::now();
    
    // Nested loops with calculations
    long long total = 0;
    for (int i = 0; i < 10000; i++) {
        for (int j = 0; j < 10000; j++) {
            total += (i * j + std::rand() % 11);
        }
    }
    
    // End timing
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    
    std::cout << "Résultat final : " << total << std::endl;
    std::cout << "Temps d'exécution : " << elapsed.count() << " secondes" << std::endl;
}

// Function to create a large test file with random content
void createLargeTestFile(const std::string& filename, size_t sizeMB) {
    std::cout << "Creating large test file (" << sizeMB << "MB)..." << std::endl;
    
    std::ofstream file(filename, std::ios::binary);
    if (!file) {
        std::cerr << "Error: Could not create file " << filename << std::endl;
        return;
    }
    
    // Setup random generator
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(32, 126); // Printable ASCII
    
    const size_t bufferSize = 8192;
    std::vector<char> buffer(bufferSize);
    size_t bytesToWrite = sizeMB * 1024 * 1024;
    
    while (bytesToWrite > 0) {
        size_t currentWriteSize = std::min(bytesToWrite, bufferSize);
        
        // Fill buffer with random characters
        for (size_t i = 0; i < currentWriteSize; i++) {
            buffer[i] = static_cast<char>(dist(gen));
        }
        
        file.write(buffer.data(), currentWriteSize);
        bytesToWrite -= currentWriteSize;
    }
    
    file.close();
    std::cout << "Large test file created successfully." << std::endl;
}

// Function to test file reading performance
void testFileReading(const std::string& filename) {
    std::cout << "Testing file reading performance..." << std::endl;
    
    // Start timing
    auto start = std::chrono::high_resolution_clock::now();
    
    // Open and read file
    std::ifstream file(filename, std::ios::binary);
    if (!file) {
        std::cerr << "Error: Could not open file " << filename << std::endl;
        return;
    }
    
    // Read entire file content
    std::string content((std::istreambuf_iterator<char>(file)),
                         std::istreambuf_iterator<char>());
    
    file.close();
    
    // End timing
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    
    std::cout << "Lecture terminée. Taille : " << content.size() << " caractères" << std::endl;
    std::cout << "Temps de lecture : " << elapsed.count() << " secondes" << std::endl;
}

int main() {
    // Test nested loops performance
    testNestedLoops();
    
    std::cout << "\n----------------------------------------\n" << std::endl;
    
    
    std::cout << "\n----------------------------------------\n" << std::endl;
    
    // Test file reading performance
    testFileReading("FichierTest.txt");
    
    return 0;
}
