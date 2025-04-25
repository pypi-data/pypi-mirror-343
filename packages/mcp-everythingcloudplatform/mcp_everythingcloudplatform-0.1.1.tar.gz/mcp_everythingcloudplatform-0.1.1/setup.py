from setuptools import setup, find_packages
setup(
    name='mcp_everythingcloudplatform',
    version='0.1.1',
    description='MCP Demo Everything Cloud Platform',
    author='Jai Chenchlani',    
    install_requires=[
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mcp_hello=mcp_everythingcloudplatform.main:hello',
            'mcp_add=mcp_everythingcloudplatform.main:add',
            'mcp_multiply=mcp_everythingcloudplatform.main:multiply',
        ],
    },
)