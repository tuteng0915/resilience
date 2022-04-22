from cv2 import convertFp16
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def read_X(datapath):
    f = open(datapath,'r')
    x1 = []
    x2 = []
    f.readline()
    for lines in f.readlines():
        line = lines.rstrip().split(",")
        x1.append(float(line[1]))
        x2.append(float(line[2]))
    f.close() 
    return x1,x2

def read_Y(datapath):
    f = open(datapath,'r')
    y = [[]for i in range(26)]
    f.readline()
    for lines in f.readlines():
        line = lines.rstrip().split(",")
        #print(len(line))
        for i in range(1,27):
            if line[i] =="":
                y[i-1].append(0)
            else:
                y[i-1].append(float(line[i]))
    f.close() 
    return y
def feature_matrix(x1,x2, d):
    #fill in
    #There are several ways to write this function. The most efficient would be a nested list comprehension
    #which for each sample in x calculates x^d, x^(d-1), ..., x^0.
   
    X1 = [[x1[i]**j for j in range(d,0,-1)] for i in range(len(x1))] 
    X2 = [[x2[i]**j for j in range(d,0,-1)] for i in range(len(x2))]
    X_C = [[(x1[i]**j)*(x2[i]**(d-j)) for j in range(d-1,0,-1)] for i in range(len(x1))] 
    X = []
    for i in range(len(X1)):
        X.append(X1[i]+X2[i]+X_C[i])
    return X

def regularization(X_t,y):
    ###########################################################################
    Test_reserved = 0.25
    #Define the range of lambda to test
    lmbda = np.logspace(-1.00,2.00,num=101,base=10.0)
    ###########################################################################
    #Training and testing split, with 25% of the data reserved as the test set
    X = [np.array(X_t[i]) for i in range(len(X_t))]

    [X_train, X_test, y_train, y_test] = train_test_split(X, y, test_size=Test_reserved, random_state=101)
    #Normalizing training and testing data
    [X_train, trn_mean, trn_std] = normalize_train(X_train)
    X_test = normalize_test(X_test, trn_mean, trn_std)
    
    MODEL = []
    MSE = []
    for l in lmbda:
        #Train the regression model using a regularization parameter of l
        model = train_model(X_train,y_train,l)

        #Evaluate the MSE on the test set
        mse = error(X_test,y_test,model)

        #Store the model and mse in lists for further processing
        MODEL.append(model)
        MSE.append(mse)

    #Plot the MSE as a function of lmbda
    plt.plot(lmbda,MSE) #fill in
    plt.xlabel("value of lambda")
    plt.ylabel("MSE")
    plt.title("MSE VS lambda")
    #plt.show()

    #Find best value of lmbda in terms of MSE
    
    ind = MSE.index(min(MSE))#fill in

    [lmda_best,MSE_best,model_best] = [lmbda[ind],MSE[ind],MODEL[ind]]

    print('Best lambda tested is ' + str(lmda_best) + ', which yields an MSE of ' + str(MSE_best))
    f = model_best.fit(X,y)
    R2 = model_best.score(X,y)
    coef = model_best.coef_
    return lmda_best,R2


#Function that normalizes features in training set to zero mean and unit variance.
#Input: training data X_train
#Output: the normalized version of the feature matrix: X, the mean of each column in
#training set: trn_mean, the std dev of each column in training set: trn_std.
def normalize_train(X_train):
    #fill in
    mean = np.mean(X_train,axis=0)
    std = np.std(X_train,axis=0)
    X = (X_train - mean)/std
    return X, mean, std


#Function that normalizes testing set according to mean and std of training set
#Input: testing data: X_test, mean of each column in training set: trn_mean, standard deviation of each
#column in training set: trn_std
#Output: X, the normalized version of the feature matrix, X_test.
def normalize_test(X_test, trn_mean, trn_std):
    #fill in
    X = (X_test - trn_mean) / trn_std
    return X



#Function that trains a ridge regression model on the input dataset with lambda=l.
#Input: Feature matrix X, target variable vector y, regularization parameter l.
#Output: model, a numpy object containing the trained model.
def train_model(X,y,l):

    #fill in
    model_ridge = linear_model.Ridge(alpha=l,fit_intercept=True)
    model = model_ridge.fit(X,y)
    
    return model


#Function that calculates the mean squared error of the model on the input dataset.
#Input: Feature matrix X, target variable vector y, numpy model object
#Output: mse, the mean squared error
def error(X,y,model):

    #Fill in
    y_p = model.predict(X)
    mse = mean_squared_error(y,y_p)
 
    return mse
def main():
    #################################
    X_file_path = "regx.csv"
    Y_file_path = "Cohens_d.csv"
    d = 5
    #################################
    x1,x2=read_X(X_file_path)
    X = feature_matrix(x1,x2,d)
    y = read_Y(Y_file_path)
    La = []
    R2list = []
    cohens = pd.read_csv('Cohens_d.csv')

    for i in range(26):
        LAMBDA, R2 = regularization(X,y[i])
        La.append(LAMBDA)
        R2list.append(R2)
        
    RIGDE = pd.DataFrame(columns=['performance','LA','R_2'])
    RIGDE['performance'] = cohens.iloc[0,1:]
    RIGDE['LA'] = La
    RIGDE['R_2'] =R2list
    print(RIGDE)


if __name__ == '__main__':
    main()
