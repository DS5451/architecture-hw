import random

file = open("ls.trace", "r")
virtual_address = [] 
memRef = []
instruction_type = []
for line in file.readlines():
    memRef.append(line)
    line = list(filter(lambda element: element or element == 0, line.split(",")[0].split(" ")))
    instruction_type.append(line[0])
    virtual_address.append(line[1])


# Calculate page numbers
pageNum = []
cache_line = 4096

for address in virtual_address:
    x = int(address, 16)
    pageNum.append(x // cache_line)

# Putting together page number with line content
cache_data = []
cache_data_di = []
for index, value in enumerate(pageNum):
    cache_data.append([value, memRef[index]])
    cache_data_di.append([value, instruction_type[index], memRef[index]])


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

def CACHE_DI(cache_data_di, n):
    N = n
    CACHE_INST = {}
    inst_misses = 0
    inst_evictions = 0
    CACHE_DATA = {}
    data_misses = 0
    data_evictions = 0


    for data in cache_data_di:
        if data[1] == 'I':
            if data[0] not in CACHE_INST:
                inst_misses += 1
                if len(CACHE_INST)==N/2:
                    delkey = random.choice(list(CACHE_INST.keys()))
                    if delkey != data[0]:
                        inst_evictions += 1
                    del CACHE_INST[delkey]
                CACHE_INST[data[0]] = data[2]
        else:
            if data[0] not in CACHE_DATA:
                data_misses += 1
                if len(CACHE_DATA)==N/2:
                    delkey = random.choice(list(CACHE_DATA.keys()))
                    if delkey != data[0]:
                        data_evictions += 1
                    del CACHE_DATA[delkey]
                CACHE_DATA[data[0]] = data[2]



    return [[inst_misses, inst_evictions],[data_misses, data_evictions]]

# Testing function
results_misses = {}
results_evictions = {}


results_DI_misses_inst = {}
results_DI_evictions_inst = {}
results_DI_misses_data = {}
results_DI_evictions_data = {}

Nums = [8, 16, 32, 64, 128, 256, 512, 1024]
for N in Nums:
    cacheCall = CACHE(cache_data, N)
    results_misses[N] = cacheCall[0]
    results_evictions[N] = cacheCall[1]

for N in Nums:
    cacheCall = CACHE_DI(cache_data_di, N)
    results_DI_misses_inst[N] = cacheCall[0][0]
    results_DI_evictions_inst[N] = cacheCall[0][1]
    results_DI_misses_data[N] = cacheCall[1][0]
    results_DI_evictions_data[N] = cacheCall[1][1]


with open('cache_results.csv', 'w') as f:
    f.write('N, Misses, Evictions, , DI Inst Misses, DI Inst Evictions, DI Data Misses, DI Data Evictions\n')
    for N in Nums:
        f.write(f'{N}, {results_misses[N]}, {results_evictions[N]}, , '
                f'{results_DI_misses_inst[N]}, {results_DI_evictions_inst[N]}, '
                f'{results_DI_misses_data[N]}, {results_DI_evictions_data[N]}\n')
