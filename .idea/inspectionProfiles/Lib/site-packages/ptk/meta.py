# -*- coding: UTF-8 -*-

# (c) Jérôme Laheurte 2015-2019
# See LICENSE.txt


class PackageInfo(object):
    version = '1.3.7'
    version_info = map(int, version.split('.'))

    project_name = 'ptk'
    project_url = 'https://github.com/fraca7/ptk'
    download_url = 'https://pypi.python.org/packages/source/p/ptk/ptk-%s.tar.gz' % version

    author_name = 'J\u00E9r\u00F4me Laheurte'
    author_email = 'jerome@jeromelaheurte.net'

    short_description = 'LR(1) parsing framework for Python with support for asynchronous input'


version = PackageInfo.version
version_info = PackageInfo.version_info
