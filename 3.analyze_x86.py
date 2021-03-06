#!/usr/bin/env python3
from gem5_utils import parse_result, to_csv, generate_plot

# Define benchmark names.
benchmarks = [
      #'400.perlbench',
      '401.bzip2',
      #'403.gcc',
      #'410.bwaves',
      #'416.gamess',
      #'429.mcf',
      #'433.milc',
      #'434.zeusmp',
      #'435.gromacs',
      #'436.cactusADM',
      #'437.leslie3d',
      #'444.namd',
      #'445.gobmk',
      #'450.soplex',
      #'453.povray',
      #'454.calculix',
      #'456.hmmer',
      #'458.sjeng',
      #'459.GemsFDTD',
      #'462.libquantum',
      #'464.h264ref',
      #'470.lbm',
      #'471.omnetpp',
      #'473.astar',
      #'482.sphinx3'
]


# Create CSVs and Figures illustrating the relationship between the L2 Cache Size and the L2 Miss Rate.
def parse_results_l2_sizes():
    results = []

    for benchmark in benchmarks:
        # for l2_size in ['256kB', '512kB', '1MB', '2MB', '4MB', '8MB']:
        # for l2_size in ['256kB', '512kB']:
        for l2_size in ['256kB']:
            results.append(
                parse_result('results/' +
                             benchmark + '/' + l2_size + '/8way/4c/',
                             benchmark=benchmark,
                             l2_size=l2_size)
            )

    to_csv('results/l2_sizes.csv', results, [
        ('Benchmark', lambda r: r.props['benchmark']),
        ('L2 Size', lambda r: r.props['l2_size']),
        ('L2 Miss Rate', lambda r: r.stats[0]['system.l2.overall_miss_rate::total']),
        ('# Cycles', lambda r: r.stats[0]['system.switch_cpus0.numCycles'])
    ])

    generate_plot('results/l2_sizes.csv',
                  'results/l2_sizes_vs_l2_miss_rate.pdf', 'Benchmark', 'L2 Miss Rate',
                  'L2 Size', 'L2 Miss Rate')
    generate_plot('results/l2_sizes.csv',
                  'results/l2_sizes_vs_num_cycles.pdf', 'Benchmark', '# Cycles',
                  'L2 Size', '# Cycles')

    return results


# Create CSVs and Figures illustrating the relationship between the L2 Cache Size and the L2 Miss Rate.
results_l2_sizes = parse_results_l2_sizes()

# Sample Usage: access configs from parsed results
print('system.l2.size: ' + str(results_l2_sizes[0].configs['system.l2.size']))

# Sample Usage: access stats from parsed results.
# Note: Here, the stats are an array of dictionaries, which corresponds to different program phases.
print('[phase ' + str(0) + '] system.switch_cpus0.numCycles: ' + results_l2_sizes[0].stats[i][
    'system.switch_cpus0.numCycles'])
