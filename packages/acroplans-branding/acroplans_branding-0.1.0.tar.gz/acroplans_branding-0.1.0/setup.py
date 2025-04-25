from setuptools import setup, find_packages

setup(
    packages=find_packages() + ['acroplans_branding.assets'],
    package_data={
        "acroplans_branding": ["assets/*"],
    },
)