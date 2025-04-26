from setuptools import setup, find_packages

setup(
    name="nia-cli",
    version="0.1.0",
    description="NIA Code Assistant CLI",
    author="Nozomio Labs",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer[all]>=0.9.0",
        "rich>=10.16.0",
        "requests>=2.28.0",
        "pydantic>=2.0.0",
    ],
    entry_points="""
        [console_scripts]
        nia=nia_cli.__main__:main
    """,
)