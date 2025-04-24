from distutils.core import setup

setup(name='amz_extractor',
      version='1.1.1',
      description='提取亚马逊详情页和评论信息',
      author='lonely',
      packages=['amz_extractor'],
      package_dir={'amz_extractor': 'amz_extractor'},
      install_requires=['dateparser>=1.1.4', 'pyquery>=1.4.3']
      )

"""
# 更新版本命令

python setup.py sdist bdist_wheel

twine upload dist/*

pypi-AgEIcHlwaS5vcmcCJGVlNmRiNTMxLTQyZTEtNDNkMS1iZGM5LTk3YTNiZjdmOGI1NAACFVsxLFsiYW16LWV4dHJhY3RvciJdXQACLFsyLFsiMTc1MjU0ZTEtZGUzOS00YTU1LWJlNTMtYmNkNDlhNjVjZmIzIl1dAAAGIOVRCwJiFoE6gR8dilK5H7k5TMh78w8uG12u6HMOLsCn


"""