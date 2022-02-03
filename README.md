# pl-nii2mnc-u8

`pl-nii2mnc-u8` is a _ChRIS_ _ds_ plugin wrapper around
[`nii2mnc`](http://bic-mni.github.io/man-pages/man/nii2mnc.html)
with hard-coded options `-unsigned -byte`.
It converts NIFTI images in its input directory into MINC files
in a specified output directory.
For every input file `N`, the output of the `nii2mnc` command
itself is saved to `{N}.nii2mnc.log`.

[![chrisstore.co](https://github.com/FNNDSC/cookiecutter-chrisapp/blob/master/doc/assets/badge/light.png?raw=true)](https://chrisstore.co/plugin/pl-nii2mnc-u8)

## Usage

```shell
singularity exec docker://fnndsc/pl-pl-nii2mnc-u8 nii2mnc_wrapper [-p PATTERN] input/ output/
```

## Examples

```shell
mkdir input output
mv mydata/*.nii input/
singularity exec docker://fnndsc/pl-pl-nii2mnc-u8 nii2mnc_wrapper -p '*.nii' input/ output/
```

### Development

#### Building

```shell
docker build -t localhost/fnndsc/pl-pl-nii2mnc-u8 .
```

#### Get JSON Representation

```shell
docker run --rm localhost/fnndsc/pl-pl-nii2mnc-u8 chris_plugin_info > Nii2mncU8.json
```

#### Local Test Run

```shell
docker run --rm -it --userns=host -u $(id -u):$(id -g) \
    -v $PWD/nii2mnc_wrapper.py:/opt/conda/lib/python3.10/site-packages/nii2mnc_wrapper.py:ro \
    -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw -w /outgoing \
    localhost/fnndsc/pl-pl-nii2mnc-u8 nii2mnc_wrapper /incoming /outgoing
```
