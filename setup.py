import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="params-FranklinLi", # Replace with your own username
    version="0.0.1",
    author="Franklin Li",
    author_email="franklin_a_h_p@qq.com",
    description="Command line flags alternative for Jupyter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CourierKyn/params",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['ipywidgets>=7.5.1'],
)
