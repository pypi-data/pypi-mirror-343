from setuptools import setup, find_packages

setup(
    name='nevora',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas'
    ],
    description='Nevora: Transform raw sales and returns data into Nevada chart format for warranty and reliability analysis.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourname/nevora',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    python_requires='>=3.7',
)
