#-------------------------------------------------------------------------------
# Importations
import numpy as np
from .validation import log_colors

#-------------------------------------------------------------------------------
# Class logistic_regression

class LogisticRegression:


    def __init__(self, alpha: float = 1e-8, num_iters:int = 700):
        self.alpha = alpha
        self.num_iters = num_iters
        self.theta = None

    def gradientDescent(self, X, y, theta) -> tuple:
        '''
        Input:
            x: matrix of features which is (m,n+1)
            y: corresponding labels of the input matrix x, dimensions (m,1)
            theta: weight vector of dimension (n+1,1)
            alpha: learning rate
            num_iters: number of iterations you want to train your model for
        Output:
            J: the final cost
            theta: your final weight vector
        '''

        
        for _ in range(self.num_iters):
            
            # get z, the dot product of x and theta
            z = np.dot(X, theta)
            
            # get the sigmoid of z
            h = self.sigmoid(z)
            
            # calculate the cost function
            J = -(np.dot(np.transpose(y),np.log(h)) + np.dot(np.transpose(1 - y),np.log(1 - h)))/self.length

            # update the weights theta
            theta = theta -self.alpha*(np.dot(np.transpose(X),(h-y)))/self.length
            
        ### END CODE HERE ###
        J = float(J)
        return J, theta

    def train(self, X : np.array, y : np.array):
        
        self.n_feactures = X.shape[1]
        self.theta = np.zeros(self.n_feactures)
        self.length = X.shape[0]
        
        _, self.theta = self.gradientDescent(X, y, self.theta)



    
    def sigmoid(self, x):
        return 1/(1 + np.exp(-1*x))


    def predict(self, X: np.array):

        if self.theta == None:
            raise Exception(log_colors.FAIL + "Use the method"+ log_colors.BOLD + 
                            " train" + log_colors.FAIL + 
                            " first, after use this method to predict.")
        else:
            y_pred = self.sigmoid(np.dot(X, self.theta))

        return y_pred