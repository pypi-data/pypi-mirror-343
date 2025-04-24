from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="EridaSpeed",
    version="0.1.0",
    description="ВУВ (Виртуальный Ускоритель Вычислений) - ускоряет работу и скорость обучения трансформерных нейросетей в x2-x6 раз (GPT2 - в 40 раз)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Clos-Rise",
    author_email="chernaev.alex@mail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "torch>=1.10.0",
        "transformers>=4.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.7',
)
