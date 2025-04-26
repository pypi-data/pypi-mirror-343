from setuptools import find_packages, setup

from typed_envs import description, description_addon


setup(
    name="typed-envs",
    packages=find_packages(),
    use_scm_version={
        "root": ".",
        "relative_to": __file__,
        "local_scheme": "no-local-version",
        "version_scheme": "python-simplified-semver",
    },
    description=description,
    author="BobTheBuidler",
    author_email="bobthebuidlerdefi@gmail.com",
    url="https://github.com/BobTheBuidler/typed-envs",
    license="MIT",
    setup_requires=["setuptools_scm"],
    package_data={"typed_envs": ["py.typed"]},
    long_description=description + description_addon,
)
