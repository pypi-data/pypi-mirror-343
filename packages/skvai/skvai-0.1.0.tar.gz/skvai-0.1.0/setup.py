from setuptools import setup, find_packages

setup(
    name="skvai",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scikit-learn",
        "tensorflow",
        "seaborn",
         "click",
    ],
    entry_points={
        'console_scripts': [
            'skvai = skvai.__main__:main',
        ],
    },
) 
