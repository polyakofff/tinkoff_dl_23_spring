import argparse
import pickle

import numpy as np

from model import Model
from normalize_code import normalize_code
from get_features import get_features

parser = argparse.ArgumentParser()
parser.add_argument('input_file', type=str)
parser.add_argument('output_file', type=str)
parser.add_argument('--model', type=str)

args = parser.parse_args()

model = pickle.load(open(args.model, 'rb'))

with open(args.input_file, 'r', encoding='utf-8') as input:
    results = []

    for line in input.readlines():
        print(line)
        files = line.split(' ')

        with open(files[0], encoding='utf-8') as file0:
            code_a = file0.read()

        with open(files[1], encoding='utf-8') as file1:
            code_b = file1.read()
        
        try:
            code_a = normalize_code(code_a)
        except SyntaxError:
            print(f'syntax error while parsing {files[0]}')
            
        try:
            code_b = normalize_code(code_b)
        except SyntaxError:
            print(f'syntax error while parsing {files[1]}')

        # print(code_a)
        # print('-------------------------------------')
        # print(code_b)

        x = np.array([get_features(code_a, code_b)])
        # print(x)
        proba = model.predict_proba(x)[0][1]
        print(f'proba={proba}')
        results.append(proba)

        
with open(args.output_file, 'w') as output:
    for result in results:
        output.write(f'{result}\n')
