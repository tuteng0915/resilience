from re import I
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

#def main():

#Importing dataset
regx = pd.read_csv('regx.csv')
resilience = pd.read_csv('Cohens_d.csv')

for i in range(2,6,1):
    regx['MM_'+'i'] = regx['SMM']**i

print(regx)
#Feature and target matrices
X = regx[2:]
y = resilience[['RI_RT']]
X = X.to_numpy()


'''
    #Training and testing split, with 25% of the data reserved as the test set
    
    [X_train, X_test, y_train, y_test] = train_test_split(X, y, test_size=0.25, random_state=101)
    #Normalizing training and testing data
    [X_train, trn_mean, trn_std] = normalize_train(X_train)
    X_test = normalize_test(X_test, trn_mean, trn_std)
    #Define the range of lambda to test
    lmbda = np.logspace(-1.00,2.00,num=101,base=10.0)#fill in

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
    plt.show()

    #Find best value of lmbda in terms of MSE
    
    ind = MSE.index(min(MSE))#fill in

    [lmda_best,MSE_best,model_best] = [lmbda[ind],MSE[ind],MODEL[ind]]

    print('Best lambda tested is ' + str(lmda_best) + ', which yields an MSE of ' + str(MSE_best))

    return model_best


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
if __name__ == '__main__':
    best_model = main()
   
    print(f"Properties of best model: {best_model.get_params()}")
    print(f"Coefficients of best model: {best_model.coef_.tolist()}")
    print(f"b of best model: {best_model.intercept_}")
    print(f"Prediction for the diamond in Question 7: {best_model.predict(np.array([-1.15372087,-1.22213684,-1.1017549,-1.54042767,-2.43581425,-2.21169544,0.67493254 ,0.43644429,0.23566017]).reshape(1, -1))}")
'''