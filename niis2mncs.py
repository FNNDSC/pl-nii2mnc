#!/usr/bin/env python

import itertools
import os
import shlex
import shutil
import subprocess as sp
import sys
from argparse import ArgumentParser, Namespace
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

from chris_plugin import chris_plugin, PathMapper
from loguru import logger

parser = ArgumentParser(description='ChRIS ds plugin wrapper around nii2mnc')
parser.add_argument('-p', '--pattern', default='**/*.nii,**/*.nii.gz',
                    help='pattern for file names to include')
parser.add_argument('-u', '--unsigned', action='store_true',
                    help='Write integer voxel data in unsigned format.')
parser.add_argument('-b', '--byte', action='store_true',
                    help='Write voxel data in 8-bit integer format.')


def niigz2mnc(niigz: Path, mnc: Path, flags: list[str], log_prefix='') -> tuple[str, Optional[Path], int]:
    """
    If input file is ``.gz`` compressed, copy it to a temporary location and run ``gzip -d``
    before calling `nii2mnc`. Descriptions of these actions are added to the accumulator ``log_prefix``.
    """

    if niigz.suffix != '.gz':
        return nii2mnc(niigz, mnc, flags, log_prefix)

    # copy NIFTI to temporary location
    temp_niigz = temp_file('.nii.gz')
    shutil.copy(niigz, temp_niigz)

    # decompress NIFTI
    cmd = ['gzip', '-d', temp_niigz]
    cmd_str = shlex.join(cmd)
    p = sp.run(cmd)
    if p.returncode != 0:
        return shlex.join(cmd), None, p.returncode

    # check decompressed NIFTI exists
    created_nii = Path(temp_niigz[:-len('.gz')])
    if not created_nii.is_file():
        log_file = mnc.with_suffix('.gzip.log')
        log_file.write_text(f'expected {created_nii} to be created, but it was not')
        return cmd_str, log_file, 0

    logs_so_far = [
        shlex.join(['cp', str(niigz), temp_niigz]),
        cmd_str,
        ''
    ]
    # call nii2mnc by calling niigz2mnc recursively
    ret = niigz2mnc(created_nii, mnc, flags, log_prefix=' && '.join(logs_so_far))

    # clean up intermediary decompressed NIFTI
    created_nii.unlink()
    return ret


def nii2mnc(nii: Path, mnc: Path, flags: list[str], log_prefix='') -> tuple[str, Path, int]:
    log_file = mnc.with_suffix('.nii2mnc.log')
    cmd = ['nii2mnc', *flags, str(nii), str(mnc)]
    cmd_str = shlex.join(cmd)
    logger.info('{}{}', log_prefix, cmd_str)
    with log_file.open('wb') as out:
        p = sp.run(cmd, stdout=out, stderr=out)
    return cmd_str, log_file, p.returncode


def temp_file(suffix: str) -> str:
    with NamedTemporaryFile(suffix=suffix) as temp:
        return temp.name


def name_mapper(file: Path, outputdir: Path):
    if file.suffix == '.gz':
        return name_mapper(file.with_suffix(''), outputdir)
    return outputdir / file.with_suffix('.mnc')


# documentation: https://fnndsc.github.io/chris_plugin/
@chris_plugin(
    parser=parser,
    title='nii2mnc (unsigned byte)',
    category='MRI Processing',
    min_memory_limit='500Mi',
    min_cpu_limit='1000m'
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    flags = ['-quiet']
    if options.unsigned:
        flags.append('-unsigned')
    if options.byte:
        flags.append('-byte')
    mapper = PathMapper.file_mapper(inputdir, outputdir, glob=options.pattern.split(','), name_mapper=name_mapper)

    with ThreadPoolExecutor(max_workers=len(os.sched_getaffinity(0))) as pool:
        results = pool.map(lambda t, f: niigz2mnc(*t, f), mapper, itertools.repeat(flags))

    any_failed = False
    for cmd, log_file, rc in filter(lambda t: t[2] != 0, results):
        any_failed = True
        logger.error('FAILED: {} > {} ({})', cmd, log_file, rc)

    if any_failed:
        sys.exit(1)


if __name__ == '__main__':
    main()
