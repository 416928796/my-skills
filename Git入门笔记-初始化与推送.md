# Git 入门笔记：初始化本地仓库并推送到 GitHub

> 场景：把本地一个已有的文件夹初始化为 Git 仓库，关联到 GitHub 远程仓库，并推送上去。

---

## 一、整体流程速记

```
配置用户信息（仅首次）
  ↓
git init                       初始化本地仓库
  ↓
git branch -M main             分支改名为 main
  ↓
git add .                      加入暂存区
  ↓
git commit -m "Initial commit" 提交
  ↓
git remote add origin <远程地址>   关联远程仓库
  ↓
git push -u origin main        推送到 GitHub
```

---

## 二、分步详解

### 第 0 步：准备工作

打开终端（Git Bash 或 PowerShell），切换到项目目录：

```bash
# Git Bash
cd /e/Code/021-skills

# PowerShell
cd e:\Code\021-skills
```

**第一次用 Git** 需要配置身份信息（仅需一次）：

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub注册邮箱"
```

验证配置：

```bash
git config user.name
git config user.email
```

---

### 第 1 步：初始化本地仓库

```bash
git init
```

执行后文件夹会多出隐藏的 `.git` 目录，表示已被 Git 管理。

---

### 第 2 步：把分支名改为 main

GitHub 默认分支名是 `main`，保持一致：

```bash
git branch -M main
```

---

### 第 3 步：查看文件状态（养成习惯）

```bash
git status
```

此时所有文件显示为「Untracked / 未跟踪」，属正常现象。

> ⚠️ 小知识：`git diff`、`git log` 等命令在内容多时会进入**翻页模式**，看起来像"卡住了"。其实没卡——
> - 按 `q` 退出
> - 方向键 / 空格翻页

---

### 第 4 步：加入暂存区

```bash
git add .
```

`.` 表示当前目录所有文件。再 `git status` 看，文件会变绿（已暂存）。

> 💡 可选操作：如果不想把 `.zip` 等二进制文件放进 Git，可在项目根目录新建 `.gitignore` 文件，写入 `*.zip`，这样 `git add .` 时会自动忽略它们。

---

### 第 5 步：提交

```bash
git commit -m "Initial commit"
```

`-m` 后是提交说明，首次提交一般写 `Initial commit`。

---

### 第 6 步：关联远程仓库

```bash
git remote add origin https://github.com/416928796/my-skills.git
```

`origin` 是远程仓库的默认昵称。验证是否绑定成功：

```bash
git remote -v
```

应看到两行 `origin ... (fetch)` 和 `origin ... (push)`。

---

### 第 7 步：推送到 GitHub

```bash
git push -u origin main
```

参数解释：
- `push` = 推送（上传）
- `-u origin main` = 把本地 `main` 和远程 `origin/main` 关联
- 加了 `-u` 后，**以后只需 `git push`**，不用写全

首次推送可能弹出 GitHub 登录认证窗口，按提示授权即可。

---

## 三、常见问题：推送被拒绝（rejected）

### 报错现象

```
! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/416928796/my-skills.git'
hint: Updates were rejected because the remote contains work that you do not have locally.
```

### 原因

GitHub 远程仓库已有内容（通常是因为建仓库时勾选了 "Add a README"），本地没有这些内容，直接推送会被拒绝。

---

### ✅ 方案一：合并远程内容后再推送（推荐）

```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

参数解释：
- `--allow-unrelated-histories` = 本地和远程是两个互不相干的历史，必须加此参数才允许合并

#### 可能的小插曲：弹出编辑器让你写合并信息

执行 pull 后可能自动打开编辑器，顶部写着类似：

```
Merge branch 'main' of https://github.com/416928796/my-skills
```

直接保存退出即可，**不用修改**：

| 编辑器 | 退出方式 |
|--------|----------|
| nano | `Ctrl+O` 回车保存 → `Ctrl+X` 退出 |
| vim  | 按 `Esc` → 输入 `:wq` → 回车 |

> 如果改乱了别慌：按 `Esc` 输入 `:q!` 回车强制不保存退出，重新执行 pull 命令。

---

### 备选：合并时出现冲突（CONFLICT）

若本地和远程有同名文件内容不同，会报冲突：

```
CONFLICT (add/add): Merge conflict in xxx
Automatic merge failed; fix conflicts and then commit the result.
```

**最简单的处理**：

保留本地版本（覆盖远程）：

```bash
git checkout --ours .
git add .
git commit -m "合并远程，保留本地版本"
git push -u origin main
```

或保留远程版本（覆盖本地）：

```bash
git checkout --theirs .
git add .
git commit -m "合并远程，使用远程版本"
git push -u origin main
```

> 一般本地是主力内容，选 `--ours` 即可。**没看到 CONFLICT 字样就跳过这步**。

---

### 🔧 方案二：强制覆盖远程（备选，简单粗暴）

如果不在乎远程的初始 README，想让远程完全变成本地样子：

```bash
git push -u origin main --force
```

> ⚠️ 警告：`--force` 会**永久删除**远程现有的提交历史。
> - 新仓库、远程只有初始 README：用 `--force` 问题不大
> - **多人协作的项目千万别用**，会把别人的提交冲掉

---

## 四、日常使用的三件套（记住这个循环）

以后每次修改完文件，都是这三步：

```bash
git add .                          # 1. 加入暂存区
git commit -m "说明这次改了啥"      # 2. 提交
git push                           # 3. 推送到 GitHub（因之前 -u 过，不用写全）
```

---

## 五、关键命令速查表

| 命令 | 作用 |
|------|------|
| `git init` | 初始化本地仓库 |
| `git branch -M main` | 重命名当前分支为 main |
| `git status` | 查看文件状态 |
| `git add .` | 把所有文件加入暂存区 |
| `git commit -m "信息"` | 提交到本地仓库 |
| `git remote add origin <地址>` | 关联远程仓库 |
| `git remote -v` | 查看已绑定的远程仓库 |
| `git push -u origin main` | 推送并关联上游分支 |
| `git push` | 推送（已关联上游后简写） |
| `git pull origin main --allow-unrelated-histories` | 拉取并合并不相干的历史 |
| `git push --force` | 强制推送（覆盖远程历史，慎用） |

---

## 六、翻页模式小贴士

`git diff`、`git log` 等命令输出多时会进入翻页模式：

- **退出**：按 `q`
- **翻页**：方向键 或 空格
- 不是卡住，别紧张
