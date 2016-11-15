#!/usr/bin/env python


import mincemeat
import time
import glob

current_time = lambda : int(round(time.time() * 1000))

start_time = current_time()

all_files = glob.glob('D:\Fontys Classes\ADS\GCD\MapReduce\Gutenberg\Gutenberg\Gutenberg SF\*.*')
def file_contents(file_name):
    f = open(file_name, encoding = 'utf-8', errors = 'ignore')
    try:
        return f.read()
    finally:
        f.close()
data = dict((file_name, file_contents(file_name)) for file_name in all_files)

def mapfn(k, v):
    import stopwords    # Otherwise throws error, should pass it with the function

    for w in v.split():
        if(w.lower() not in stopwords.allStopWords and (w.lower().isalnum() and len(w) > 1)):
            yield w, 1

def reducefn(k, vs):
    result = 0
    for v in vs:
        result += v
    return result

s = mincemeat.Server()

# The data source can be any dictionary-like object
s.datasource = dict(enumerate(data.values()))
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")

#sort results from high to low
results = sorted(results.items(), key=lambda x: x[1], reverse=True)
#print results
i = open('outfile','w')
i.write(str(results))
i.close()


print(results)

stop_time = current_time()

print('Start time: ' + str(start_time))
print('Stop time: ' + str(stop_time))
print('It took: ' + str(stop_time - start_time) + ' ms')