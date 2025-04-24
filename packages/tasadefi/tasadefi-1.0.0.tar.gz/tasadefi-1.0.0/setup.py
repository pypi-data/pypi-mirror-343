from setuptools import setup, find_packages

setup(
      name="tasadefi",
      version="1.0.0",
      author="Vojtech Molek",
      description="Python random numbers",
      long_description=open("README.md").read(),
      long_description_content_type="text/markdown",
      url="https://github.com/Raverss/Python-Random-Types",
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires=">=3.6",
  )