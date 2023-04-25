#pragma once
#include <vector>
#include <type_traits>
#include <stdexcept>
 
/*
 * Function to transpose a 2D vector (matrix).
 * args:    2D vector to be transposed (shape MxN). The vector's type is expected to be an arithmetic type.
 * Returns: A transpose 2D vector (shape NxM).
 */
template <typename T>
std::vector<std::vector<T>> matrixTranspose(const std::vector<std::vector<T>> &matrix){
    static_assert(std::is_arithmetic<T>::value, "T must be a number type.");

    std::size_t rows = matrix.size();
    std::size_t cols = matrix[0].size();

    std::vector<std::vector<T>> matrixTrans(cols, std::vector<T>(rows));

    for(std::size_t r = 0; r < rows; r++){
        for(std::size_t c = 0; c < cols; c++){
            matrixTrans[c][r] = matrix[r][c];
        }
    }

    return matrixTrans;
}

/*
 * Function to do 2 matrices multiplication.
 * args:    Two 2D vectors (matrixA matrixB); the two matrices to be multiplied. Their type is expected to be an arithmetic type.
 * Returns: 2D vector with the result of the multiplication of the two given matrices.
 */
template <typename T>
std::vector<std::vector<T>> matrixMultiply(const std::vector<std::vector<T>> &matrixA, const std::vector<std::vector<T>> &matrixB){
    static_assert(std::is_arithmetic<T>::value, "T must be a number type.");
    if(matrixA[0].size() != matrixB.size()){
        throw std::invalid_argument("Size mismatch. Number of columns in matrixA is not equal to the number of rows in matrixB.");
    }

    std::vector<std::vector<T>> newMatrix(matrixA.size(), std::vector<T>(matrixB[0].size()));

    for(std::size_t i = 0; i < matrixA.size(); i++){
        for(std::size_t j = 0; j < matrixB[0].size(); j++){
            T cur_sum = 0;
            for(std::size_t k = 0; k < matrixA[0].size(); k++){
                cur_sum += matrixA[i][k] * matrixB[k][j];
            }
            newMatrix[i][j] = cur_sum;
        }
    }
    
    return newMatrix;
}