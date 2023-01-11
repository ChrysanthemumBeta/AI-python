import json, random, numpy
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.layers import Activation, Dense, LSTM


PATH = "SimplifiedData\SMB1 1-1 Remake.json"
#Width of surrounding block check
'''e.g
000
0/0  / = tile selected 
000
'''
COMPLEXITY = 3

#Creates a 2D list of size size
#size should be supplied as either a tuple or list with 2 int values
#e.g [2, 2]
def Create_list(size):
    list2D = []
    for x in range(size[0]):
        row = []
        for y in range(size[1]):
            row.append(0)
        list2D.append(row)
    return list2D

#Loads a level
def load_level(path):
    with open(path, "r") as file:
        file = json.load(file)
        Max = [0, 0]
        #Finds the max
        #Divides by 16 to get grid coords from screen coords
        for block in file["data"]:
            if block["x"] / 16 > Max[0]:
                Max[0] = int(block["x"] / 16)
            if block["y"] / 16 > Max[1]:
                Max[1] = int(block["y"] / 16)
        level = Create_list(Max)
        #For every block that exists, set it to 1 in the 2D list
        for block in file["data"]:
            level[int(block["x"]/16)-1][int(block["y"]/16)-1] = 1
        return level

#works for 3, bad var names
def Get_surround(coord, level):    
    X_train = Create_list([COMPLEXITY, COMPLEXITY])
    mid = [int(((COMPLEXITY+1)/2)-1), int(((COMPLEXITY+1)/2)-1)]
    for x in range(int((COMPLEXITY+1)/2)):
        for y in range(int((COMPLEXITY+1)/2)):
            if (coord[0] + x > len(level) or coord[0] - x < 0) or (coord[0] + y > len(level) or coord[1] - y < 0):
                #out of bounds on x
                X_train[mid[0] + x][mid[1] + y] = 0
            else:
                #positive
                X_train[mid[0] + x][mid[1] + y] = level[coord[0] + x - 1][coord[1] + y - 1]
                #negative
                X_train[mid[0] - x][mid[1] - y] = level[coord[0] - x - 1][coord[1] - y - 1]
    X_train[mid[0]][mid[1]] = -1
    Y_train = level[coord[0]][coord[1]]
    #X_train is surrounding
    #Y_train is the middle
    return X_train, Y_train

#Gets a list of training data to use 
def Get_training(level):
    X = []
    Y = []
    for x in range(len(level)):
        for y in range(len(level[0])):
            #get surrounding
            X_train, Y_train = Get_surround([x, y], level)
            X.append(X_train)
            Y.append(Y_train)
    return X, Y

TrainingData = Get_training(load_level(PATH))
#tensorflow stuff
model = Sequential()
model.add(LSTM(128, input_shape=(COMPLEXITY, COMPLEXITY)))
model.add(Dense(units=64, activation='relu'))
#output
model.add(Dense(units=1, activation='sigmoid'))

model.compile(loss="binary_crossentropy", optimizer="sgd", metrics="accuracy")
#Creates error
x_predictions = Get_surround([1,1], load_level(PATH))
X = numpy.asarray(x_predictions).astype(numpy.float32)

model = load_model("Model-1")
a = model.predict(X, verbose=0)[0]
print(a)
#model.fit(TrainingData[0], TrainingData[1], epochs=200, batch_size=32)
#model.save("Model-1")
