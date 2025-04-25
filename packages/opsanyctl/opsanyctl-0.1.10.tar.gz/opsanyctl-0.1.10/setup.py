from setuptools import setup, find_packages

setup(
    name='opsanyctl',
    version='0.1.10',
    author='OpsAny',
    author_email='',
    description="OpsAny's command-line tool!",
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    # url='https://gitee.com/unixhot/opsany-paas',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "setuptools==58.3.0",
        "typer",
        "rich",
        "pyyaml",
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'opsanyctl=opsanyctl.main:app',
            'opsctl=opsanyctl.main:app',
        ],
    },
)
