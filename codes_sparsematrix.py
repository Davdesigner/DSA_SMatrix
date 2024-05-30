import os
import sys
class SparseMatrix:
    """
    A class to represent a sparse matrix using a dictionary of dictionaries.
    """
    def __init__(self, rows, cols):
        """
        Initialize a sparse matrix.

        Parameters:
        rows (int): Number of rows in the matrix.
        cols (int): Number of columns in the matrix.
        """
        self.rows = rows
        self.cols = cols
        self.data = {}  # Store the matrix as a dictionary of dictionaries for sparse representation

    @staticmethod
    def from_file(file_path):
        """
        Create a SparseMatrix instance from a file.

        Parameters:
        file_path (str): Path to the input file.

        Returns:
        SparseMatrix: An instance of SparseMatrix with data from the file.

        Raises:
        ValueError: If the file format is incorrect.
        """
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]

        try:
            rows = int(lines[0].split('=')[1])
            cols = int(lines[1].split('=')[1])
        except (IndexError, ValueError):
            raise ValueError("Input file has wrong format")
        
        matrix = SparseMatrix(rows, cols)

        for line in lines[2:]:
            try:
                row, col, value = map(int, line[1:-1].split(','))
            except ValueError:
                raise ValueError("Input file has wrong format")
            matrix.set_element(row, col, value)

        return matrix

    def get_element(self, row, col):
        """
        Get the value of the element at the specified position.

        Parameters:
        row (int): Row index of the element.
        col (int): Column index of the element.

        Returns:
        int: Value of the element at the specified position, or 0 if not set.
        """
        return self.data.get(row, {}).get(col, 0)

    def set_element(self, row, col, value):
        """
        Set the value of the element at the specified position.

        Parameters:
        row (int): Row index of the element.
        col (int): Column index of the element.
        value (int): Value to set at the specified position.
        """
        if row not in self.data:
            self.data[row] = {}
        self.data[row][col] = value  # Setting the value in the sparse representation

    def add(self, matrix):
        """
        Add another sparse matrix to this matrix.

        Parameters:
        matrix (SparseMatrix): Another sparse matrix to add.

        Returns:
        SparseMatrix: A new SparseMatrix instance representing the sum.

        Raises:
        ValueError: If the dimensions of the matrices do not match.
        """
        if self.rows != matrix.rows or self.cols != matrix.cols:
            raise ValueError("Matrices must have the same dimensions for addition to perform")

        result = SparseMatrix(self.rows, self.cols)

        for row in self.data:
            for col in self.data[row]:
                result.set_element(row, col, self.get_element(row, col))

        for row in matrix.data:
            for col in matrix.data[row]:
                result.set_element(row, col, result.get_element(row, col) + matrix.get_element(row, col))

        return result

    def subtract(self, matrix):
        """
        Subtract another sparse matrix from this matrix.

        Parameters:
        matrix (SparseMatrix): Another sparse matrix to subtract.

        Returns:
        SparseMatrix: A new SparseMatrix instance representing the difference.

        Raises:
        ValueError: If the dimensions of the matrices do not match.
        """
        if self.rows != matrix.rows or self.cols != matrix.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction to perform")

        result = SparseMatrix(self.rows, self.cols)

        for row in self.data:
            for col in self.data[row]:
                result.set_element(row, col, self.get_element(row, col))

        for row in matrix.data:
            for col in matrix.data[row]:
                result.set_element(row, col, result.get_element(row, col) - matrix.get_element(row, col))

        return result

    def multiply(self, matrix):
        """
        Multiply this matrix with another sparse matrix.

        Parameters:
        matrix (SparseMatrix): Another sparse matrix to multiply with.

        Returns:
        SparseMatrix: A new SparseMatrix instance representing the product.

        Raises:
        ValueError: If the number of columns in this matrix does not match the number of rows in the other matrix.
        """
        if self.cols != matrix.rows:
            raise ValueError("Number of columns in the first matrix must be equal to the number of rows in the second matrix for multiplication to perform")

        result = SparseMatrix(self.rows, matrix.cols)

        for row in self.data:
            for col in range(matrix.cols):
                sum_product = 0
                for k in range(self.cols):
                    sum_product += self.get_element(row, k) * matrix.get_element(k, col)
                if sum_product != 0:
                    result.set_element(row, col, sum_product)

        return result

    def __str__(self):
        """
        Get a string representation of the sparse matrix.

        Returns:
        str: String representation of the matrix.
        """
        result = f"rows={self.rows}\ncols={self.cols}\n"
        for row in self.data:
            for col in self.data[row]:
                result += f"({row}, {col}, {self.data[row][col]})\n"
        return result


def prompt_user():
    """
    Prompt the user for input and perform the specified matrix operation.

    The function asks the user to input the operation (add, subtract, multiply)
    and the paths to the two matrix files. It then performs the specified operation
    and saves the result in a file in the 'sample_results' directory.
    """
    operation = input("Enter the operation (add, subtract, multiply): ").strip().lower()
    first_path = input("Enter the path for the first matrix file: ").strip()
    second_path = input("Enter the path for the second matrix file: ").strip()

    try:
        matrix1 = SparseMatrix.from_file(first_path)
        matrix2 = SparseMatrix.from_file(second_path)

        if operation == 'add':
            result = matrix1.add(matrix2)
        elif operation == 'subtract':
            result = matrix1.subtract(matrix2)
        elif operation == 'multiply':
            result = matrix1.multiply(matrix2)
        else:
            print("Invalid operation")
            return

        # Define the output file path
        sparse_matrix = 'sparse_matrix'
        sample_results = os.path.join(sparse_matrix, 'sample_results')

        # Ensure sample_results directory exists
        os.makedirs(sample_results, exist_ok=True)

        # Generate output file name based on input file names and operation
        first_file_name = os.path.basename(first_path)
        second_file_name = os.path.basename(second_path)
        output_file_name = f"{os.path.splitext(first_file_name)[0]}_{operation}_{os.path.splitext(second_file_name)[0]}_result.txt"
        output_file_path = os.path.join(sample_results, output_file_name)


        # Save the result to the output file
        with open(output_file_path, 'w') as file:
            file.write(str(result))

        print(f"Result saved to {output_file_path}")

    except Exception as e:
        print(e)

if __name__ == '__main__':
    prompt_user()
