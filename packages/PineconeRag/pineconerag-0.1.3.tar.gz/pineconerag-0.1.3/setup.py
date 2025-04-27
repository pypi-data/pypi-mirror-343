from setuptools import setup, find_packages

setup(
    name="PineconeRag",
    version="0.1.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pinecone-client>=5.0.1",
        "sentence-transformers>=2.2.2",
        "python-dotenv>=1.0.0",
    ],
    author="Kevin Freistroffer",
    author_email="kevin.freistroffer@gmail.com",
    description="A utility package for Pinecone RAG operations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KevinFreistroffer/Pinecone_RAG_retriever",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
