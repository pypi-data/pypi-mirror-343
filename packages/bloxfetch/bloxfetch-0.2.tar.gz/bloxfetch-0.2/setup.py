from setuptools import setup, find_packages

setup(
    name='bloxfetch',
    version='0.2',
    description='A simple but advanced way for fetching roblox user info',
    long_description="Usage: To get the user: user = fetch_user(user_id).... Attributes: name, display_name, description, avatar_url, headshot_url",
    packages=find_packages(),
    install_requires=[
        'requests', 
    ]
)