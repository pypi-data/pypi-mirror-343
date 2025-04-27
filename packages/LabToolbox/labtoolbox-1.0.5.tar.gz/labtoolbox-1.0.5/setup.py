from setuptools import setup, find_packages

setup(
    name='LabToolbox',
    version='1.0.5',
    packages=find_packages(),
    install_requires=[
        'numpy', 'scipy', 'matplotlib.pyplot', 'statsmodels.api', 'math', 'lmfit', 'corner', 'emcee'
    ],
    author='Giuseppe Sorrentino',
    author_email='sorrentinogiuse@icloud.com',
    description="Libreria contenente funzioni potenzialmente utili per l'analisi di dati di laboratorio.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/tuo-username/tuo-pacchetto',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',  # Aggiungi questa linea
)