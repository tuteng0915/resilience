import numpy as np
import matplotlib.pyplot as plt
#Return fitted model parameters to the dataset at datapath for each choice in degrees.
#Input: datapath as a string specifying a .txt file, degrees as a list of positive integers.
#Output: paramFits, a list with the same length as degrees, where paramFits[i] is the list of
#coefficients when fitting a polynomial of d = degrees[i].
def main(datapath, degrees):
    paramFits = []

    #fill in
    #read the input file, assuming it has two columns, where each row is of the form [x y] as
    f_1 = open(r'regx.csv','r')
    f_2 = open(r'Cohens_d.csv','r')
    x = []
    y = []
    for lines in f_1.readlines():
        line = lines.split()
        x.append(float(line[1,2]))
    for lines in f_2.readlines():
        y.append(float(line[1:]))
    f_1.close()
    f_2.close()

    #iterate through each n in degrees, calling the feature_matrix and least_squares functions to solve
    #for the model parameters in each case. Append the result to paramFits each time.
    for n in degrees:
        X=feature_matrix(x,n)
        B = least_squares(X,y)
        paramFits.append(B)
    return paramFits


#Return the feature matrix for fitting a polynomial of degree d based on the explanatory variable
#samples in x.
#Input: x as a list of the independent variable samples, and d as an integer.
#Output: X, a list of features for each sample, where X[i][j] corresponds to the jth coefficient
#for the ith sample. Viewed as a matrix, X should have dimension #samples by d+1.
def feature_matrix(x, d):
    #fill in
    #There are several ways to write this function. The most efficient would be a nested list comprehension
    #which for each sample in x calculates x^d, x^(d-1), ..., x^0.
    X = [[x[i]**j for j in range(d,-1,-1)] for i in range(len(x))] 
    return X


#Return the least squares solution based on the feature matrix X and corresponding target variable samples in y.
#Input: X as a list of features for each sample, and y as a list of target variable samples.
#Output: B, a list of the fitted model parameters based on the least squares solution.
def least_squares(X, y):
    X = np.array(X)
    y = np.array(y)
    #fill in
    #Use the matrix algebra functions in numpy to solve the least squares equations. This can be done in just one line.
    B = np.linalg.inv(X.T @ X)@X.T@y

    return B.tolist()

def plotting():
    datapath = 'poly.txt'
    f = open(datapath,'r')
    x = []
    y = []
    for lines in f.readlines():
        line = lines.split()
        x.append(float(line[0]))
        y.append(float(line[1]))
    degrees = [1,2,3,4,5]
    plt.figure(figsize=(20,10))
    plt.scatter(x,y,label='points')
    for n in degrees:
        X=feature_matrix(x,n)
        B = least_squares(X,y)
        Y = (np.array(X) @ np.array(B)).tolist()
        #print value when x=2
        #print("when d = %d:"%n,end='')
        #print(float(np.dot(np.array(feature_matrix([2],n)),np.array(B))))
        # order points in ascending x order
        points =[]
        temp_x = x[:]
        # couple each x and y point
        for i in range(len(x)):
            points.append((temp_x[i],Y[i]))
        points = sorted(points)
        x_x =[]
        y_y =[]
        # decouple (x,y) to new list
        for i in range(len(points)):
            x_x.append(points[i][0])
            y_y.append(points[i][1])
        # get label
        l = 'y'+str(n)
        plt.plot(x_x,y_y,label=l)
    plt.legend()
    return



if __name__ == '__main__':
    datapath = 'poly.txt'
    degrees = [1,2,3,4,5]
    paramFits = main(datapath, degrees)
    plotting()
    print(paramFits)
