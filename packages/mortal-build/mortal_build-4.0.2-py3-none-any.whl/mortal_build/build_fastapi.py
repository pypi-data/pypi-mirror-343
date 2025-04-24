#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/10/15 20:00
@SoftWare: PyCharm
@Project: mortal
@File: build_flask.py
"""
import hashlib
import os
import sys

import click
import jwt
import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from mortal_bases import MortalBases

from .text import build_ext_setup_file_template
from .text import build_ext_setup_template

bases = MortalBases()


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
            bases.path_copy(tmp_file, pack_file)
            bases.path_delete(tmp_file)


def _conda_init_modify():
    if os.name != "nt":
        if os.path.exists("~/.pydistutils.cfg"):
            with open("~/.pydistutils.cfg", "r", encoding="utf-8") as f:
                data = f.read()
            data = data.replace("index-url", "index_url")
            with open("~/.pydistutils.cfg", "w", encoding="utf-8") as f:
                f.write(data)


@click.command()
@click.option("--port", "-p", default=5000, help="api-port")
def build_api(port):
    app = FastAPI()
    root_path = os.getcwd()
    path = os.path.join(root_path, "test_build")
    os.makedirs(path, exist_ok=True)
    _conda_init_modify()

    @app.get('/')
    def index():
        return {"message": "build api ready"}

    @app.post('/build')
    async def build_index(request: Request):
        data = await request.json()
        token_dict = jwt.decode(data.get("token"), "mortal_build", issuer="mortal", algorithms=['HS256'])
        result = token_dict.get("data")
        content = result.get('content')
        md5_result = hashlib.md5()
        if isinstance(content, bytes):
            md5_result.update(content)
        else:
            md5_result.update(content.encode(encoding="utf-8"))
        md5_result = md5_result.hexdigest()
        md5 = md5_result.upper()
        file_name = result.get('file_name')
        tmp_path = os.path.join(os.getcwd(), "test_build", md5)
        os.makedirs(tmp_path, exist_ok=True)
        with open(os.path.join(tmp_path, file_name), "w", encoding="utf-8") as f:
            f.write(content)
        _build_ext_one(tmp_path, file_name, md5)
        os.chdir(root_path)
        return JSONResponse({"status": "success", "received": md5})

    @app.post('/file')
    async def file_index(request: Request):
        data = await request.json()
        md5 = data.get("sign")
        try:
            suffix = "pyd" if os.name == 'nt' else "so"
            file_path = os.path.join(path, md5, f"{md5}.{suffix}")
            return FileResponse(file_path)
        except(Exception,):
            return JSONResponse({"status": "failed", "received": md5}), 500

    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
