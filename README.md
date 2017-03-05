# python-fastsort-benchmark
A simple benchmark demonstrating the speed-up from exploiting type-homogeneity in `list.sort()`. To build:
```
sh build.sh
```
To run the benchmark:
```
python-ref/python bench.py ref.pickle
python-dev/python bench.py dev.pickle
```
To process the pickles (here, we compute mean and standard deviation for each type):
```
import pickle
ref = pickle.load(open('ref.pickle','rb'))
dev = pickle.load(open('dev.pickle','rb'))

import numpy as np
for interpreter in [ref,dev]:
    for bench_set in interpreter:
        for key in bench_set.keys():
            bench_set[key] = np.array(bench_set[key])
            bench_set[key] = (np.mean(bench_set[key]),
                              np.std(bench_set[key]))

print('ref scalar:')
for key in ref[0].keys():
    print('{}:'.format(key),ref[0][key])
print()
print('ref tuple:')
for key in ref[1].keys():
    print('{}:'.format(key),ref[1][key])
print()
print('dev scalar:')
for key in dev[0].keys():
    print('{}:'.format(key),dev[0][key])
print()
print('dev tuple:')
for key in dev[1].keys():
    print('{}:'.format(key),dev[1][key])
print()
```
