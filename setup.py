from setuptools import setup

setup(
    name='niis2mncs',
    version='1.1.0',
    description='A ChRIS ds plugin wrapper for nii2mnc, which converts NIFTI (.nii, .nii.gz) to MINC (.mnc)',
    author='Jennings Zhang',
    author_email='Jennings.Zhang@childrens.harvard.edu',
    url='https://github.com/FNNDSC/pl-nii2mnc',
    py_modules=['niis2mncs'],
    install_requires=['chris_plugin', 'loguru'],
    license='MIT',
    entry_points={
        'console_scripts': [
            'niis2mncs = niis2mncs:main'
        ]
    },
    extras_require={
        'none': [],
        'dev': [
            'pytest~=7.1'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ]
)
