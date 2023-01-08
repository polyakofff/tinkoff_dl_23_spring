import argparse
import os
import random
import csv
import pickle

import numpy as np
from sklearn.metrics import accuracy_score

from model import Model
from normalize_code import normalize_code
from get_features import get_features

random.seed(42)

parser = argparse.ArgumentParser()
parser.add_argument('files', type=str)
parser.add_argument('plagiat1', type=str)
parser.add_argument('plagiat2', type=str)
parser.add_argument('--model', type=str)

args = parser.parse_args()

files = os.listdir(args.files)
plagiat1 = os.listdir(args.plagiat1)
plagiat2 = os.listdir(args.plagiat2)

codes = {}
for file in files:
    with open(args.files + '/' + file, 'r', encoding='utf-8') as input:
        codes[file.split('.')[0]] = input.read()

plags1 = {}
for file in plagiat1:
    with open(args.plagiat1 + '/' + file, 'r', encoding='utf-8') as input:
        plags1[file.split('.')[0]] = input.read()

plags2 = {}
for file in plagiat2:
    with open(args.plagiat2 + '/' + file, 'r', encoding='utf-8') as input:
        plags2[file.split('.')[0]] = input.read()

train_data_1 = []
for file, code in codes.items():
    plag = plags1.get(file)
    if plag is not None:
        train_data_1.append((file, code, file, plag, 1))
    plag = plags2.get(file)
    if plag is not None:
        train_data_1.append((file, code, file, plag, 1))

n_1 = len(train_data_1)
n_0 = n_1 * 2
train_data_0 = []

while len(train_data_0) < n_0:
    file, code = random.choice(list(codes.items()))
    plag_file, plag = random.choice(list(plags1.items())) if random.getrandbits(1) else random.choice(list(plags2.items()))
    if file != plag_file:
        train_data_0.append((file, code, plag_file, plag, 0))

train_data = train_data_1 + train_data_0
random.shuffle(train_data)

print(f'number of label 1: {n_1}, number of label 0: {n_0}')


xs = []
ys = []
n_bad_codes = 0
for i, (file, code, plag_file, plag, label) in enumerate(train_data):
    # print(f'line {i}: {file}.py {plag_file}.py')
    # нормализация повышает точность с 87% до 97%! (на тренировочных данных)
    code = normalize_code(code)
    try:
        plag = normalize_code(plag)
    except SyntaxError:
        n_bad_codes += 1
        print(f'syntax error while parsing plagiat/{plag_file}.py')
    x = get_features(code, plag)
    xs.append(x)
    ys.append(label)

print(f'number of bad (non-compiled) codes: {n_bad_codes}')

with open('train_data.csv', 'w', newline='') as output:
    writer = csv.writer(output, delimiter=',')
    for x, y in zip(xs, ys):
        writer.writerow((*x, y))
        

X_train = np.array(xs)
y_train = np.array(ys)

model = Model()
model.fit(X_train, y_train)

pred = model.predict(X_train)
print(f'train accuracy={accuracy_score(y_train, pred)}')

pickle.dump(model, open(args.model, 'wb'), pickle.HIGHEST_PROTOCOL)
print('model saved')
