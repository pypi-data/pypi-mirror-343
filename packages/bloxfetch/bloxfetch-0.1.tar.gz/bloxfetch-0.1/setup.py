from setuptools import setup, find_packages

setup(
    name='bloxfetch',
    version='0.1',
    description='A simple but advanced way for fetching ',
    long_description="Usage: To get the user: user = fetch_user().... Attributes: name, display_name, description, avatar_url, headshot_url",
    packages=find_packages(),
    install_requires=[
        'requests', 
    ]
)