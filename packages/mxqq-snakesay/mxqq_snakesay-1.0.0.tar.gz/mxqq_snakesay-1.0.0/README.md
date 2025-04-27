# pypi项目推送演示


## 本地打包：
```
python -m pip install -e .
```
验证是否打包成功：
```
# 查看是否有包
pip list 
# 执行命令查看
python -m snakesay "Hello World"
# 或均可以看到输出
ssay "Hello World"
```


> 我们通常pip install下载的包，需要到site-packages去修改代码才能生效，-e 的意思是可以编辑的含义，将本地代码和site-packages建立映射，这样修改本地源码就能生效。

## 推送到远端

安装必要的打包工具：
```
python -m pip install --upgrade pip
python -m pip install build twine
```
构建分发包
```
python -m build
```

上传到 PyPI：
```
python -m twine upload dist/*
```
上传时会要求输入你的 PyPI 用户名和密码
如果想先测试，可以上传到测试版 PyPI：
```
python -m twine upload --repository testpypi dist/*
```
验证安装：
```
pip install snakesay
```
或从测试版 PyPI 安装：
```
pip install --index-url https://test.pypi.org/simple/ snakesay
```

注意事项：
1. 请确保更新 pyproject.toml 中的个人信息（作者名称和邮箱）
2. 确保包名 "snakesay" 在 PyPI 上是可用的（没有被其他人使用）
3. 每次上传新版本时，需要在 pyproject.toml 中更新版本号
4. 建议先上传到 test.pypi.org 测试无误后再上传到正式的 PyPI