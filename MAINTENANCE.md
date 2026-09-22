# 维护说明（改首页的速查表）

这个仓库只有一个使命：**它就是你的 GitHub 首页**。
GitHub 会把「仓库名和用户名完全相同的公开仓库」里的 `README.md` 渲染到 `https://github.com/junfennie162-sketch` 的最上方。

---

## 一、文件都是干什么的

```
README.md                      首页正文（你平时改的就是这个）
preview.html                   本地预览素材：浏览器直接打开即可，不用推 GitHub
assets/                        首页用的 SVG 素材（全部由脚本生成，别手改）
  banner-light.svg / banner-dark.svg        顶部头图
  terminal-light.svg / terminal-dark.svg    终端面板
  langcard-light.svg / langcard-dark.svg    语言构成卡（脚本会联网拉真实字节数）
  status-*-light.svg / status-*-dark.svg    状态徽标（在做/已完成/在学）
scripts/make_assets.py         生成上面这些 SVG 的脚本（改文字/配色就改这里）
.github/workflows/snake.yml    每天自动更新贡献图贪吃蛇（推到 output 分支）
```

---

## 二、常见的四件事

### 1. 改头图上的名字、标语、小标签、配色

打开 `scripts/make_assets.py`：

- **名字 / 标语 / 标签 / 雷达下方文字**：在文件底部 `main()` 里的 `banner(...)` 调用处改；
- **配色**：改顶部 `THEMES` 字典对应的色值（亮暗两套，键名一一对应）；
- **终端面板里的文字**：同一函数下面的 `terminal(...)` 调用，`lines` 列表里每行是 `(类型, 文本)`：
  `cmd` = 命令行、`out` = 普通输出、`hl` = 高亮行、`comment` = 灰注释。

改完重跑（任何 Python 3.9+ 都行）：

```powershell
python scripts/make_assets.py
```

然后刷新 `preview.html` 看一眼，满意就提交：

```powershell
git add -A; git commit -m "更新首页素材"; git push
```

### 2. 改自我介绍、项目卡、技术栈

直接编辑 `README.md`。两条规矩：

- **只写能被仓库证明的东西**（测试数量、跑分、延迟这类），别写「精通」；数字变了就顺手改；
- 亮暗两套图用 `<picture>` 包着，加新图时照抄现有写法：

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/xxx-dark.svg" />
  <img src="./assets/xxx-light.svg" alt="说明" width="100%" />
</picture>
```

### 3. 补资料页字段（名字 / 简介 / 位置 / 网站）

首页左上角的简介来自**个人资料**，不在本仓库里。改简介要用带 `user` 权限的令牌，
当前登录的令牌只有 `gist / read:org / repo`，所以先补权限（会弹一次浏览器授权，一次性）：

```powershell
gh auth refresh -h github.com -s user
```

然后：

```powershell
gh api -X PATCH user -f bio="LLM 应用工程 · RAG / Agent / 安全工具链"
```

位置、网站同理（`-f location="太原"`、`-f blog="https://..."`）。
改完打开 https://github.com/junfennie162-sketch 刷新就能看到。

> 不想动令牌也行：网页 https://github.com/settings/profile 里手填，效果一样。

### 4. 置顶仓库（这个 API 改不了，只能网页点）

GitHub 的置顶**没有开放 API**，需要手动：打开 https://github.com/junfennie162-sketch
→ 右侧 `Pinned` 区域右上角 **Customize your pins** → 勾选 6 个仓库 → Save。
建议顺序（把最能打的两三个放最前面）：

1. `textbook-exercise-rag`（主力项目，工程完整度最高）
2. `birensupa-spectralconv`（竞赛 + 有硬数字）
3. `corehacker`
4. `phish`
5. `pentest-ai-knowledge`
6. `AIxVuln`

---

## 三、外部依赖坏了怎么办

首页里有三类**外部图片服务**，都属于「免费公共实例」，偶尔会抽风：

| 用途 | 出处 | 挂了怎么办 |
|---|---|---|
| 技术栈小徽标 | `img.shields.io` | 极少挂；真挂了就删掉对应 `<img>` |
| 社交图标 | `cdn.simpleicons.org` | 同上 |
| 贪吃蛇 | `raw.githubusercontent.com/.../output/...` | 看仓库 Actions 里 `snake.yml` 那次运行为什么失败 |

> 头图、终端面板、语言构成卡、状态徽标都是**本地 SVG**，不依赖任何外部服务，永远都能显示。
> 语言构成卡里的数字是生成脚本当时拉到的真实字节数（卡上标了日期），
> 语言占比变化后重跑 `python scripts/make_assets.py` 就会更新。

---

## 四、贪吃蛇不想用了

删掉 README 里 `📊 GitHub 概览` 最后那个 `<picture>` 块，再删 `.github/workflows/snake.yml`，
最后把 `output` 分支删掉即可（不影响其他任何东西）。
