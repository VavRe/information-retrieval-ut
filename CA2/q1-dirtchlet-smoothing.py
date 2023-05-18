import os
import subprocess
import io
import pandas as pd
import json

csv_final = pd.DataFrame([], columns=['Algorithm','mu', 'MAP','P@20'])
scorer = "dirichlet"
min_range_mu = 0
max_range_mu = 500
split_rate_mu = 50
mu_array = [min_range_mu + x * (max_range_mu - min_range_mu) / split_rate_mu for x in range (split_rate_mu+1)]
print(mu_array)
# k_array = [0.7, 0.8, 0.9, 1.1, 1.2, 1.3]
homework_num = 2
home_directory=f"/home/vavre/information-retrieval/information-retrieval-ut/HW{homework_num}"
galago_path='/home/vavre/information-retrieval/galago-3.16/core/target/appassembler/bin/galago'
index_path="./myindex"
queries_path= "./inputData/q3.json"
f = open (queries_path, "r")
queries = json.loads(f.read())

for i in mu_array:
    with io.open('mu-command.json', 'w') as f:
            f.write('{\n')
            # f.write(' \"casefold\" : true,\n')
            f.write(' \"requested\" : 100,\n')
            f.write(f' \"index\" : \"{index_path}\",\n')
            f.write(' \"trec\" : true,\n')
            f.write(f' \"scorer\" : "{scorer}" ,\n')
            f.write(f' \"mu\" : {i} ,\n')
            next_line = ' \"queries\" : ' + json.dumps(queries['queries'])
            f.write(next_line)
            f.write('}')
    print('mu: ' + str(i) + " start", end="\r")
    command = [galago_path, 'batch-search', f'{home_directory}/mu-command.json']
    result = subprocess.check_output(command)
    splitiiit = str(result)[2:-1].split(sep='\\n')
    print('mu: ' + str(i) + " start --> Cmd ran", end="\r")
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
    print("mu" + str(i) + " start --> Cmd ran --> eval done", end="\r")

    
    map = float(splitiiit[0].split(sep=' ')[-1])
    p20 = float(splitiiit[1].split(sep=' ')[-1])

    data = [[scorer ,i, map,  p20]]
    df = pd.DataFrame(data, columns=csv_final.columns)
    csv_final = csv_final.append(df)
    print('i: '+ str(i) + " start --> Cmd ran --> eval done --> added to csv")

csv_final.reset_index(drop=True).to_csv(f'{scorer}-{min_range_mu}-{max_range_mu}-{split_rate_mu}',sep=',')