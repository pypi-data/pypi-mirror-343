from setuptools import setup,find_packages
import os

setup(name='mlstelemetry',
      version=os.getenv('CI_COMMIT_TAG',"0.0.0"),
      description='A library that wraps the OpenTelemetry Python SDK.',
      long_description=open("README.md").read(),
      long_description_content_type="text/markdown",
      author="MLSysOps Project Consortium",
      author_email="info@mlsysops.eu",
      license='Apache License 2.0',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      extras_require = {
            'dev': [''],
            'build': ['cachetools','opentelemetry-exporter-otlp','opentelemetry-exporter-otlp-proto-common',
                      'opentelemetry-exporter-otlp-proto-grpc',
                      'opentelemetry-api','opentelemetry-exporter-otlp-proto-http',
                      'opentelemetry-proto','opentelemetry-sdk',' opentelemetry-semantic-conventions','prometheus_client','asyncio']
      },
    classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.10",
        ],
)