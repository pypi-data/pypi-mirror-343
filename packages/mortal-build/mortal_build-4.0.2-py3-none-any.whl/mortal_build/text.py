# cython: language_level=3
# #!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/16 17:14
@SoftWare: PyCharm
@Project: mortal
@File: text
"""


build_ext_setup_file_template = """#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from setuptools import setup
from Cython.Build import cythonize


"""


build_ext_setup_template = "setup(name='${name}', ext_modules=cythonize(r'${file}', " \
                           "compiler_directives={'language_level': 3, 'boundscheck': False, " \
                           "'initializedcheck': False}))\n"


build_wheel_setup_cfg_template = """[metadata]
name = wheel_name
description = 'wheel_desc'
version = wheel_version
author = wheel_author
long_description = 'wheel_long_desc'
long_description_content_type = wheel_long_type
classifiers = 
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent

[options]
python_requires = >=3.7
packages = find:
install_requires = wheel_install_requires

[options.entry_points]
console_scripts = wheel_console_scripts"""


build_wheel_setup_template = """#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from setuptools import setup


setup(include_package_data=True)
"""


build_params = {
    "name": "name", "desc": "desc", "version": "version", "author": "MJ", "long_desc": "long_desc",
    "long_desc_type": "text/markdown", "path": "path", "install_requires": [], "console_scripts": {},
    "skip_dir": [".idea", "__pycache__", "venv"], "remove": False
}
