from setuptools import setup, find_packages

setup(
    name='LabToolbox',
    version='1.0.6',
    packages=find_packages(),
    install_requires=[
        'numpy', 'scipy', 'matplotlib.pyplot', 'statsmodels.api', 'math', 'lmfit', 'corner', 'emcee'
    ],
    author='Giuseppe Sorrentino',
    author_email='sorrentinogiuse@icloud.com',
    description="LabToolbox è una raccolta di strumenti per l'analisi e l'elaborazione di dati sperimentali in ambito scientifico. Fornisce funzioni intuitive e ottimizzate per il fitting, la propagazione delle incertezze, la gestione dei dati e la visualizzazione grafica, rendendo più rapido e rigoroso il trattamento dei dati di laboratorio. Pensata per studenti, ricercatori e chiunque lavori con dati sperimentali, combina semplicità d'uso con rigore metodologico.",
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