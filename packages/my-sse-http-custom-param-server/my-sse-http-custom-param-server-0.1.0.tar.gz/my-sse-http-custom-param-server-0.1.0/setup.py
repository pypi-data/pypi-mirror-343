from setuptools import setup, find_packages

setup(
    name='my-sse-http-custom-param-server',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'my-sse-http-custom-param-server=main:main',
        ],
    },
    install_requires=[
        'fastapi==0.115.12',
        'mcp==1.6.0',
    ],
    author='MCP Demo',
    author_email='mcp.demo@example.com',
    description='A custom MCP SSE HTTP Server with parameter support.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Framework :: FastAPI',
    ],
)