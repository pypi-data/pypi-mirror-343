from setuptools import setup

setup(
    name="DASHub",
    version="0.1.1",
    long_description="DAS Hub",
    long_description_content_type="text/markdown",
    packages=["dashub"],
    install_requires=["numpy",  "h5py", "matplotlib", "pandas"],
)
