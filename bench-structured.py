#These functions construct the different types of lists we will benchmark
funcs = []

def star_sort(n):
    random.seed(n)
    return [random.randint(-2**31,2**31) for _ in range(n)]
funcs.append(('*sort',star_sort))

def backslash_sort(n):
    L = list(range(n))
    L.reverse()
    return L
funcs.append(('\sort',backslash_sort))

def slash_sort(n):
    random.seed(n)
    return list(range(n))
funcs.append(('/sort',slash_sort))

def three_sort(n):
    random.seed(n)
    L = list(range(n))
    for _ in range(3):
        a = random.randint(0,n-1); b = random.randint(0,n-1)
        L[a], L[b] = L[b], L[a]
    return L
funcs.append(('3sort',three_sort))

def plus_sort(n):
    random.seed(n)
    return (list(range(n)) +
            [random.randint(0,n-1) for _ in range(10)])
funcs.append(('+sort',plus_sort))

def percent_sort(n):
    random.seed(n)
    L = list(range(n))
    for _ in range(n//100):
        L[random.randint(0,n-1)] = random.randint(0,n-1)
    return L
funcs.append(('%sort',percent_sort))

def tilde_sort(n):
    random.seed(n)
    L = [0]*(n//4) + [1]*(n//4) + [2]*(n//4) + [3]*(n//4)
    random.shuffle(L)
    return L
funcs.append(('~sort',tilde_sort))

def equal_sort(n):
    return [0]*n
funcs.append(('=sort',equal_sort))
    
#This is the main benchmark loop

#stdout_redirector from:
#https://raw.githubusercontent.com/berkerpeksag/python-playground/master/stdout_redirector.py
from stdout_redirector import stdout_redirector
import io, random, re

def run_benchmark(iterations,start_size,step,end_size):
    times = {label:[]for (label,func) in funcs};

    print("Benchmark started")
    
    for iteration in range(iterations):
        print("{}%".format(100*iteration/iterations))
        for (label,func) in funcs:
            total_time = 0
            for n in range(start_size,end_size,step):
                stdout_capture = io.BytesIO()
                with stdout_redirector(stdout_capture):
                    func(n).sort()
                (time,) = re.match('TOT (\d+)',
                                stdout_capture.getvalue().\
                                decode('utf-8')).groups()
                total_time += int(time)
            times[label].append(total_time)
                
    print("Benchmark ended")
    return times

def main():
    import pickle,sys
    pickle.dump(run_benchmark(500,1000,100,10000), open(sys.argv[1],'wb'))

if __name__ == '__main__':
    main()
