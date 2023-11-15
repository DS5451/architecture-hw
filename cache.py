import random

file = open("ls.trace", "r")
virtual_address = [] 
memRef = []

for line in file.readlines():
    memRef.append(line)
    line = list(filter(lambda element: element or element == 0, line.split(",")[0].split(" ")))[1]
    virtual_address.append(line)

# Calculate page numbers
pageNum = []
cache_line = 4096

for address in virtual_address:
    x = int(address, 16)
    pageNum.append(x // cache_line)

# Putting together page number with line content
cache_data = []
for index, value in enumerate(pageNum):
    cache_data.append([value, memRef[index]])

# Now creating the cache function
def CACHE(cache_data, n):
    N = n
    misses = 0
    evictions = 0
    cache = {}

    for i in cache_data:
        if i[0] not in cache:
            misses += 1
            if len(cache) == N:
                delkey = random.choice(list(cache.keys()))
                if delkey != i[0]:
                    evictions += 1
                del cache[delkey]
            cache[i[0]] = i[1]  

    return [misses, evictions]

def CACHE_DI(cache_data, n):
    return []

# Testing function
results_misses = {}
results_evictions = {}


Nums = [8, 16, 32, 64, 128, 256, 512, 1024]
for N in Nums:
    cacheCall = CACHE(cache_data, N)
    results_misses[N] = cacheCall[0]
    results_evictions[N] = cacheCall[1]

# Writing results to a CSV file manually
with open('cache_results3.csv', 'w') as f:
    f.write('N,Misses,Evictions\n')
    for N in Nums:
        f.write(f'{N},{results_misses[N]},{results_evictions[N]}\n')
