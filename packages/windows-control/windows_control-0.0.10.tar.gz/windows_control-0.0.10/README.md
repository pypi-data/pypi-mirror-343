# Project Name

[windows_control_python](https://pypi.org/project/windows-control/) is a project to generate a Python module named `windows_control`, which provides some simple and efficient ways to do manipulations on Windows systems(Especially on Win10). It is written in Rust using [PyO3](https://crates.io/crates/pyo3).

## Installation

```bash
pip install windows_control
```

## Requirements

- Setting for final usage: Python (version 3.9.11 or later)
- Extra setting for development: Rust (version 1.68 or later)

## Examples

(TODO)

## Contributing

### TODO
windows module
add opencv support,after that pub a new version: https://www.perplexity.ai/search/bc8f7e79-b31a-4ba6-8a7f-f94e239f4c77?s=u

### Prerequisites

Before contributing to the project, you need to know about PyO3. You can follow the instructions:
- [PyO3 getting start](https://pyo3.rs/v0.19.0/getting_started);
- [PyO3 guide](https://pyo3.rs/v0.19.0/building_and_distribution#manual-builds);
- [How to use maturin to publish a python package](https://www.maturin.rs/tutorial.html);
- [PyO3 Define a Class/Struct/Enum](https://pyo3.rs/v0.19.0/class.html#attribute-access).

### Manual Development

1. Install the python package `maturin` by running `pip install maturin` in terminal.
2. Make sure there is a virtual env at your project root directory. You can do it by running `python -m venv .venv` in terminal---the name `.venv` is specified for `maturin`. NOTE: please restart your terminal after creating the virtual env.
3. To add new features (like new funcs or new modules), modify the `src/lib.rs` file.
4. After making changes, generate the Python module by running `maturin develop`. This command generates a library in `target/debug`.
5. On Windows, rename the generated library file `[your_module].dll` to `[your_module].pyd`.
6. Finally, to test the generated library, run `python test.py` in the root directory to verify that the newly added features work correctly in Python.

### Automatic Development

If you have [just](https://crates.io/crates/just) installed, run just to automatically generate and test the project. The justfile contains specific commands for this purpose.

### Publish
First, update the field `version` in file `pyproject.toml`.

使用 API 令牌发布包有两种方式：

#### 方式一：使用环境变量（推荐）

在 Git Bash 中设置环境变量并发布：
```bash
export MATURIN_PYPI_TOKEN="pypi-YOUR_API_TOKEN_HERE"
source .venv/Scripts/activate
maturin publish
```

在 PowerShell 中设置环境变量并发布：
```powershell
$env:MATURIN_PYPI_TOKEN="pypi-YOUR_API_TOKEN_HERE"
.venv\Scripts\Activate.ps1
maturin publish
```

或者直接运行 `just pub` 命令，该命令已配置为在 Git Bash 中使用 API 令牌。

#### 方式二：使用 .pypirc 文件

在用户主目录（`%USERPROFILE%`）下创建 `.pypirc` 文件：
```
[pypi]
username = __token__
password = pypi-YOUR_API_TOKEN_HERE
```

然后运行：

在 Git Bash 中：
```bash
source .venv/Scripts/activate
maturin publish
```

在 PowerShell 中：
```powershell
.venv\Scripts\Activate.ps1
maturin publish
```

当你看到以下输出时，表示发布成功：
```bash
🚀 Uploading 2 packages
✨ Packages uploaded successfully
```

你可以在 [PyPI](https://pypi.org/project/windows-control/) 上查看发布的包。

Finally, update section `Examples` in both `README.md`(this file) and `README_PUB.md`.


## License

This project is licensed under the MIT License.
