from setuptools import setup

setup(
    name='nii2mnc_u8',
    version='1.0.0',
    description='A ChRIS ds plugin wrapper for nii2mnc -unsigned -byte',
    author='Jennings Zhang',
    author_email='dev@babyMRI.org',
    url='https://github.com/FNNDSC/pl-nii2mnc-u8',
    py_modules=['nii2mnc_wrapper'],
    install_requires=['chris_plugin', 'loguru'],
    license='MIT',
    python_requires='>=3.10.2',
    entry_points={
        'console_scripts': [
            'nii2mnc_wrapper = nii2mnc_wrapper:main'
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
