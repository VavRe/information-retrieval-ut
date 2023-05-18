import os
import subprocess
import io
import pandas as pd
import json

scorer = "two-steps-smoothing"
csvResult = pd.DataFrame([], columns=['Algorithm', 'lambda', 'miu','MAP','P@20'])
min_range_lambda = 0
max_range_lambda = 1
split_rate_lambda = 10
min_range_miu = 0.0
max_range_miu = 10
split_rate_miu = 10
lambda_array = [min_range_lambda + x * (max_range_lambda - min_range_lambda) / split_rate_lambda for x in range (split_rate_lambda+1)]
# lambda_array = [0.2, 0.25, 0.3, 0.35]
miu_array = [min_range_miu + x * (max_range_miu - min_range_miu) / split_rate_miu for x in range (split_rate_miu+1)]
print(lambda_array)
print(miu_array)
# miu_array = [0.7, 0.8, 0.9, 1.1, 1.2, 1.3]
homework_num = 2
home_directory=f"/home/vavre/information-retrieval/information-retrieval-ut/HW{homework_num}"
galago_path='/home/vavre/information-retrieval/galago-3.16/core/target/appassembler/bin/galago'
index_path="./myindex"
queries_path= "./inputData/q3.json"

f = open (queries_path, "r")
queries = json.loads(f.read())


for lambda_ in lambda_array:
    for miu in miu_array:
        with io.open('command2.json', 'w') as f:
            f.write('{\n')
            # f.write(' \"casefold\" : true,\n')
            f.write(' \"requested\" : 100,\n')
            f.write(f' \"index\" : \"{index_path}\",\n')
            f.write(' \"miu\" : '+ str(miu) + ',\n')
            f.write(' \"lambda\" : '+ str(lambda_) + ',\n')
            f.write(' \"trec\" : true,\n')
            f.write(f' \"scorer\" : \"{scorer}",\n')
            next_line = ' \"queries\" : ' + json.dumps(queries['queries'])
            f.write(next_line)
            f.write('}')



        print('lambda_: ' + str(lambda_) + 'miu: ' + str(miu) + " start", end="\r")
        command = [galago_path, 'batch-search', f'{home_directory}/command2.json']
        result = subprocess.check_output(command)
        splitiiit = str(result)[2:-1].split(sep='\\n')
        print('lambda_: ' + str(lambda_) + 'miu: ' + str(miu) + " start --> Cmd ran", end="\r")
        with io.open('baseline.txt', 'w') as f:
            for s in splitiiit[:-1]:
                f.write(s + '\n')
            f.write(splitiiit[-1])

        command = [galago_path,
        'eval',
        '--judgments=./inputData/relevance.txt',
        '--baseline=./baseline.txt',
        '--metrics+map',
        '--metrics+P20',
        ]

        result = subprocess.check_output(command)
        splitiiit = str(result)[2:-1].split(sep='\\n')
        sp = splitiiit[0].split(sep=' ')
        print('lambda_: ' + str(lambda_) + 'miu: ' + str(miu) + " start --> Cmd ran --> eval done", end="\r")

        
        map = float(splitiiit[0].split(sep=' ')[-1])
        p20 = float(splitiiit[1].split(sep=' ')[-1])

        data = [['two-steps-smoothing', lambda_, miu, map, p20]]
        df = pd.DataFrame(data, columns=csvResult.columns)
        csvResult = csvResult.append(df)
        print('lambda_: ' + str(lambda_) + 'miu: ' + str(miu) + " start --> Cmd ran --> eval done --> added to csv")



csvResult.reset_index(drop=True).to_csv('two-steps-smoothing',sep=',')
