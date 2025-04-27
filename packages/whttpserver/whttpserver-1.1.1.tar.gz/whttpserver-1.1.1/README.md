# whttpserver

whttpserver 是一个简单的HTTP服务器，类似于`python -m http.server`，但增加了文件上传和下载功能。

## 功能

- **文件上传**：用户可以通过Web界面上传文件到服务器指定的目录。
- **文件下载**：用户可以浏览服务器上的目录，并下载文件。
- **目录浏览**：用户可以查看服务器上的文件和子目录。

## 安装

如果没有pip，可以先安装pip，python2的安装方式如下：

```bash
wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
python get-pip.py
```

python3的安装方式如下：

```bash
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
```

## 使用

运行服务器：

```bash
python -m whttpserver --port <port_number> --dir <root_directory> --debug <debug_mode>
```

- `--port <port_number>`：设置服务器监听的端口号，默认为25000。
- `--dir <root_directory>`：设置文件上传和下载的根目录，默认为`/data/`。
- `--debug <debug_mode>`：设置调试模式，默认为`True`。

### Python 2 和 Python 3 环境

whttpserver 可以在Python 2和Python 3环境下运行。确保安装了Flask：

```bash
# Python 2
pip install flask

# Python 3
pip3 install flask
```

在Python 2环境下运行：

```bash
python2 -m whttpserver --port <port_number> --dir <root_directory> --debug <debug_mode>
```

在Python 3环境下运行：

```bash
python3 -m whttpserver --port <port_number> --dir <root_directory> --debug <debug_mode>
```

## 配置

- `UPLOAD_FOLDER`：设置文件上传的目录，默认为`/data/`。

## 路由

- `/`：显示根目录下的文件和目录。
- `/upload`：上传文件接口。
- `/download/<filename>`：下载指定文件。

## 注意事项

- 确保`UPLOAD_FOLDER`目录存在，并具有写权限。