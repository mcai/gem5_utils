#!/usr/bin/env python3

#
# A Python script to run all multi-core experiments for CPU2006 benchmarks.
#
# Copyright (C) Min Cai 2015
#

import os
import multiprocessing as mp

os.environ['M5_CPU2006'] = '/home/itecgo/Tools/CPU2006/'

def run(bench, l2_size, l2_assoc, num_threads):
    dir = 'results/' + bench + '/' + l2_size + '/' + str(l2_assoc) + 'way/' + str(num_threads) + 'c/'

    os.system('rm -fr ' + dir)
    os.system('mkdir -p ' + dir)

    cmd_run = '../gem5/build/X86_MESI_Two_Level/gem5.opt -d ' + dir + ' ../gem5/configs/example/se.py --cpu-type=timing --num-cpus=' \
              + str(num_threads) + ' --fast-forward=200000000 --maxinsts=2000000000' \
              + ' --bench=' + bench \
              + ' --caches --l2cache --num-l2caches=1' \
              + ' --l1d_size=32kB --l1i_size=32kB --l2_size=' + l2_size + ' --l2_assoc=' + str(l2_assoc)
    print(cmd_run)
    os.system(cmd_run)


def run_experiment(args):
    bench, l2_size, l2_assoc, num_threads = args
    run(bench, l2_size, l2_assoc, num_threads)

experiments = []


def run_experiments():
    num_processes = mp.cpu_count()
    pool = mp.Pool(num_processes)
    pool.map(run_experiment, experiments)

    pool.close()
    pool.join()


def add_experiment(bench, l2_size, l2_assoc, num_threads):
    args = bench, l2_size, l2_assoc, num_threads
    experiments.append(args)


def add_experiments(bench):
    add_experiment(bench, '256kB', 8, 4)
    # add_experiment(bench, '512kB', 8, 4)
    # add_experiment(bench, '1MB', 8, 4)
    # add_experiment(bench, '2MB', 8, 4)
    # add_experiment(bench, '4MB', 8, 4)
    # add_experiment(bench, '8MB', 8, 4)


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

for benchmark in benchmarks:
    add_experiments(benchmark)

run_experiments()
