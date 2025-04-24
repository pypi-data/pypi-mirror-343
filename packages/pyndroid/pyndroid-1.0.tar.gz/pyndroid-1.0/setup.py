from setuptools import setup

setup(name='pyndroid',
      version='1.0',
      description='Android developing',
      packages=['pyndroid'],
      package_data={
            "pyndroid": ["resources/*.java", "resources/java/*.java", "resources/*.xml", "resources/layout/*.xml"]
      },
      author_email='a.s.ulmasov@yandex.ru',
      zip_safe=False)
