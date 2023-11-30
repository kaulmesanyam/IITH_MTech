
# =============================================================================
# Sanyam Kaul: CS23MTECH14011
# Mayuresh Rajesh Dindorkar: CS23MTECH14007
# Shrenik Ganguli: CS23MTECH14014
# Sreyash Mohanty: CS23MTECH14015
# 
# 
# 
# Assumption
# 1. Polytope is non-degenerate.
# 2. Rank of A is n 
# =============================================================================


import csv
import numpy as np
from numpy import linalg as la

class LO_Assignment_3():

    def __init__(self, A, B, C, z, m, n ):
        self.m = m
        self.n = n
        self.A = A
        self.B = B
        self.C = C
        self.eps = 1e-8
        self.X = z.reshape((n,1))
        
        self.check_dimensions(self.A, self.B, self.C, self.X, self.n, self.m)
    
    def check_dimensions(self, A, B, C, X, n, m):
        try:
            assert(A.shape == (m, n))
            assert(B.shape == (m, 1))
            assert(C.shape == (n, 1))
            assert(X.shape == (n, 1))
        except AssertionError:
            self._return_error()
            return
        
        self.B = self.get_non_degenerate()  # Making LP non degenerate
        print(self.B)
        if self.B is not None:
            print("Non-feasible problem") if self.n != np.linalg.matrix_rank(self.A) else self.execute_simplex_algo()

    def get_non_degenerate(self) -> np.ndarray:
        """ Converts polytope to non degenerate

        :return: Modified version of B
        """
        itr = 0
        while True:
            i = self.m - self.n
            B_ = self.B
            if (itr < 1000):
                # Perturbing B by adding noise
                
                B_[:i] = self.B[:i] + np.random.uniform(1e-6, 1e-5, size=(i,1))
                itr += 1

            else:
                # Checking for a larger range
                B_[:i] = self.B[:i] + np.random.uniform(0.1, 10, size=(i,1))

            Z = np.dot(self.A, self.X) - B_
            inds = np.where(np.abs(Z) < self.eps)[0]
            if len(inds) == self.n:  # Converted to non degenerate
                break
            print(itr)
        return B_

    def check_point_feasibility(self, A, X, B):
        return np.all(np.dot(A, X) <= B)

    def check_any_constraint_tight(self, A, X, B):
        return True if np.any(B - np.dot(A, X) < pow(10, -4)) else False

    def approach_polytope_boundary(self, A, X, B, C):
        print('Approaching boundry: -')
        dir_vec = C
        alpha = 0.01
        while not self.check_any_constraint_tight(A, X, B):
                if not self.check_point_feasibility(A, (X + alpha * dir_vec), B):
                    alpha /= 10
                else:
                    cost = np.dot(X.T, C)
                    print('X: ', X.ravel(), ', Cost: ', cost.ravel())
                    X = X + alpha * dir_vec
        return X

    def obtain_initial_vertex(self, A, B):
        rank = la.matrix_rank(A)
        initial_vertex = np.dot(la.pinv(A[:rank]), B[:rank])
        return initial_vertex

    def calculate_alpha_value(self, A, X, B, C):
        get_independent_rows = lambda A, X, B: (B - np.dot(A, X) < self.eps).T[0]
        lin_ind = A[get_independent_rows(A, X, B)]
        alpha = np.dot(la.pinv(lin_ind.T), C)
        return alpha
    
    def calculate_beta(self, A, X, B, is_min_ratio_positive, min_ratio):
        beta = np.min(((B - np.dot(A, X)).T[0] / min_ratio + 1e-12)[is_min_ratio_positive])
        return beta
    
    def find_optimal_vertex(self, A, X, B, C):
        if np.all(self.calculate_alpha_value(A, X, B, C) >= 0):
            calculated_cost = np.dot(X.T, C).ravel()
            print(f'X: {X.ravel()}, cost: {calculated_cost}')
            return X
        get_independent_rows = lambda A, X, B: (B - np.dot(A, X) < pow(10, -4)).T[0]
        tight_rows_matrix = get_independent_rows(A, X, B)
        direction_matrix = -la.pinv(A[tight_rows_matrix])
        print('dm', direction_matrix.shape)
        cost_list = []
        for i in range(0, direction_matrix.shape[1], 1):
            direction_vector = direction_matrix[:, i].reshape(-1, 1)
            min_ratio = (np.dot(A, direction_vector)).T
            is_min_ratio_positive = min_ratio > 0
            if np.any(is_min_ratio_positive):
                beta = self.calculate_beta(A, X, B, is_min_ratio_positive, min_ratio)
                z_prime = X + direction_vector * beta
                calculated_cost = np.dot(z_prime.T, C)
                cost_list.append((calculated_cost, i, z_prime))
                print(f'z_prime: {z_prime}, cost: {calculated_cost}')
            else:
                print("this is unbounded case")
                return []
        
        _, index, z_prime = max(cost_list)
        return self.find_optimal_vertex(A, z_prime, B, C)

    def execute_simplex_algo(self):
        temp_A, temp_B, temp_C = self.A, self.B, self.C
        if self.X.shape != self.C.shape:
            temp_A = np.append(np.append(self.A, np.zeros((1, self.n)), axis = 0), np.ones((self.m + 1, 1)), axis = 1)
            temp_A[-1][-1] = -1
            temp_B = np.append(self.B, [abs(min(self.B))], axis = 0)
            temp_C = np.zeros((self.n +1, 1))
            temp_C[-1] = 1

        self.X = self.approach_polytope_boundary(temp_A, self.X, temp_B, temp_C)
        print('reached polytope boundary, now approaching vertex: -')
        self.X = self.obtain_initial_vertex(temp_A, temp_B)
        print('X', self.X)
        opt_vertex = self.find_optimal_vertex(temp_A, self.X, temp_B, temp_C)
        if len(opt_vertex) == 0:
            print('Polytope is unbounded- optimal value does not exit')
        else:
            print(f'Optimal vertex: {self.X.T[0]}')
            
def read_linear_programming_input(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    
    # Extracting data
    z = np.array([float(x) for x in data[0][:-1]])
    c = np.array([float(x) for x in data[1][:-1]])
    b = np.array([float(x) for x in [row[-1] for row in data[2:]]])
    A = np.array([[float(x) for x in row[:-1]] for row in data[2:]])
    return z, c, b, A
 
    
def main():
    file_path = 'Assignment3.csv'
    z, C, B, A = read_linear_programming_input(file_path)
    
    print(f'Initial feasible point z: {z}')
    print(f'Cost Vector C: {C}')
    print(f'Constraint Vector B: {B}')
    print(f'Co-efficient Matrix A:\n {A}')
    
    m = A.shape[0]
    n = A.shape[1]
    
    print('m:', m)
    print('n:',n)
    B = B.reshape((m,1))
    C = C.reshape((n,1))
    
    LO_Assignment_3(A, B, C, z, m, n)

if __name__=="__main__": 
    main()
