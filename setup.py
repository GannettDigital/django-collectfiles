from setuptools import setup, find_packages

setup(name="django-collectfiles",
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires=[
        "django>=1.4,<1.5",
      ],
      version="0.0.1",
)

