from setuptools import setup, find_packages

VERSION = '0.3' 
DESCRIPTION = 'Gabe similarity finder'
LONG_DESCRIPTION = 'A package to find similarity between a pair of genomes'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="FunnyPack", 
        version=VERSION,
        author="Dr Gabe O'Reilly",
        author_email="<g.oreilly@garvan.org,au>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],

        keywords=['python', 'test', 'Genetics', 'Diversity'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
