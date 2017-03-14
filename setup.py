from setuptools import setup, find_packages

setup(name='broadlink-http',
      version='0.1.0',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['broadlink-http=broadlink_http.http:main',
                              'broadlink-httpd=broadlink_http.httpd:main',
                              'broadlink=broadlink_http.broadlink_cmd:main']
      },
      install_requires = ['broadlink',
                          'python-daemon'],
      include_package_data=True
)

