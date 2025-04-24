from setuptools import setup, find_packages

setup(
    name="create_woragis_api",
    version="0.1",
    author="Woragis",
    author_email="masteringthecode.woragis@gmail.com",
    description="Create FastAPI backends with templates: REST, gRPC, AI",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",  # For CLI functionality
    ],
    extras_require={
        "rest": ["fastapi", "uvicorn"],
        "grpc": ["grpcio", "protobuf"],
        "ai-rest": ["fastapi", "uvicorn", "openai"],  # For OpenAI integration
        "ai-grpc": ["grpcio", "protobuf", "openai"],
        "rest-grpc": ["fastapi", "uvicorn", "grpcio", "protobuf"],
        "ai-rest-grpc": ["fastapi", "uvicorn", "grpcio", "protobuf", "openai"],
        # Example for data-science
        "data-science": ["pandas", "numpy", "scikit-learn", "matplotlib"],
        # Example ML extras
        "data-science-ml": ["pandas", "numpy", "scikit-learn", "matplotlib", "tensorflow"],
    },
    entry_points={
        "console_scripts": [
            "create-woragis-api=create_woragis_api.main:cli",
        ],
    },
    # Include package data, like templates and extras
    package_data={
        "create_woragis_api": [
            "templates/*",
            "extras/*",
        ],
    },
)
