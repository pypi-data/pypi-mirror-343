# cython: language_level=3
# #!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/16 17:12
@SoftWare: PyCharm
@Project: mortal
@File: build_main
"""
import os
import random
import re
import shutil
import string
import sys
import time
from datetime import datetime

import jwt
import requests
from mortal_bases import MortalBases

from .text import build_ext_setup_file_template
from .text import build_ext_setup_template
from .text import build_params
from .text import build_wheel_setup_cfg_template
from .text import build_wheel_setup_template


bases = MortalBases()


class MortalBuildMain:
    def __init__(self):
        self._management()

    @staticmethod
    def _management():
        key = 2374693573
        characters = string.ascii_letters + string.digits
        seed = int(datetime.now().strftime("%Y%m%d%H"))
        random.seed(int((seed + key + 1) / 9098))
        string1 = ''.join(random.choice(characters) for _ in range(32))
        random.seed(int((seed + key + 2) / 9098))
        string2 = ''.join(random.choice(characters) for _ in range(32))
        random.seed(int((seed + key + 3) / 9098))
        string3 = ''.join(random.choice(characters) for _ in range(32))
        content = MortalBases.auth_encode(MortalBases.auth_union(string1), string2)
        sign = MortalBases.auth_encode(MortalBases.auth_union(MortalBases.auth_decode(content, string2)), string3)
        value = MortalBases.auth_build("mortal-build", content)
        if sign != value:
            raise Exception("Unknown mortal anomaly")

    @staticmethod
    def _build_config():
        return build_params

    def _build_ext_wheel_pypi(self, config):
        wheel_path = self._build_ext_wheel(config)
        os.chdir(os.path.dirname(config.get("path")))
        os.system(f"twine upload {wheel_path}")
        print(f"上传成功：{wheel_path}")
        return wheel_path

    def _build_ext_wheel(self, config):
        self._build_ext(config, wheel=True)
        path = config.get("path")
        src_path = os.path.dirname(path)
        tgt_path = os.path.join(src_path, "ext")
        config["path"] = os.path.join(tgt_path, os.path.basename(path))
        whl_path = self._build_wheel(config, wheel=True)
        return whl_path

    @staticmethod
    def _build_ext_api(config, src_file, api_file, file_name):
        url = config.get("url")
        if not url:
            return
        try:
            trying = 0
            while trying < 5:
                result = requests.get(url).text
                if result == "build api ready":
                    break
                else:
                    trying += 1
                    print(f"获取文件失败 {trying} 次")
                    time.sleep(0.5)
            if trying > 1:
                raise Exception("获取文件失败，取消打包")
        except(Exception,) as err:
            raise Exception(f"获取文件失败，取消打包：{err}")
        with open(src_file, "r", encoding="utf-8") as f:
            content = f.read()
        token_data = {"content": content, "file_name": file_name}
        token_dict = {'data': token_data, 'iat': int(time.time()), 'iss': "mortal", "exp": int(time.time()) + 86400}
        data = jwt.encode(token_dict, "mortal_build", algorithm='HS256')
        res = requests.post(url + "/build", json={"token": data})
        md5 = res.json().get("received") if res.status_code == 200 else None
        if not md5:
            raise Exception(f"获取文件失败，取消打包：{res.text}")
        suffix = "so" if os.name == 'nt' else "pyd"
        print(f"生成{suffix}文件：{md5}.{suffix}")
        res = requests.post(url + "/file", json={"sign": md5})
        if res.status_code == 200:
            with open(api_file, "wb") as f:
                f.write(res.content)
            print(f"获取{suffix}文件：{md5}.{suffix}")
        else:
            raise Exception("获取文件失败，取消打包")

    @staticmethod
    def _build_ext_one(tmp_path, file_name, md5):
        os.chdir(bases.path_normal(tmp_path))
        suffix = "pyd" if os.name == 'nt' else "so"
        src_file = os.path.join(os.getcwd(), file_name)
        new_template = build_ext_setup_template.replace("${name}", f"test{suffix}")
        new_template = new_template.replace("${file}", src_file)
        setup_file_list = new_template
        content = build_ext_setup_file_template + setup_file_list
        setup_file = f"setup_{suffix}.py"
        with open(setup_file, "w") as f:
            f.write(content)
        os.system(f"{sys.executable} setup_{suffix}.py build_ext --inplace")
        bases.path_delete(setup_file)
        bases.path_delete(os.path.join(os.getcwd(), "build"))
        c_file = src_file.replace(".py", ".c")
        bases.path_delete(c_file)
        file_split = file_name.split(".")
        for i in os.listdir(os.getcwd()):
            i_split = i.split(".")
            if file_split[0] == i_split[0] and i_split[-1] == suffix:
                tmp_file = os.path.join(os.getcwd(), i)
                pack_file = os.path.join(os.getcwd(), f"{md5}.{suffix}")
                bases.path_delete(pack_file)
                shutil.copy(tmp_file, pack_file)
                bases.path_delete(tmp_file)

    def _build_ext(self, config, wheel=False):
        suffix = "pyd" if os.name == 'nt' else "so"
        path = config.get("path")
        name = config.get("name")
        version = config.get("version")
        src_path = os.path.dirname(path)
        target_path = config.get("target_path")
        if wheel:
            tgt_path = os.path.join(src_path, "ext")
        else:
            tgt_path = os.path.join(target_path, "ext")
        os.chdir(src_path)
        bases.path_delete(os.path.join(tgt_path, f"{name}-{version}"))
        os.makedirs(tgt_path, exist_ok=True)
        old_files = bases.path_file_dict(path, skip_dir=config.get("skip_dir"))
        ext_count = 1
        setup_file_list = list()
        for key, value in old_files.items():
            for i in value:
                src_file = bases.path_normal(os.path.join(src_path, key, i))
                print(f"正在处理：{src_file}")
                if i == "__init__.py" or not i.endswith(".py"):
                    continue
                api_file = src_file.replace(".py", ".so")
                self._build_ext_api(config, src_file, api_file, i)
                new_template = build_ext_setup_template.replace("${name}", f"test{ext_count}")
                new_template = new_template.replace("${file}", src_file)
                setup_file_list.append(new_template)
                ext_count += 1
        content = build_ext_setup_file_template + "".join(setup_file_list)
        setup_file = f"setup_{suffix}.py"
        with open(setup_file, "w") as f:
            f.write(content)
        os.system(f"{sys.executable} setup_{suffix}.py build_ext --inplace")
        bases.path_delete(setup_file)
        bases.path_delete(os.path.join(os.getcwd(), "build"))
        new_files = bases.path_file_dict(path, skip_dir=config.get("skip_dir"))
        ext_total = sum([len(value) for key, value in new_files.items()])
        ext_count = 0
        for key, value in new_files.items():
            for i in value:
                tgt_dir = os.path.join(tgt_path, key)
                os.makedirs(tgt_dir, exist_ok=True)
                ext_count += 1
                src_file = bases.path_normal(os.path.join(src_path, key, i))
                print(f"进度： {ext_count} / {ext_total}，源文件：{src_file}")
                if i.endswith(".c"):
                    bases.path_delete(src_file)
                    continue
                if i.endswith(f".{suffix}"):
                    i_split = i.split(".")
                    pack_file = bases.path_normal(os.path.join(tgt_path, key, f"{i_split[0]}.{i_split[-1]}"))
                    bases.path_delete(pack_file)
                    shutil.copy(src_file, pack_file)
                    bases.path_delete(src_file)
                    continue
                if i.endswith(f".so") or i.endswith(f".pyd"):
                    tgt_file = bases.path_normal(os.path.join(tgt_path, key, i))
                    shutil.copy(src_file, tgt_file)
                    bases.path_delete(src_file)
                    continue
                if i == "__init__.py" or (not i.endswith(".py") and not i.endswith(f".{suffix}")):
                    tgt_file = bases.path_normal(os.path.join(tgt_path, key, i))
                    shutil.copy(src_file, tgt_file)
                    continue
        if wheel:
            target_path = os.path.join(target_path or tgt_path, "ext")
            os.makedirs(target_path, exist_ok=True)
            bases.path_copy(os.path.join(tgt_path, name), os.path.join(target_path, f"{name}-{version}"))
        else:
            bases.path_move(os.path.join(tgt_path, name), os.path.join(tgt_path, f"{name}-{version}"))

    def _build_wheel(self, config, wheel=False):
        path = config.get("path")
        name = config.get("name")
        desc = config.get("desc")
        version = config.get("version")
        author = config.get("author")
        long_desc = config.get("long_desc")
        long_desc_type = config.get("long_desc_type")
        install_requires = config.get("install_requires")
        console_scripts = config.get("console_scripts")
        skip_dir = config.get("skip_dir")
        remove = config.get("remove")
        src_path = os.path.dirname(path)
        target_path = config.get("target_path") or src_path
        os.makedirs(os.path.join(target_path, "dist"), exist_ok=True)
        os.chdir(src_path)
        files = bases.path_file_dict(path, skip_dir=skip_dir)
        whl_files = [i for i in os.listdir(os.path.join(target_path, "dist")) if f"{name}-{version}-" in i]
        if whl_files and config.get("replace"):
            bases.path_delete(os.path.join(os.getcwd(), "dist", whl_files[0]))
        elif whl_files and not config.get("replace"):
            raise Exception(f"待打包的wheel版本已存在：{whl_files}，直接替换打包需添加参数 replace=True")
        with open("MANIFEST.in", "w", encoding="utf-8") as f:
            for key, value in files.items():
                for i in value:
                    src_file = os.path.join(key, i).replace("\\", "/")
                    if not src_file.endswith(".py"):
                        f.write(f"include {src_file}\n")
        content = re.sub(r"wheel_name", name, build_wheel_setup_cfg_template)
        content = re.sub(r"wheel_desc", desc, content)
        content = re.sub(r"wheel_version", version, content)
        content = re.sub(r"wheel_author", author, content)
        content = re.sub(r"wheel_long_desc", long_desc, content)
        content = re.sub(r"wheel_long_type", long_desc_type, content)
        install_requires = [f"\n    {i}" for i in install_requires]
        content = re.sub(r"wheel_install_requires", ''.join(install_requires), content)
        console_scripts = [f"\n    {key} = {value}" for key, value in console_scripts.items()]
        content = re.sub(r"wheel_console_scripts", ''.join(console_scripts), content)
        with open("setup.cfg", "w", encoding="utf-8") as f:
            f.write(content)
        with open("setup.py", "w", encoding="utf-8") as f:
            f.write(build_wheel_setup_template)
        os.system(sys.executable + " setup.py bdist_wheel")
        whl_files = [i for i in os.listdir(os.path.join(os.getcwd(), "dist")) if f"{name}-{version}-" in i]
        if not whl_files:
            raise Exception("打包wheel文件失败")
        self._get_lib_files(src_path, target_path, name, version, wheel)
        whl_path = self._get_wheel_path(target_path, src_path, name, version)
        if remove:
            bases.path_delete(os.path.join(os.getcwd(), "build"))
            bases.path_delete(os.path.join(os.getcwd(), "MANIFEST.in"))
            bases.path_delete(os.path.join(os.getcwd(), "setup.cfg"))
            bases.path_delete(os.path.join(os.getcwd(), "setup.py"))
            egg_dirs = [i for i in os.listdir(os.getcwd()) if ".egg-info" in i]
            for i in egg_dirs:
                bases.path_delete(os.path.join(os.getcwd(), i))
            if src_path != target_path:
                bases.path_delete(os.path.join(os.getcwd(), "dist"))
        return whl_path

    @staticmethod
    def _get_wheel_path(src_path, tgt_path, name=None, version=None):
        if src_path == tgt_path:
            whl_name = [i for i in os.listdir(os.path.join(src_path, "dist")) if f"{name}-{version}-" in i][0]
            return os.path.join(src_path, "dist", whl_name)
        dist_path = os.path.join(src_path, "dist")
        os.makedirs(dist_path, exist_ok=True)
        old_dist_path = os.path.join(tgt_path, "dist")
        whl_list = [i for i in os.listdir(old_dist_path)]
        whl_name = [i for i in whl_list if f"{name}-{version}-" in i][0]
        if src_path != tgt_path:
            bases.path_move(os.path.join(old_dist_path, whl_name), os.path.join(dist_path, whl_name))
            if len(whl_list) == 1:
                bases.path_delete(os.path.join(tgt_path, "dist"))
        return os.path.join(dist_path, whl_name)

    @staticmethod
    def _get_lib_files(src_path, tgt_path, name=None, version=None, wheel=False):
        lib_path = os.path.join(tgt_path, "lib")
        os.makedirs(lib_path, exist_ok=True)
        tgt_lib = os.path.join(lib_path, f"{name}-{version}")
        if wheel:
            bases.path_copy(os.path.join(os.path.dirname(src_path), name), tgt_lib)
        else:
            bases.path_copy(os.path.join(src_path, "build", "lib", name), tgt_lib)
