from setuptools import setup, find_packages

setup(
    name='lokall',
    version='0.1.0',
    description='Moteur de recherche Lokall',
    author='Arthur ELLIES',
    author_email='lokall@openstudy.me',
    packages=find_packages(),
    install_requires=[
        # Liste des dépendances si nécessaire
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
