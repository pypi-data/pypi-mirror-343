from setuptools import setup, find_packages

setup(
    name="qgbot",
    version="1.0.0",
    author="LoQiseaking69",
    author_email="REEL0112359.13@proton.me",
    description="Modular Quant-Grade Intelligent Volatility-Aware ETH Grid Trading Bot",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LoQiseaking69/qgbot",
    license="BSD-3-Clause",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "quantgridbot=qgbot.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Software Development :: Libraries",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords=[
        "ethereum",
        "grid trading",
        "quantitative trading",
        "decentralized finance",
        "volatility trading",
        "crypto trading bot",
        "uniswap",
        "ethereum bot",
        "python trading bot",
        "crypto bot",
    ],
)
