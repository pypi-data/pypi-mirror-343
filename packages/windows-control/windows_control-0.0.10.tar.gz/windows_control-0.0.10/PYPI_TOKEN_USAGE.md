# 使用 PyPI API 令牌发布包

## 本地发布

### 方式一：使用环境变量（推荐）

1. 更新 `pyproject.toml` 中的版本号。

2. 在 Git Bash 中设置环境变量并发布：
```bash
export MATURIN_PYPI_TOKEN="pypi-AgEIcHlwaS5vcmcCJDc1YWEzZWFmLTE3NWEtNDllNi1hOTBmLWY4NTg1NDRmMDFlYgACKlszLCIyMTg3YTBkNS1iMTYyLTQ5ZTAtODkzMy0yMmQ2ZjAyNWVhZTciXQAABiAXtfEPcwepKallJAU2eYwun6vgEQqJYOBHpqOFu7qr2g"
source .venv/Scripts/activate
maturin publish
```

3. 在 PowerShell 中设置环境变量并发布：
```powershell
$env:MATURIN_PYPI_TOKEN="pypi-AgEIcHlwaS5vcmcCJDc1YWEzZWFmLTE3NWEtNDllNi1hOTBmLWY4NTg1NDRmMDFlYgACKlszLCIyMTg3YTBkNS1iMTYyLTQ5ZTAtODkzMy0yMmQ2ZjAyNWVhZTciXQAABiAXtfEPcwepKallJAU2eYwun6vgEQqJYOBHpqOFu7qr2g"
.venv\Scripts\Activate.ps1
maturin publish
```

4. 或者直接运行 `just pub` 命令，该命令已配置为在 Git Bash 中使用 API 令牌：
```bash
just pub
```

### 方式二：使用 .pypirc 文件

1. 更新 `pyproject.toml` 中的版本号。

2. 在用户主目录（`%USERPROFILE%`）下创建 `.pypirc` 文件：
```
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcCJDc1YWEzZWFmLTE3NWEtNDllNi1hOTBmLWY4NTg1NDRmMDFlYgACKlszLCIyMTg3YTBkNS1iMTYyLTQ5ZTAtODkzMy0yMmQ2ZjAyNWVhZTciXQAABiAXtfEPcwepKallJAU2eYwun6vgEQqJYOBHpqOFu7qr2g
```

3. 然后运行：
```powershell
.venv\Scripts\Activate.ps1
maturin publish
```

## GitHub Actions 自动发布

当你创建一个新的 Git 标签并推送到 GitHub 时，GitHub Actions 工作流程会自动构建并发布包。

1. 在 GitHub 仓库的 Settings -> Secrets -> Actions 中添加一个名为 `PYPI_API_TOKEN` 的密钥，值为你的 PyPI API 令牌。

2. 创建并推送一个新的 Git 标签：
```bash
git tag v0.0.11
git push origin v0.0.11
```

3. GitHub Actions 工作流程会自动构建并发布包到 PyPI。

## 注意事项

- PyPI API 令牌是敏感信息，不要将其提交到公共仓库中。
- 如果你在多台计算机上工作，每台计算机都需要配置 `.pypirc` 文件。
- 令牌有过期时间，过期后需要在 PyPI 网站上重新生成。
