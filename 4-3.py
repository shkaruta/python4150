## Задание 3
'''
При помощи numpy
* Сгенерируйте случайную квадратную матрицу размером 10 на 10
* Найдите ее определитель (не забудьте обработать вариант с вырожденной матрицей)
* транспонируйте матрицу
* Найдите ранг матрицы
* Найдите собственные значения и собственные вектора матрицы
* сгенерируйте вторую матрицу размером 10 на 10 и выполните сложение и умножение двух матриц
'''

import numpy as np

# генерация матрицы mat1 размером 10 * 10 из целых
mat1 = np.random.randint(low=-100, high=100, size=(10, 10))
print(f"Matrix mat1:\n{mat1}")

# определитель mat1
det_mat1 = np.linalg.det(mat1)
if np.isclose(det_mat1, 0):  
    print("Matrix is degenerate (determinant = 0)")
else:
    print(f"Determinant of mat1: {det_mat1}")

# транспонирование mat1
mat1_transposed = np.transpose(mat1)
print(f"Transposed mat1:\n{mat1_transposed}")

# ранг mat1
rank_mat1 = np.linalg.matrix_rank(mat1)
print(f"Rank of mat1: {rank_mat1}")

# собственные значения и собственные вектора mat1
eigenvalues_mat1, eigenvectors_mat1 = np.linalg.eig(mat1)
print(f"Eigenvalues of mat1:\n{eigenvalues_mat1}")
print(f"Eigenvectors of mat1:\n{eigenvectors_mat1}")

# генерация матрицы mat2 размером 10 * 10 из целых
mat2 = np.random.randint(low=-100, high=100, size=(10, 10))

# сложение mat1 + mat2
mat_sum = mat1 + mat2
print(f"Sum of mat1 and mat2:\n{mat_sum}")

# поэлементное умножение mat1 и mat2
mat_product = mat1 * mat2
print(f"Element-wise product of mat1 and mat2:\n{mat_product}")

# произведение матриц mat1 * mat2
mat_dot_product = np.dot(mat1, mat2)
print(f"Matrix multiplication (dot product) of mat1 and mat2:\n{mat_dot_product}")
