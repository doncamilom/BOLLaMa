"""
    Setup file for bollama.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.4.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from setuptools import setup, find_packages

if __name__ == "__main__":

    __version__ = "0.0.1"

    try:
        setup(
            name="bollama",
            version=__version__,
            description="Natural Language interface to Bayesian Optimization in Chemistry",
            author="Bojana Rankovic & Andres M Bran",
            author_email="bojana.rankovic@epfl.ch",
            url="https://github.com/doncamilom/BoLLaMa",
            license="MIT",
            packages=find_packages(),
            install_requires=[
                "rdkit",
                "pandas",
                "nest_asyncio",
                "gradio",
                "ansi2html",
                "langchain==0.0.173",
                "openai<1.0.0",
                "chaos @ git+https://github.com/schwallergroup/chaos.git@practical",
                "python-dotenv",
            ],
            extras_require={
                'extras': [
                    "graphein"
                ],
            },
            test_suite="tests",
            long_description_content_type="text/markdown",
            classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ],
        )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
