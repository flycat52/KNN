# COMP307 - Assignment1 - part1
# 300434790 - Yalian

import math
import os
import os.path
import argparse

def prepare_dataset(trainingfile, testfile):
    training_o = get_file_array(trainingfile)   # original training set
    test_o = get_file_array(testfile)           # original test set

    training = get_dataset(training_o)
    test = get_dataset(test_o)
    
    return training, test


def KNN(training, test, output_file, k):
    (R0, R1, R2, R3) = get_training_range(training)

    CLASS_SETOSA = 'Iris-setosa'
    CLASS_VERSICOLOR = 'Iris-versicolor'
    CLASS_VIRGINICA = 'Iris-virginica'
    num_accurate = 0

    for p in range(len(test)):
        d = []
        t = test[p][0] #test features
        test_class = test[p][1] #test class of one instance
        for i in range(len(training)):
            tr = training[i][0]
            tr_class = training[i][1]
            dv = math.sqrt( (t[0]- tr[0])**2/(R0**2) + (t[1] - tr[1])**2 / (R1**2) + (t[2]- tr[2])**2/(R2**2) + (t[3] - tr[3])**2 / (R3**2))
            d.append((dv, tr, tr_class))
    
        sorted_d = sorted(d, key=lambda x: float(x[0]), reverse=False)
    
        nearest_neighbour = []
        for kk in range(k): 
            nearest_neighbour.append(sorted_d.pop(kk)[2])
        num_setosa = nearest_neighbour.count(CLASS_SETOSA)
        num_versicolor = nearest_neighbour.count(CLASS_VERSICOLOR)
        num_virginica = nearest_neighbour.count(CLASS_VIRGINICA)
        
        maxclass = max(num_setosa, num_versicolor, num_virginica)
        
        if maxclass == num_setosa:
            predict_class = CLASS_SETOSA
        elif maxclass == num_versicolor:
            predict_class = CLASS_VERSICOLOR    
        elif maxclass == num_virginica:
            predict_class = CLASS_VIRGINICA

        
        if test_class == predict_class:
            result = 'Correct'
            num_accurate += 1
        else: result = 'Incorrect'

        with open(output_file,"a") as f:
            f.write('Test instance: ' + str(t) + ' predicted class is: ' + predict_class +'. Result: ' + result + "\n")
            print('Test instance: ' + str(t) + ' predicted class is: ' + predict_class +'. Result: ' + result + "\n")
    accuracy = round(float(num_accurate) / len(test) * 100, 2)

    f = open(output_file, "a")
    f.write('k = ' + str(k) + '\n')  
    f.write('Accuracy = ' + str(accuracy) + '% \n\n\n')
    print('k = ' + str(k) )  
    print('Accuracy = ' + str(accuracy) + '%')    

    
        
def get_dataset(dataset):
    data = []
    for line in dataset:
        line = line.split()
        data.append(([float(line[0]), float(line[1]), float(line[2]), float(line[3])], str(line[4])))
    return data 


def get_training_range(training):    
    sl, sw, pl, pw = ([] for i in range(4))
    for line in training:
        sl.append(float(line[0][0]))
        sw.append(float(line[0][1]))
        pl.append(float(line[0][2]))
        pw.append(float(line[0][3]))

    R0 = max(tuple(sl)) - min(tuple(sl))
    R1 = max(tuple(sw)) - min(tuple(sw))
    R2 = max(tuple(pl)) - min(tuple(pl))
    R3 = max(tuple(pw)) - min(tuple(pw))

    return (R0, R1, R2, R3)


def get_file_array(file):
    with open(file, 'r') as ftr:
        array = []
        for line in ftr:
            if line != '\n' and line != '\r':
                array.append(line)
    return array


def Main():
    output_file = 'sampleoutput.txt'
    if os.path.exists(output_file):
        os.remove(output_file)

    parser = argparse.ArgumentParser()
    parser.add_argument('trainingset', help='Choose a training data set')
    parser.add_argument('testset', help='Choose a test data set')
    args = parser.parse_args()

    (training, test) = prepare_dataset(args.trainingset, args.testset)
    #(training, test) = prepare_dataset('iris-training.txt', 'iris-test.txt')
    # k = 1
    KNN(training, test, output_file, 1)
    # k = 3
    KNN(training, test, output_file, 3)

Main()
