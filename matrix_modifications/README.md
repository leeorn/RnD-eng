# Introduction
In this folder, you can find my attempted solution for writing production c++ code to implement matrix transpose and matrix multiplication.

# Instructions
- First, make sure you're in your project's folder. From the terminal `cd <path/to/project/>`.
- If an include folder doesn't exist, create one - `mkdir include`.
- Move the library file, Nehardea-Leeor.h, inside the include folder `mv <old/path/Nehardea-Leeor.h> <path/to/prject/include/Nehardea-Leeor.h>`
- Lastly, include the library in the project and make sure to refer to it when building the project.

The tests (test/tests.cpp) in this directory serve as a client to the library, and can be used as a reference on how to include it. Additionally, the Makefile can also be used as a reference on how to compile and link the library.

### Build
To build this project, please keep the files and directories in the same order (also in the "Files" section below). If the files are zipped, unzip it first.
- To run the code, use the command `make run`. This will create the file _Nehardea-Leeor_ in the current directory and run it. The result will be shown in the terminal.
- To only compile the test file use the command `make tests`.
- To clean the object files and the executable run the command `make clean`.

# Files
### Folders
- `include`: Contains the header file of the library (Nehardea-Leeor.h).
- `test`: Contains the test files (.cpp).
### Files
- `Makefile`: A Makefile to build and run the code.
- `README.md`: This README file to explain my thought process using words.


# Explanation
As stated in the assignment prompt, the task is a bit vague in some ways. Therefore, I decided to support several types for the two required functions.<br>
Since I used templates, the implementation has to happen in the header file (evaluates at compile time). Thus, to use this new library, all that the client needs to do is include the header file (similar to the last include line in test/tests.cpp). <br>
I have decided to use vectors instead of arrays because vectors are easy, clean, and elegant to use, even when working with large matrices. With vectors, there is no need to create a unique or shared pointer like in arrays when working with large matrices. Additionally, it is very likely that the client is already using vectors prior to using the library since they can easily be resized, among other benefits. This makes them the go-to choice when working with matrices.

As a side note, overflow protection is *not* covered. It can be address by adding built-in functions (such as __builtin_(add/mul)_overflow for integer types, and other functions from the _cmath_ library for floating-point types).

### Code Evaluation
##### Matrix Transpose 
- Time complexity: O(N). 
- Space complexity: O(N).
"N" refers to the number of elements in the given matrix.

##### Matrix Multiplication
- Time complexity: O($MN^2$). 
- Space complexity: O(MK).
Dim(A) = M x N and Dim(B) = N x K, where A and B are matrices.


# Tests
The test file (test/tests.cpp) is an example for a client to the library. In this file I wrote a few tests to check the code correctness.<br>
I would have liked to use a coding framework (such as Google's gtest), but it requires installation. Thus, to keep things simple, I chose not to use it.


# Future Work
### Library optimization
This code can be optimized in several ways. Below are my suggestions:
- Multi-threading: Matrix multiplication and matrix transpose are great examples where multi-threading could help a lot. In these examples, each thread could take care of a small part and write the results in the new matrix.
- GPU: There is some overhead involved with using the GPU, yet, in terms of time, large matrices could benefit from it.
If both of the suggested solutions are implemented, then a few quick tests could result in a proxy of what matrix size should start using GPU (when available) and which one should only use multi-threading.

### Test improvement
To minimize the number of packages required to run the test code, I did not use any non-built-in packages. However, for more extensive and automated tests, we could use third-party C++ packages, such as BLAS, to compare our code's correctness and efficiency against BLAS's result. <br>
Furthermore, we could use Python and its library NumPy (with a C++ wrapper, for example) to quickly develop tests and automate comparisons. Python and NumPy are very popular and easy to use and can help test the code since the API is fairly simple, and Python code can be concise and clear.

Lastly, a testing framework (such as Google's gtest) could have helped with the testing process. But, again, to maintain simplicity and minimize installation requirements, it was not used in this case.
