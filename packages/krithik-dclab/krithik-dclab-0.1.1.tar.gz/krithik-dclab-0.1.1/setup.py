from setuptools import setup, find_packages

setup(
      name="krithik-dclab",
      version="0.1.1",
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          "click>=8.0",
      ],
      entry_points={
          "console_scripts": [
              "dclab-print=krithik_dclab.cli:print_java_files",
          ],
      },
      author="Krithik Patil",
      author_email="your.email@example.com",
      description="A package to print Java source code from Distributed Computing Lab experiments",
      long_description=open("README.md").read(),
      long_description_content_type="text/markdown",
      url="https://github.com/yourusername/krithik-dclab",
      license="MIT",
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires=">=3.6",
  )