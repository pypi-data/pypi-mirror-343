from setuptools import setup, find_packages

setup(
    name='tech_analysis',
    version='0.1.0',
    author='Bimal Kumar Shah',
    author_email='shah.bimal005@gmail.com',
    description='Pure Python technical analysis package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bimalkshah/technicalanalysis',
    packages=find_packages(),  # Automatically finds all packages and subpackages
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Change to your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=[
        # list your package dependencies here, for example:
        'requests>=2.0.0',
    ],
)
