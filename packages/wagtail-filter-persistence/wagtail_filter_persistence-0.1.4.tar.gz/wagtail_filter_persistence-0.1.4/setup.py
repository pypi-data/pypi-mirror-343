from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="wagtail-filter-persistence",
    version="0.1.4",
    author="Emil P",
    author_email="emil@verdatek.com",
    description="A Wagtail plugin that persists filter selections in admin listings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/indigo7333/wagtail-filter-persistence",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 5",
    ],
    python_requires=">=3.6",
    install_requires=[
        "wagtail>=2.15",
    ],
     options={
        'bdist_wheel': {
            'universal': True,
        }
    },
)