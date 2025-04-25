from setuptools import setup, find_packages

setup(
    name='web3automation',
    version='1.1.5',
    author='zack',
    description='web automation for web3',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/username/my_package',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
