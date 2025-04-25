from setuptools import setup, find_packages

setup(
    name='odefinterp',
    version='0.1.38',
    description="ODEFormer but tweaked to aid interpretability",
    author="Soumyadeep Bose",
    author_email="soumyadeepboseee@gmail.com",
    packages=find_packages(),
    license="MIT",
    #download_url="https://github.com/sdascoli/odeformer/archive/refs/tags/v_01.tar.gz",
    install_requires=[
        "numexpr>=2.8.4",
        "sympy==1.11.1",
        "matplotlib",
        "numpy",
        "pandas",
        "requests",
        "scikit-learn",
        "scipy",
        "seaborn",
        "setproctitle",
        "torch>=2.0.0",
        "tqdm",
        "wandb",
        #"pysindy",
        "gdown",
        "regex"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
