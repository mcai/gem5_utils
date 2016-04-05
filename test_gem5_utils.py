from gem5_utils import parse_result, to_csv

benchmarks = [
    'blackscholes',
    'bodytrack',
    'canneal',
    'dedup',
]

# l2_sizes = ['256kB', '512kB', '1MB', '2MB', '4MB', '8MB']
l2_sizes = ['256kB']

l2_replacement_polices = ['LRU', 'IbRDP', 'RRIP']

results = []

for benchmark in benchmarks:
    for l2_size in l2_sizes:
        for l2_replacement_policy in l2_replacement_polices:
            results.append(
                parse_result('/home/itecgo/gem5_hmm_llc_replacement/results/alpha_no_checkpoints/' +
                             benchmark + '/simsmall/' + l2_size + '/8way/' + l2_replacement_policy + '/4c/',
                             benchmark=benchmark,
                             l2_size=l2_size,
                             l2_replacement_policy=l2_replacement_policy)
            )

print('system.l2.size: ' + str(results[0].configs['system.l2.size']))

for i in range(4):
    print(
        '[phase ' + str(i) + '] system.switch_cpus0.numCycles: ' + results[0].stats[i]['system.switch_cpus0.numCycles'])

to_csv('result.csv', results, [
    ('Benchmark', lambda r: r.props['benchmark']),
    ('L2 Size', lambda r: r.props['l2_size']),
    ('L2 Replacement Policy', lambda r: r.props['l2_replacement_policy']),
    ('# Cycles', lambda r: r.stats[3]['system.switch_cpus0.numCycles'])
])