#include <iostream>
#include <vector>
#include <type_traits>
#include <random>
#include <time.h>
#include <chrono>

#include "Nehardea-Leeor.h"

// ###################### Suppot functions ######################

/*
 * Function to create a matrix shape row x col with random values. 
 * args:    - row: number of rows
 *          - col: number of columns
 *          - (optional) seed: to generete the semi-random values
 * Returns: 2D vector with random values.
 */
template <typename T>
std::vector<std::vector<T>> createRandMatrix(size_t row, size_t col, int seed = 0){
    std::vector<std::vector<T>> matrix(row, std::vector<T>(col));

    if(seed)
        srand(seed);
    else
        srand(time(NULL));

    int maxVal = 1000;

    if(std::is_same<T, int>::value){
        for(std::size_t r = 0; r < row; r++){
            for(std::size_t c = 0; c < col; c++){
                matrix[r][c] = rand() % maxVal;
            }
        }
    }

    else if(std::is_same<T, float>::value){
        for(std::size_t r = 0; r < row; r++){
            for(std::size_t c = 0; c < col; c++){
                matrix[r][c] = ((float) rand() / (float) RAND_MAX)* maxVal;
            }
        }
    }

    return matrix;
}

/*
 * Function to print a given matrix.
 * args:    Matrix to be printed
 * Returns: None
 */
template <typename T>
void printMatrix(const std::vector<std::vector<T>> &matrix){
    std::cout << std::endl;

    int rows = matrix.size();
    int cols = matrix[0].size();

    for(int r = 0; r < rows; r++){
        for(int c = 0; c < cols; c++){
            std::cout << matrix[r][c] << " "; 
        }
        std::cout << "\n";
    }
}

/*
 * Function to compare that the values of 2 matrices are the same. The matrices size is expected to be the same.
 * args:    two 2D matrices.
 * Returns: True if the values are the same. False else.
 */
template <typename T>
bool compareMatrcies(const std::vector<std::vector<T>> &matrixA, const std::vector<std::vector<T>> &matrixB){
    for(int i = 0; i < matrixA.size(); i++){
        for(int j = 0; j < matrixA[0].size(); j++){
            if(matrixA[i][j] != matrixB[i][j])
                return false;
        }
    }

    return true;
}


// ###################### TESTS ######################

/*
 * Test to check a simply small 3x3 matrix transpose (int)
 */
bool test1(bool printResult=false){
    std::vector<std::vector<int>> matrix{{1,2,3}, {4,5,6}, {7,8,9}};
    std::vector<std::vector<int>> matrixT = matrixTranspose(matrix);

    std::vector<std::vector<int>> expectedMatrixT{{1,4,7}, {2,5,8}, {3,6,9}};

    if(printResult){
        std::cout << "***********************" << std::endl;
        std::cout << "Test 1: The matrix before transpose is:"; 
        printMatrix(matrix);
        std::cout << "\n the calculated transpose matrix is:";
        printMatrix(matrixT);
        std::cout << "***********************" << std::endl;
    }

    return compareMatrcies(expectedMatrixT, matrixT);
}

/*
 * Test to check a simple 2x4 matrix transpose (int)
 */
bool test2(bool printResult=false){
    std::vector<std::vector<int>> matrix{{1,2,3,4}, {5,6,7,8}};
    std::vector<std::vector<int>> matrixT = matrixTranspose(matrix);

    std::vector<std::vector<int>> expectedMatrixT{{1,5}, {2,6}, {3,7}, {4,8}};

    if(printResult){
        std::cout << "***********************" << std::endl;
        std::cout << "Test 2: The matrix before transpose is:"; 
        printMatrix(matrix);
        std::cout << "\nthe transposed matrix is:";
        printMatrix(matrixT);
        std::cout << "***********************" << std::endl;
    }

    return compareMatrcies(expectedMatrixT, matrixT);
}

/*
 * Test to check a simple 2x1 matrix transpose (float)
 */
bool test3(bool printResult=false){
    std::vector<std::vector<float>> matrix{{1.5}, {7.9}};
    std::vector<std::vector<float>> matrixT = matrixTranspose(matrix);

    std::vector<std::vector<float>> expectedMatrixT{{1.5, 7.9}};

    if(printResult){
        std::cout << "***********************" << std::endl;
        std::cout << "Test 3: The matrix before transpose is:"; 
        printMatrix(matrix);
        std::cout << "\nthe transposed matrix is:";
        printMatrix(matrixT);
        std::cout << "***********************" << std::endl;
    }

    return compareMatrcies(expectedMatrixT, matrixT);
}

/*
 * Test to check a simple 1x2 matrix transpose (float)
 */
bool test4(bool printResult=false){
    std::vector<std::vector<float>> matrix{{50000.1, -3.14}};
    std::vector<std::vector<float>> matrixT = matrixTranspose(matrix);

    std::vector<std::vector<float>> expectedMatrixT{{50000.1}, {-3.14}};

    if(printResult){
        std::cout << "***********************" << std::endl;
        std::cout << "Test 4: The matrix before transpose is:"; 
        printMatrix(matrix);
        std::cout << "\nthe transposed matrix is:";
        printMatrix(matrixT);
        std::cout << "***********************" << std::endl;
    }

    return compareMatrcies(expectedMatrixT, matrixT);
}

/*
 * Test to check a simple 15x20 matrix transpose (float)
 */
void test5(bool printResult=false){
    std::vector<std::vector<float>> matrix = createRandMatrix<float>(15, 20, 3);
    std::vector<std::vector<float>> matrixT = matrixTranspose(matrix);

    if(printResult){
        std::cout << "***********************" << std::endl;
        std::cout << "Test 5: The matrix before transpose is:"; 
        printMatrix(matrix);
        std::cout << "\nthe transposed matrix is:";
        printMatrix(matrixT);
        std::cout << "\nits shape is:" << matrixT.size() << "x" <<  matrixT[0].size() << "\n";
        std::cout << "***********************" << std::endl;
    }
}

/*
 * 2 3x3 matrices multiplication (int)
 */
bool test6(bool printResult=false){
    std::vector<std::vector<int>> matrixA{{1,2,3}, {4,5,6}, {7,8,9}};
    std::vector<std::vector<int>> matrixB{{10,11,12}, {13,14,15}, {16,17,18}};
 
    std::vector<std::vector<int>> matrixResult = matrixMultiply(matrixA, matrixB);

    std::vector<std::vector<int>> expectedMatrix = {{84,90,96},{201,216,231},{318,342,366}};

    if(printResult){
        std::cout << "***********************" << std::endl;
        std::cout << "Test 6: MatrixA and MatrixB are below";
        printMatrix(matrixA);
        printMatrix(matrixB);
        std::cout << "\nTheir multiplication result is:";
        printMatrix(matrixResult);
        std::cout << "***********************" << std::endl;
    }

    return compareMatrcies(expectedMatrix, matrixResult);
}

/*
 * 1x2 & 2x3 matrix multiplication (float)
 */
bool test7(bool printResult=false){
    std::vector<std::vector<float>> matrixA{{0.1,2.4}};
    std::vector<std::vector<float>> matrixB{{10.1,11.0,12.2}, {13,14,15}};

    std::vector<std::vector<float>> matrixResult = matrixMultiply(matrixA, matrixB);

    std::vector<std::vector<float>> expectedMatrix = {{32.21,34.7,37.22}};

    if(printResult){
        std::cout << "***********************" << std::endl;
        std::cout << "Test 7: MatrixA and MatrixB are below";
        printMatrix(matrixA);
        printMatrix(matrixB);
        std::cout << "\nTheir multiplication result is:";
        printMatrix(matrixResult);
        std::cout << "***********************" << std::endl;
    }

    return compareMatrcies(expectedMatrix, matrixResult);
}

/*
 * 1x2 & 1x3 matrix multiplication (float).
 * Mismatched dimensions. Will terminate the code if this test is used (as expected).
 */
bool test8(bool printResult=false){
    std::vector<std::vector<float>> matrixA{{0.1,2.4}};
    std::vector<std::vector<float>> matrixB{{10.1,11.0,12.2}};

    std::vector<std::vector<float>> matrixResult = matrixMultiply(matrixA, matrixB);

    std::vector<std::vector<float>> expectedMatrix = {{32.21,34.7,37.22}};

    if(printResult){
        std::cout << "***********************" << std::endl;
        std::cout << "Test 8: MatrixA and MatrixB are below";
        printMatrix(matrixA);
        printMatrix(matrixB);
        std::cout << "\nTheir multiplication result is:";
        printMatrix(matrixResult);
        std::cout << "***********************" << std::endl;
    }

    return compareMatrcies(expectedMatrix, matrixResult);
}

// Generate random float matrices (size 50x50 and 50x100) and multiply them.
void test9(bool printResult=false){
    std::vector<std::vector<int>> matrixA = createRandMatrix<int>(50, 50, 1);
    std::vector<std::vector<int>> matrixB = createRandMatrix<int>(50, 100);

    std::vector<std::vector<int>> matrixResult = matrixMultiply(matrixA, matrixB);

    if(printResult){
        std::cout << "***********************" << std::endl;
        std::cout << "Test 9: MatrixA and MatrixB are below";
        printMatrix(matrixA);
        printMatrix(matrixB);
        std::cout << "\nTheir multiplication result is:";
        printMatrix(matrixResult);
        std::cout << "***********************" << std::endl;
    }
}

// *Warning* This function takes time to execute!
// Measure how long it takes to transpose a relatively large matrix
void test10(bool printResult=false){
    std::vector<std::vector<int>> matrix = createRandMatrix<int>(20000, 40000);

    auto start = std::chrono::high_resolution_clock::now();
    std::vector<std::vector<int>> matrixT = matrixTranspose(matrix);
    auto end = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    if(printResult){
        std::cout << "***********************" << std::endl;
        std::cout << "Test 10: it took (about) " << duration.count() / 1e6 << " seconds to transpose a matrix size " 
            << matrix.size() << "x" << matrix[0].size() << "\n";
        std::cout << "***********************" << std::endl;
    }
}

// *Warning* This function takes time to execute!
// Measure how long it takes to multiply two relatively large matrices
void test11(bool printResult=false){
    std::vector<std::vector<int>> matrixA = createRandMatrix<int>(1000, 2000, 7);
    std::vector<std::vector<int>> matrixB = createRandMatrix<int>(2000, 1000);

    auto start = std::chrono::high_resolution_clock::now();
    std::vector<std::vector<int>> matrixResult = matrixMultiply(matrixA, matrixB);
    auto end = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    if(printResult){
        std::cout << "***********************" << std::endl;
        std::cout << "Test 11: it took (about) " << duration.count() / 1e6 << " seconds to multiply the matrices\n";
        std::cout << "***********************" << std::endl;
    }
}


int main(){    
    if(test1() && test2() && test3() && test4() && test6() && test7()){
        std::cout << "\nPassed tests" << std::endl;
    }
    else{
        std::cout << "\nFailed tests" << std::endl;
    }

    return 0;
}