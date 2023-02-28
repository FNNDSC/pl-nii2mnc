#!/usr/bin/env python

import os
from pathlib import Path
from argparse import ArgumentParser, Namespace
from chris_plugin import chris_plugin, PathMapper
import subprocess as sp
from concurrent.futures import ThreadPoolExecutor
from loguru import logger


parser = ArgumentParser(description='ChRIS ds plugin wrapper around nii2mnc')
parser.add_argument('-p', '--pattern', default='**/*.nii',
                    help='pattern for file names to include')


def nii2mnc(nii: Path, mnc: Path):
    log_file = mnc.with_suffix('.nii2mnc.log')
    with log_file.open('wb') as out:
        sp.run(['nii2mnc', '-quiet', '-unsigned', '-byte', str(nii), str(mnc)],
               check=True, stdout=out, stderr=out)
    logger.info('Converted {} to {}', nii, mnc)


# documentation: https://fnndsc.github.io/chris_plugin/
@chris_plugin(
    parser=parser,
    title='nii2mnc (unsigned byte)',
    category='MRI Processing',
    min_memory_limit='500Mi',
    min_cpu_limit='1000m'
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    with ThreadPoolExecutor(max_workers=len(os.sched_getaffinity(0))) as pool:
        mapper = PathMapper.file_mapper(inputdir, outputdir, glob=options.pattern, suffix='.mnc')
        results = pool.map(lambda t: nii2mnc(*t), mapper)

    # raise any Exceptions
    for _ in results:
        pass


if __name__ == '__main__':
    main()
