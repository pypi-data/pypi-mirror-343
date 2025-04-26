
from setuptools import setup, find_packages

setup(
    name='idtec_core',
    version='1.5.0',
    author='IDTec Quantum Team',
    author_email='contact@idtecsecure.com',
    description='Post-Quantum Cryptographic Signature & Encryption Module for Python',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/idtec-secure/idtec_core',
    packages=find_packages(),
    install_requires=[
        'cryptography>=42.0.0',
        'pycryptodome>=3.19.0',
        'click>=8.1.3'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'idtec-sign=idtec_core.signer:main',
            'idtec-encrypt=idtec_core.crypto:encrypt_cli'
        ]
    },
    include_package_data=True,
    zip_safe=False
)
