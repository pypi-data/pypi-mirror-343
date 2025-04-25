from setuptools import setup, find_packages

setup(
    name="sahil25",
    version="1.0.1",
    # Include only the renamed package directory 'sahil25' and its subpackages
    packages=find_packages(include=["sahil25", "sahil25.*"]),
    include_package_data=True,
    description="Experiment for test purposes",
    author="Sahil Kirtane",
    author_email="kirtanesahil25@gmail.com",
    install_requires=[
        # Add any runtime dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Top‐level launcher for listing/running experiments
            'sahil25 = sahil25.__main__:main',
            # Individual experiment commands
            'exp1 = sahil25.exp1:main',
            'exp2a = sahil25.exp2a:main',
            'exp2b = sahil25.exp2b:main',
            'exp3a = sahil25.exp3a:main',
            'exp3b = sahil25.exp3b:main',
            'exp4a = sahil25.exp4a:main',
            'exp4b = sahil25.exp4b:main',
            'exp5a = sahil25.exp5a:main',
            'exp5b = sahil25.exp5b:main',
            'exp6 = sahil25.exp6:main',
            'exp7a = sahil25.exp7a:main',
            'exp7b = sahil25.exp7b:main',
            'exp8a = sahil25.exp8a:main',
            'exp8b = sahil25.exp8b:main',
            'exp9 = sahil25.exp9:main',
        ],
    },
)
