#!/usr/bin/env python

import os
import argparse
from glob import glob


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", dest='input', help="path to directory for input file list")
    parser.add_argument("output_dir", dest='output', help="path to directory for output file list")
    parser.add_argument("-p", "--pattern", help="glob pattern for input files", default='*.xml')
    parser.add_argument("-o", "--output", dest='outpath', help="directory where filelists should be written")
    args = parser.parse_args()

    inpath = os.path.join(args.input, args.pattern)
    ins = []
    outs = []
    for i in glob(inpath):
        ins.append(i)
        fname, _ = os.path.splitext(os.path.basename(i))
        outs.append(os.path.join(args.output, fname + '.conllu'))

    finpath = os.path.join(args.outpath, 'input.fl') if args.outpath else 'input.fl'
    foutpath = os.path.join(args.outpath, 'output.fl') if args.outpath else 'output.fl'

    with open(finpath, 'w') as f:
        f.write("\n".join(ins))
    with open(foutpath, 'w') as f:
        f.write("\n".join(outs))
