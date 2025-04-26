from setuptools import setup, find_packages

setup(
    name = "imgfit",
    version = "0.3.2",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires = ["pillow >= 8", "matplotlib >= 3.4", "PyLaTeXenc >= 2"],
    python_requires = ">=3.7",
    author = "xystudio",
    author_email = "173288240@qq.com",
    description = "Change your images.",
    long_description = open("README.md",encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license = "MIT",
    url = "https://github.com/xystudio889/imgfit",
    entry_points={
        "console_scripts": [
            "img = img_fit.__init__:main",
        ]
    }, 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords = "image, fit, latex, pillow",
)
