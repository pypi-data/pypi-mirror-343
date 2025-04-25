from setuptools import setup, find_packages
import os

# バージョン番号を直接指定
VERSION = '0.1.24'

# フォントファイルのパスを取得
def get_font_files():
    font_dir = os.path.join('cubicpy', 'font')
    return [os.path.join(font_dir, f) for f in os.listdir(font_dir) if f.endswith('.ttf')]

setup(
    name="cubicpy",
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "cubicpy": ["models/*.egg", "examples/*.py", "font/*.ttf"],
    },
    install_requires=[
        "panda3d",
        "websockets",
        "numpy",
        "scipy",
    ],
    scripts=['cubicpy/cli.py'],  # 明示的にスクリプトを指定
    entry_points={
        "console_scripts": [
            "cubicpy=cubicpy.cli:main",
        ],
    },
    author="creativival",
    author_email="creativival@gmail.com",
    description="A Python library for creating 3D basic shape models and animations with Physics.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/creativival/CubicPy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)