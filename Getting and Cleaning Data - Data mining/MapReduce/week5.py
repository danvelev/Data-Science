#!/usr/bin/env python
import mincemeat
import glob
import operator
import time

current_milli_time = lambda: int(round(time.time() * 1000))

startTime = current_milli_time()

print('Trying to acces the map')
all_files = glob.glob('Gutenberg/Gutenberg SF/*.*')

print('Creating function to read the files')
def file_contents(file_name):
    f = open(file_name, encoding="charmap")
    try:
        return f.read()
    except UnicodeEncodeError:
        f.close()
    finally:
        f.close()
        
print('Getting the datasource')
data = dict((file_name, file_contents(file_name)) for file_name in all_files)

lists = []
for file_name in all_files:
    print('Getting the text for : ' + file_name)
    text = data[file_name]
    lists.append(text)
    #print(text)
    
    #print('Removing all the special characters')
    #textWithoutSpecial = re.sub('[^a-zA-Z0-9-_ ]', '', text)
    #print(textWithoutSpecial)
    
    #print('Getting all words, also avoiding all words with less the 2 characters')
    #words = [x.lower() for x in textWithoutSpecial.split(' ')]
    #print(words)
    
    #lists.append(words)

def mapfn(k, v):
    import re
    import stopwords
    textWithoutSpecial = re.sub('[^a-zA-Z0-9-_ ]', '', v)
    
    print('Filtering')
    for w in [x.lower() for x in textWithoutSpecial.split(' ') if len(x) > 1 and x.lower() not in stopwords.allStopWords]:
        yield w, 1

def reducefn(k, vs):
    result = 0
    for v in vs:
        result += v
    return result

s = mincemeat.Server()

# The data source can be any dictionary-like object
s.datasource = dict(enumerate(lists))
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")

print('Sort')
results = sorted(results.items(), key=lambda x: x[1], reverse=True)
#print results
i = open('outfile','w')
i.write(str(results))
i.close()
print('List sorted')

index = 1
for item in results[:10]:
    print(index, item)
    index = index + 1
    
stopTime = current_milli_time()

print(startTime)
print(stopTime)
print('It took:')
print(stopTime - startTime)
print('Ms:')
