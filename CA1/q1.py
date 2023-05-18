import os
import subprocess
import io
import pandas as pd
import json

csvResult = pd.DataFrame([], columns=['Algorithm', 'b', 'k', 'Recall', 'MAP', 'nDCG', 'P@5'])
min_range_b = 0
max_range_b = 1
split_rate_b = 10
min_range_k = 0.0
max_range_k = 3
split_rate_k = 15
b_array = [min_range_b + x * (max_range_b - min_range_b) / split_rate_b for x in range (split_rate_b+1)]
# b_array = [0.2, 0.25, 0.3, 0.35]
k_array = [min_range_k + x * (max_range_k - min_range_k) / split_rate_k for x in range (split_rate_k+1)]
min_range_k = 4
max_range_k = 7
split_rate_k = 6
k_array += [min_range_k + x * (max_range_k - min_range_k) / split_rate_k for x in range (split_rate_k + 1)]
print(k_array)
print(b_array)
# k_array = [0.7, 0.8, 0.9, 1.1, 1.2, 1.3]

home_directory="/home/vavre/information-retrieval/information-retrieval-ut/HW1"
galago_path='/home/vavre/information-retrieval/galago-3.16/core/target/appassembler/bin/galago'
index_path="./myindex"
f = open ('./inputData/queries.json', "r")
queries = json.loads(f.read())


i = 0
for b in b_array:
    for k in k_array:
        with io.open('command2.json', 'w') as f:
            f.write('{\n')
            # f.write(' \"casefold\" : true,\n')
            f.write(' \"requested\" : 10,\n')
            f.write(f' \"index\" : \"{index_path}\",\n')
            f.write(' \"k\" : '+ str(k) + ',\n')
            f.write(' \"b\" : '+ str(b) + ',\n')
            f.write(' \"trec\" : true,\n')
            f.write(' \"scorer\" : \"bm25",\n')
            next_line = ' \"queries\" : ' + json.dumps(queries['queries'])
            f.write(next_line)
            f.write('}')



        print('b: ' + str(b) + 'k: ' + str(k) + " start", end="\r")
        command = [galago_path, 'batch-search', f'{home_directory}/command2.json']
        result = subprocess.check_output(command)
        splitiiit = str(result)[2:-1].split(sep='\\n')
        print('b: ' + str(b) + 'k: ' + str(k) + " start --> Cmd ran", end="\r")
        with io.open('baseline.txt', 'w') as f:
            for s in splitiiit[:-1]:
                f.write(s + '\n')
            f.write(splitiiit[-1])

        command = [galago_path,
        'eval',
        '--judgments=./inputData/relevance.txt',
        '--baseline=./baseline.txt',
        '--metrics+num_rel_ret',
        '--metrics+num_rel',
        '--metrics+map',
        '--metrics+ndcg',
        '--metrics+P5',
        ]

        result = subprocess.check_output(command)
        splitiiit = str(result)[2:-1].split(sep='\\n')
        sp = splitiiit[0].split(sep=' ')
        print('b: ' + str(b) + 'k: ' + str(k) + " start --> Cmd ran --> eval done", end="\r")

        
        num_rel_ret = float(splitiiit[0].split(sep=' ')[-1])
        num_rel = float(splitiiit[1].split(sep=' ')[-1])
        recall = num_rel_ret / num_rel
        map = float(splitiiit[2].split(sep=' ')[-1])
        ndcg = float(splitiiit[3].split(sep=' ')[-1])
        p5 = float(splitiiit[4].split(sep=' ')[-1])

        data = [['bm25', b, k, recall, map, ndcg, p5]]
        df = pd.DataFrame(data, columns=csvResult.columns)
        csvResult = csvResult.append(df)
        print('b: ' + str(b) + 'k: ' + str(k) + " start --> Cmd ran --> eval done --> added to csv")


    i += 1

csvResult.reset_index(drop=True).to_csv('q1_bm25_res(k).csv',sep=',')
