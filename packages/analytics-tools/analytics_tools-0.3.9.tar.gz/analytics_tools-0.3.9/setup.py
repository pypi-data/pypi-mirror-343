from setuptools import setup, find_packages

setup(
        name = 'analytics_tools',
        version = '0.3.9',
        description = 'A package to help data analysts at cotidian tasks, mainly EDA and ETL tasks',
        long_description = open('README.md').read(),
        long_description_content_type = 'text/markdown',
        author = 'Arnaldo Joao Bastos Junior',
        author_email = 'arnaldo.jbj@gmail.com',
        packages = find_packages(),
        install_requires = [
                            'pandas',
                            'numpy',
                            'IPython',
                            'matplotlib',
                            'seaborn',
                            'scipy'
                           ],
        classifiers = [
                        'Programming Language :: Python :: 3',
                        'License :: OSI Approved :: MIT License',
                        'Operating System :: OS Independent',
                      ],
        python_requires = '>=3.6',
)