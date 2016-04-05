#!/usr/bin/python
# -*- coding: UTF8 -*-
import csv
import json

import collections
from objectpath import *
from os import path
from pyparsing import Word, Optional, ParseException, printables, nums, restOfLine
from enum import Enum


class ExperimentType(Enum):
    FOUR_PHASE_FS_SIMULATION, THREE_PHASE_SE_SIMULATION = range(2)


class ExperimentResults:
    def __init__(self, configs, stats, props):
        self.configs = configs
        self.stats = stats
        self.props = props


class ExperimentConfigs:
    def __init__(self, raw_configs):
        self.raw_configs = raw_configs

    def __getitem__(self, index):
        return self.raw_configs.execute('$.' + index)


class ExperimentStats:
    def __init__(self, raw_stats):
        self.raw_stats = raw_stats

    def __getitem__(self, index):
        return self.raw_stats[index] if index in self.raw_stats else None


def read_configs(result_dir, config_json_file_name):
    try:
        with open(path.join(result_dir, config_json_file_name)) as config_json_file:
            configs = Tree(json.load(config_json_file))
    except Exception as e:
        print(e)
        return None
    else:
        return configs


def read_stats(result_dir, stats_file_name):
    stat_rule = Word(printables) + Word('nan.%' + nums) + Optional(restOfLine)

    stats = []

    try:
        with open(path.join(result_dir, stats_file_name)) as stats_file:
            i = 0
            for stat_line in stats_file:
                if len(stats) <= i:
                    stats.append(collections.OrderedDict())

                try:
                    stat = stat_rule.parseString(stat_line)
                    key = stat[0]
                    value = stat[1]

                    stats[i][key] = value
                except ParseException as e:
                    # print(e)
                    pass

                if 'End Simulation Statistics' in stat_line:
                    i += 1
    except Exception as e:
        print(e)
        return None
    else:
        return stats


def parse_result(result_dir, config_json_file_name='config.json', stats_file_name='stats.txt', **props):
    return ExperimentResults(ExperimentConfigs(read_configs(result_dir, config_json_file_name)),
                             [ExperimentStats(stat) for stat in read_stats(result_dir, stats_file_name)], props)


def to_csv(output_file_name, results, fields):
    with open(output_file_name, 'w') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        writer.writerow([field[0] for field in fields])

        for result in results:
            writer.writerow([field[1](result) for field in fields])


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
