#!/usr/bin/env bash
cd ../gem5
scons build/X86_MESI_Two_Level/gem5.opt -j4
cd ../gem5_utils