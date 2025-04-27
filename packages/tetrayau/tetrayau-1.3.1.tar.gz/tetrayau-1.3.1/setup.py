# setup.py for TetraYau v1.3.1 — Sovereign Final Release

from setuptools import setup, find_packages

setup(
    name='tetrayau',
    version='1.3.1',  # updated version (important!)
    author='Michael Tass MacDonald (Abraxas618)',
    description='TetraYau: Hyperdimensional Sovereign Cryptography Suite',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Abraxas618/TetraYau',
    project_urls={
        'Documentation': 'https://github.com/Abraxas618/TetraYau',
        'IPFS Archive': 'https://ipfs.io/ipfs/bafkreiasrqitizdcgxprnxsxqn74w3hqkprilhtndvzzd3qjb3nkvphzgq',
        'OpenTimestamps Proof': 'https://ipfs.io/ipfs/bafkreihgkcy6kddlvjruufuuojo6dl5ys4msckgnwvufezqnijqrirccya',
    },
    packages=find_packages(where='tetrayau'),
    package_dir={'': 'tetrayau'},
    include_package_data=True,
    python_requires='>=3.8',

    license='Apache-2.0',  # ✅ SPDX modern license standard

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: Apache Software License',  # (still useful for PyPI)
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],

    keywords='cryptography post-quantum sovereign hyperdimensional tesseract blockchain tetrahedral encryption',
)
