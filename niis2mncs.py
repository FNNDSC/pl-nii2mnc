#!/usr/bin/env python

import itertools
import os
import shlex
import subprocess as sp
import sys
from argparse import ArgumentParser, Namespace
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from chris_plugin import chris_plugin, PathMapper
from loguru import logger

parser = ArgumentParser(description='ChRIS ds plugin wrapper around nii2mnc')
parser.add_argument('-p', '--pattern', default='**/*.nii',
                    help='pattern for file names to include')
parser.add_argument('-u', '--unsigned', action='store_true',
                    help='Write integer voxel data in unsigned format.')
parser.add_argument('-b', '--byte', action='store_true',
                    help='Write voxel data in 8-bit integer format.')


def nii2mnc(nii: Path, mnc: Path, flags: list[str]) -> tuple[str, Path, int]:
    log_file = mnc.with_suffix('.nii2mnc.log')
    cmd = ['nii2mnc', *flags, str(nii), str(mnc)]
    cmd_str = shlex.join(cmd)
    logger.info(cmd_str)
    with log_file.open('wb') as out:
        p = sp.run(cmd, stdout=out, stderr=out)
    return cmd_str, log_file, p.returncode



# documentation: https://fnndsc.github.io/chris_plugin/
@chris_plugin(
    parser=parser,
    title='nii2mnc (unsigned byte)',
    category='MRI Processing',
    min_memory_limit='500Mi',
    min_cpu_limit='1000m'
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    flags = ['-quiet', '-unsigned', '-byte']
    if options.unsigned:
        flags.append('-unsigned')
    if options.byte:
        flags.append('-byte')
    mapper = PathMapper.file_mapper(inputdir, outputdir, glob=options.pattern, suffix='.mnc')

    with ThreadPoolExecutor(max_workers=len(os.sched_getaffinity(0))) as pool:
        results = pool.map(lambda t, f: nii2mnc(*t, f), mapper, itertools.repeat(flags))

    any_failed = False
    for cmd, log_file, rc in filter(lambda t: t[2] != 0, results):
        any_failed = True
        logger.error('FAILED: {} > {} ({})', cmd, log_file, rc)

    if any_failed:
        sys.exit(1)


if __name__ == '__main__':
    main()
