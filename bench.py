#These functions construct the different types of lists we will benchmark
funcs = []

def float_list(n):
    random.seed(n)
    return [random.random() for _ in range(0,n)]
funcs.append(('float',float_list))

def small_int_list(n):
    random.seed(n)
    return [int(2**31*random.random() - 2**30) for _ in range(0,n)]
funcs.append(('small_int',small_int_list))

def int_list(n):
    random.seed(n)
    return small_int_list(n) + [2**64]
funcs.append(('int',int_list))

def latin_string_list(n):
    random.seed(n)
    return [str(random.random()) for _ in range(0,n)]
funcs.append(('latin_string',latin_string_list))

def string_list(n):
    random.seed(n)
    return latin_string_list(n) + ["\uffff"]
funcs.append(('string',string_list))

def heterogeneous_list(n):
    return float_list(n) + [0]
funcs.append(('heterogeneous',heterogeneous_list))

#This function allows us to benchmark the above types when they're in tuples
def tuplify(L):
    return [(x,) for x in L]

#This is the main benchmark loop

#stdout_redirector from:
#https://raw.githubusercontent.com/berkerpeksag/python-playground/master/stdout_redirector.py
from stdout_redirector import stdout_redirector
import io, random, re

def run_benchmark(iterations,start_size,step,end_size):
    scalar_times = {label:[]for (label,func) in funcs};
    tuple_times = {label:[] for (label,func) in funcs};

    print("Benchmark started")
    
    for iteration in range(iterations):
        print("{}%".format(100*iteration/iterations))
        for (label,func) in funcs:
            total_scalar_time = 0; total_tuple_time = 0
            for n in range(start_size,end_size,step):
                stdout_capture = io.BytesIO()
                with stdout_redirector(stdout_capture):
                    func(n).sort()
                    tuplify(func(n)).sort()
                (scalar_time,tuple_time) = re.match('SORT TIME: (\d+)\nSORT TIME: (\d+)',
                                                    stdout_capture.getvalue().\
                                                    decode('utf-8')).groups()
                total_scalar_time += int(scalar_time)
                total_tuple_time += int(tuple_time)
            scalar_times[label].append(total_scalar_time)
            tuple_times[label].append(total_tuple_time)
                
    print("Benchmark ended")
    return (scalar_times, tuple_times)

def main():
    import pickle,sys
    pickle.dump(run_benchmark(1000,1000,100,10000), open(sys.argv[1],'wb'))

if __name__ == '__main__':
    main()
