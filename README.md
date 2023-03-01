# pl-nii2mnc

[![Version](https://img.shields.io/docker/v/fnndsc/pl-nii2mnc?sort=semver)](https://hub.docker.com/r/fnndsc/pl-nii2mnc)
[![MIT License](https://img.shields.io/github/license/fnndsc/pl-nii2mnc)](https://github.com/FNNDSC/pl-nii2mnc/blob/main/LICENSE)
[![Build](https://github.com/FNNDSC/pl-nii2mnc/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/pl-nii2mnc/actions)

`pl-nii2mnc` is a _ChRIS_ _ds_ plugin wrapper around
[`nii2mnc`](http://bic-mni.github.io/man-pages/man/nii2mnc.html).
It converts NIFTI images in its input directory into MINC files
in a specified output directory.
For every file in its input directory `N`, the output of the `nii2mnc`
command itself is saved to `{N}.nii2mnc.log`.

[![chrisstore.co](https://github.com/FNNDSC/cookiecutter-chrisapp/blob/master/doc/assets/badge/light.png?raw=true)](https://chrisstore.co/plugin/pl-nii2mnc)

## Usage

```shell
apptainer exec docker://fnndsc/pl-nii2mnc niis2mncs [--unsigned] [--byte] input/ output/
```

`input/` should be a directory of `.nii` (NIFTI) or `.nii.gz` (compressed NIFTI) files.

## Examples

```shell
mkdir input output
cp examples/incoming/* input/
apptainer exec docker://fnndsc/pl-nii2mnc niis2mncs --unsigned --byte input/ output/
```
