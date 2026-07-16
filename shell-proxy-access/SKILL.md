---
name: shell-proxy-access
description: 当 Git Bash / Shell 访问外网超时但浏览器能访问时，通过本地 SOCKS5/HTTP 代理临时访问目标服务，且不影响系统全局配置。
---

# Shell 代理访问指南（沙箱化）

## 核心原则

**只影响当前命令或当前终端，不写全局配置。**

- ✅ 推荐：单次命令加代理参数
- ✅ 可选：当前终端临时设置环境变量（关闭终端即失效）
- ❌ 不推荐：直接修改 `~/.bashrc`、`git config --global`、`npm config` 等全局配置

## 问题场景

浏览器能正常访问，但 Git Bash 里：

```text
* Connection timed out
* Failed to connect
```

常见服务：Docker Hub、GitHub、npm registry、PyPI、Go modules、任意外网 API。

## 前置信息

确认本地代理软件正在运行，并记录：

```text
SOCKS5: 127.0.0.1:10808  (Clash/V2Ray 常见)
HTTP:   127.0.0.1:7890   或 127.0.0.1:10809
```

具体端口以代理软件设置页为准。

## 推荐用法：单次命令加代理

### curl / wget

```bash
# SOCKS5
curl --socks5-hostname 127.0.0.1:10808 -sL https://hub.docker.com

# HTTP 代理
curl -x http://127.0.0.1:7890 -sL https://hub.docker.com

# wget
wget -e use_proxy=yes -e http_proxy=127.0.0.1:7890 https://example.com
```

### git（单次克隆/拉取）

```bash
# 单次生效，不写入全局配置
git -c http.proxy=socks5h://127.0.0.1:10808 \
    -c https.proxy=socks5h://127.0.0.1:10808 \
    clone https://github.com/xxx/xxx.git
```

### pip（单次安装）

```bash
pip install xxx --proxy http://127.0.0.1:7890

# 或用国内镜像（不依赖代理）
pip install xxx -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### npm（单次安装）

```bash
npm install xxx --proxy http://127.0.0.1:7890

# 或用国内镜像
npm install xxx --registry https://registry.npmmirror.com
```

## 可选用法：当前终端临时生效

如果当前终端里要连续执行多个命令，可以临时设置：

```bash
export ALL_PROXY=socks5h://127.0.0.1:10808
```

**效果：** 仅当前终端生效，关闭终端自动失效，不影响系统和其他程序。

取消：

```bash
unset ALL_PROXY
```

## 不推荐但可行：持久化配置（需用户明确同意）

以下操作会改变全局配置，**执行前必须确认用户确实需要**：

```bash
# git 全局代理
git config --global http.proxy socks5h://127.0.0.1:10808

# npm 全局代理
npm config set proxy http://127.0.0.1:7890
npm config set https-proxy http://127.0.0.1:7890

# ~/.bashrc 写入环境变量
echo 'export ALL_PROXY=socks5h://127.0.0.1:10808' >> ~/.bashrc
```

如果执行了，要同时提供撤销方法：

```bash
# 撤销 git 代理
git config --global --unset http.proxy
git config --global --unset https.proxy

# 撤销 npm 代理
npm config delete proxy
npm config delete https-proxy

# 撤销 ~/.bashrc 中的代理设置
sed -i '/ALL_PROXY=/d' ~/.bashrc
```

## 子 shell 沙箱方案（推荐批量操作）

想在隔离环境中执行多个命令，又不污染当前 shell：

```bash
(
  export ALL_PROXY=socks5h://127.0.0.1:10808
  curl -sL https://hub.docker.com
  git clone https://github.com/xxx/xxx.git
  npm install
)
```

括号 `()` 会创建子 shell，退出后 `ALL_PROXY` 不会泄漏到父 shell。

## 一键检测脚本

保存为 `proxy_test.sh`：

```bash
#!/bin/bash
TARGET=${1:-https://hub.docker.com}
SOCKS5_PROXY="127.0.0.1:10808"
HTTP_PROXY="127.0.0.1:7890"

echo "目标: $TARGET"
echo "--- 直连 ---"
curl -sI --max-time 8 "$TARGET" | head -1 || echo "失败"

echo "--- SOCKS5 $SOCKS5_PROXY ---"
curl --socks5-hostname "$SOCKS5_PROXY" -sI --max-time 8 "$TARGET" | head -1 || echo "失败"

echo "--- HTTP $HTTP_PROXY ---"
curl -x "http://$HTTP_PROXY" -sI --max-time 8 "$TARGET" | head -1 || echo "失败"
```

运行：

```bash
bash proxy_test.sh https://github.com
```

## Docker Desktop 特殊说明

`ALL_PROXY` 对 Docker Daemon 无效。如果用户需要 `docker pull` 走代理：

1. 在 Docker Desktop → Settings → Resources → Proxies 中填写代理地址
2. 重启 Docker Desktop

**但这是 Docker 的全局设置**，会影响所有 `docker pull` 行为。如果只是临时拉一个镜像，更推荐：

```bash
# 先在浏览器/代理环境下载镜像 tar
# 然后 docker load -i xxx.tar
```

## 常见端口参考

| 软件 | SOCKS5 | HTTP |
|------|--------|------|
| Clash Verge / Clash for Windows | 10808 | 10809 / 7890 |
| v2rayN | 10808 | 10809 |
| Shadowsocks (Windows) | 1080 | - |

## 沙箱检查清单

执行任何代理相关命令前，确认：

- [ ] 是否只影响当前命令/当前终端？
- [ ] 是否修改了 `~/.bashrc`、`~/.gitconfig`、`~/.npmrc` 等全局文件？
- [ ] 关闭终端后是否自动失效？
- [ ] 是否提供了撤销命令？
