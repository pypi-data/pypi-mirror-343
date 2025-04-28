from setuptools import setup, find_packages

setup(
    name="winiTranslate",  # Le nom de ton module
    version="0.1.0",  # La version de ton module
    packages=find_packages(),  # Trouve tous les packages Python dans le répertoire
    install_requires=[  # Les dépendances de ton module
        "googletrans==4.0.0-rc1",
    ],
    author="soldat205",  # Ton nom
    author_email="winhardydev@gmail.com",  # Ton email
    description="Un module simple pour traduire, détecter et lister les langues et simple a utiliser",  # Description courte
    long_description=open('README.md', encoding='utf-8').read(),  # Lire la description longue à partir du README
    long_description_content_type='text/markdown',  # Type de format pour la description longue
    classifiers=[  # Pour aider les utilisateurs à trouver ton module
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Version minimum de Python requise
    
)