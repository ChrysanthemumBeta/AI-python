import numpy as np
import json, random, time, os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.layers import Activation, Dense, LSTM

def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    Temp = []
    for pred in preds:
        Temp.append(abs(pred))
    preds = Temp
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)




BlockData = {
    "Stone" : 0,
    "Cloud" : 1,
    "Note Block" : 2,
    "? Block" : 3,
    "Coin" : 4,
    "Red Coin" : 5,
    "Block" : 6,
    "Ground" : 7,
    "Koopa" : 8,
    "Goomba" : 9,
    "Lakitu" : 10,
    "Hidden Block" : 11,
    "Muncher" : 12,
    "Piranha Flower" : 13,
    "Spiny" : 14,
    "Air" : 15
    }


SEQ_LENGTH = 10
STEP_SIZE = 3
POSSIBLE = len(BlockData.keys())
TrainingData = []

def Save_Level(blocks):
    LevelData = {
        "name" : "AI Generated Level",
        "data" : []
        }
    for i, block in enumerate(blocks):
        LevelData["data"].append({
            "name" : block,
            "x" : i * 16,
            "y" : 24,
            "flag": ""
            })
    with open("AI Generated\\" + LevelData["name"] + ".json", "w") as file:
        file.write(json.dumps(LevelData))
        

def generate_level(length, temperature):
    #start_index = random.randint(0, len(level) - SEQ_LENGTH - 1)
    generated = []
    block = ["Ground"] * SEQ_LENGTH#level[start_index: start_index + SEQ_LENGTH]
    generated.append(block)
    for i in range(length):
        x_predictions = np.zeros((1, len(block), POSSIBLE))
        for t, Id in enumerate(block):
            x_predictions[0, t, BlockData[Id]] = 1
        predictions = model.predict(x_predictions, verbose=0)[0]
        next_index = sample(predictions,
                                 temperature)
        next_block = list(BlockData.keys())[next_index]

        generated.append(next_block)
        block.append(next_block)
    return generated




def GetTrainingData(FileName):
    blocks = [] 
    next_block = []
    level = []
    with open("SimplifiedData\\" + FileName) as file:
        file = json.load(file)
        for x in range(0, 1600, 16):
            for block in file["data"]:
                if block["x"] == x and block["y"] == 24:
                    if block["name"] != "Muncher":
                        level.append(block["name"])
                else:
                    level.append("Air")


    for i in range(0, len(level) - SEQ_LENGTH, STEP_SIZE):
        blocks.append(level[i: i + SEQ_LENGTH])
        next_block.append(level[i + SEQ_LENGTH])


    x = np.zeros((len(blocks), SEQ_LENGTH,
              POSSIBLE), dtype=np.bool)
    y = np.zeros((len(blocks),
              POSSIBLE), dtype=np.bool)

    for i, block in enumerate(blocks):
        for t, Id in enumerate(block):
            x[i, t, BlockData[Id]] = 1
        y[i, BlockData[next_block[i]]] = 1
    return [x, y]

Levels = os.listdir("Training")

for file in Levels:
    TrainingData.append(GetTrainingData(file))



model = Sequential()
model.add(LSTM(128, input_shape=(SEQ_LENGTH, POSSIBLE)))

model.add(Dense(POSSIBLE))

model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))

model.load_weights("model4.h5")

for Data in TrainingData:
    model.fit(Data[0], Data[1], batch_size=256, epochs=4)


model.save_weights("model4.h5")
Save_Level(generate_level(100, 0.1))


