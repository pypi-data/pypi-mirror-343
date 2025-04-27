from setuptools import setup, find_packages

setup(
    name='TDistributionClassifier',
    version='1.1.8',
    author='Abdul Mofique Siddiqui',
    author_email='mofique7860@gmail.com',
    description='A binary classifier using Student\'s t-distribution for univariate and multivariate continuous data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Luckyy0311',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'scipy',
    ],
)
