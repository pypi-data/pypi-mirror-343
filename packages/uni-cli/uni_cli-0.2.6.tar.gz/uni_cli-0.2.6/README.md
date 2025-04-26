### 项目使用 uv 管理虚拟环境

> https://docs.astral.sh/uv/

### 项目依赖安装

-   `uv sync`:同步 <u>pyproject.toml</u> 中的依赖
-   `uv pip install -r requirements.txt`:通过 pip 安装`requirements.txt`中的依赖<br/>

### 发布到 pypi

-   `uv build`

### command

```shell
uv sync
uv run example hello Xiaoming
uv run example goodbye Xiaoming --formal
uv run say -t hello
uv run os
uv run bitget spot btc,eth
uv run bitget mix popcat
uv run pyv
uv run sync grid
uv run sync strategy
uv run bitget spot btc,eth -p http://127.0.0.1:7890
uv run bitget spot btc,eth -p socks5h://127.0.0.1:7890
uv run bitget sync
uv run gate
```
