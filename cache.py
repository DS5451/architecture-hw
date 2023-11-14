""" 
***SETTING UP CACHE INFO***:

zip file contains memory references
first symbol is access type
I = instruction
L = load
S = store
M = modify

this is followed by a virtual address
whatever is after the comma is incorrect

ps = page size is 4kb (4096 bytes)
vs = virtual address
page number is determined by dividing the full virtual address and rounding down the result
pn = vs/ps

***CACHE INFO***:
TODO:
    - CACHE WILL BE LIST OF LISTS
    - LENGTH N
    - FIRST ITEM WILL INDICATE PAGE NUMBER
    
    - cache starts in a cold state meaning all lines are invalid

    -Go through each memory reference and check if its in the cache



simulate a fully associative CPU level 1 cache

cache line equals the page size (4096)
the page number serves as the associative key
the page content is the line itself
cache will have N entries
when it reaches capactiy the cache will randomly select and evict one of the cache lines


***RESULTS/SIMULATIONS***:

Run the cache simulation using the provided trace file for different cache sizes(N = 8,16,32,64,128,256,512,1024)
For each run record the number of misses and line evictions

Chart one is cache misses vs N
chart two is cache line evictions vs N
Analyze the charts and provide an explanation of the observed trends and patterns
how does cache influence the number of cache misses and evictions

"""
import random
import pandas as pd

file = open("ls.trace", "r")
virtual_address = [] 
memRef = []

#need a list of just virtual addresses to calculate page number 
#need a list of content

for line in file.readlines():
    memRef.append(line)
    line = list(filter(lambda element: element or element == 0,line.split(",")[0].split(" ")))[1]
    virtual_address.append(line)


#calculate page numbers
pageNum = []
cache_line = 4096

for address in virtual_address:
    x = int(address, 16)
    pageNum.append(x//cache_line)

#putting together page number with line content
cache_data = []
for index, value in enumerate(pageNum):
    cache_data.append([value,memRef[index]])

#now creating the cache function
def CACHE(cache_data,n):
    N = n
    hits = 0
    misses = 0

    cache = {}
    for i in cache_data:
        if(len(cache)==N):
            delkey = random.choice(list(cache.keys()))
            del cache[delkey]



        if i[0] in cache:
            hits+=1
        if i[0] not in cache:
            misses+=1
            cache[i[0]] = i[1]

    return[hits, misses]

#testing function
results_hits = {}
results_misses = {}

Nums = [8,16,32,64,128,256,512,1024]
for N in Nums:
    cacheCall = CACHE(cache_data, 8)
    results_hits[N] = cacheCall[0]
    results_misses[N] = cacheCall[1]

data = {
    'N': [],
    'Hits': [],
    'Misses': []
}

for N in Nums:
    data['N'].append(N)
    data['Hits'].append(results_hits[N])
    data['Misses'].append(results_misses[N])

# Create DataFrame
df = pd.DataFrame(data)

# Export to CSV
df.to_csv('cache_results.csv', index=False)

    
