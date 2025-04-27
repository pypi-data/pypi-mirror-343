from setuptools import setup, find_packages

setup(
    name='tetrayau',
    version='1.3.3',  # MUST bump to 1.3.2
    author='Michael Tass MacDonald (Abraxas618)',
    description='TetraYau: Hyperdimensional Sovereign Cryptography Suite',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Abraxas618/TetraYau',
    packages=find_packages(),  # ✅ correct
    include_package_data=True,
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
)
