from setuptools import setup, find_packages

setup(
    name='ptl-si',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'mpmath',
        'skglm'
    ],
    author='Nguyen Vu Khai Tam, Cao Huyen My, Vo Nguyen Le Duy',
    author_email='22521293@gm.uit.edu.vn, 22520896@gm.uit.edu.vn, duyvnl@uit.edu.vn',
    description='PTL-SI: Statistical inference for high-dimensional regression after transfer learning',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/22520896/PTL_SI',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)