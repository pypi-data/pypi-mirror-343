# setup.py

from setuptools import setup, find_packages

setup(
    name='problemsolvr',
    version='1.0.0',
    author='Zain ul Abideen',
    author_email='zainthenpc03@gmail.com',
    description='An easy-to-use Python library for solving graph problems using classic search algorithms like BFS, DFS, A*, and Greedy with visualization support.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/problemsolvr',     packages=find_packages(),
    install_requires=[
        'matplotlib',
        'networkx'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)
