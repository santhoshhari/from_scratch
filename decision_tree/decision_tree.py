import pandas as pd
import numpy as np


def compute_mse(y):
    """
    Function to compute MSE given a response
    Prediction is assumed as mean of response
    """
    return np.mean(np.square(y-np.mean(y)))


class DecisionTreeRegressor():
    def __init__(self, x, y, idxs):
        """
        x - DataFrame with featuers
        y - Series with response
        idxs - Index of x to be considered for building decision tree
        """
        self.x = x
        self.y = y
        self.idxs = idxs
        self.n_rows = len(idxs)
        self.n_cols = x.shape[1]
        self.predicted_value = np.mean(y[idxs])
        self.score = np.Inf
        self.find_best_col()
        self.is_leaf = True if self.score == np.Inf else False

    def find_col_split(self, col_num):
        """
        Function to find best value to split a column
        Minimizes MSE (score)
        """
        y_vals = self.y.values[self.idxs]
        if compute_mse(y_vals) == 0:
            return
        col_vals = self.x.values[self.idxs, col_num]
        sorted_idxs = np.argsort(col_vals)
        sorted_x = col_vals[sorted_idxs]
        sorted_y = y_vals[sorted_idxs]
        for i in range(1, self.n_rows-1):
            if sorted_x[i] == sorted_x[i+1]:
                continue
            lhs_mse = compute_mse(sorted_y[:i])
            rhs_mse = compute_mse(sorted_y[i:])
            curr_score = lhs_mse + rhs_mse
            if curr_score < self.score:
                self.score = curr_score
                self.col_num = col_num
                self.split = sorted_x[i]
                self.split_name = self.x.columns[self.col_num]

    def find_best_col(self):
        """
        Function to find best column to split on
        """
        for i in range(self.n_cols):
            self.find_col_split(i)
        if self.score == np.Inf:
            return
        lhs_flag = self.x.values[self.idxs, self.col_num] < self.split
        rhs_flag = self.x.values[self.idxs, self.col_num] >= self.split
        self.lhs = DecisionTreeRegressor(self.x, self.y, self.idxs[lhs_flag])
        self.rhs = DecisionTreeRegressor(self.x, self.y, self.idxs[rhs_flag])

    def __repr__(self):
        s = f'n: {self.n_rows}; predicted_value:{self.predicted_value}'
        if not self.is_leaf:
            s += f'; score:{self.score}; split:{self.split};' +
            f' var:{self.split_name}'
        return s

    def predict_obs(self, xi):
        if self.is_leaf:
            return self.predicted_value
        t = self.lhs if xi[self.col_num] < self.split else self.rhs
        return t.predict_obs(xi)

    def predict(self, x):
        return np.array([self.predict_obs(xi) for _, xi in x.iterrows()])


if __name__ == "__main__":
    main()
