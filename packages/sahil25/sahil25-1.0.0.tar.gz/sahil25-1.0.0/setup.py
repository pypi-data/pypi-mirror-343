from setuptools import setup, find_packages

setup(
    name="sahil25",
    version="1.0.0",
    packages=find_packages(),
    description="Experiment for test purposes",
    author="Sahil Kirtane",
    author_email="kirtanesahil25@gmail.com",
    install_requires=[],  # Add any dependencies here
    entry_points={
        'console_scripts': [
            'exp1=sahil.exp1:main',
            'exp2a=sahil.exp2a:main',
            'exp2b=sahil.exp2b:main',
            'exp3a=sahil.exp3a:main',
	    'exp3b=sahil.exp3b:main',
	    'exp4a=sahil.exp4a:main',
	    'exp4b=sahil.exp4b:main',
	    'exp5a=sahil.exp5a:main',
	    'exp5b=sahil.exp5b:main',
	    'exp6=sahil.exp6:main',
	    'exp7a=sahil.exp7a:main',
	    'exp7b=sahil.exp7b:main',
	    'exp8a=sahil.exp8a:main',
	    'exp8b=sahil.exp8b:main',
	    'exp9=sahil.exp9:main',
            # Add similar entries for all your files
        ],
    },
)