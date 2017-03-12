from setuptools import setup, find_packages

setup(name='broadlink-http',
      version='0.1.0',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['broadlink-http=broadlink_http.broadlink_http:main',
                              'broadlink=broadlink_http.broadlink_cmd:main']
      },
      install_requires = ['broadlink'],
      include_package_data=True
)
