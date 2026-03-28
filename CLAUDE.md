# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**MoodMusicUI**（音信）是一个完全在单个 HTML 文件中构建的单页音乐流媒体应用。面向中文用户，主打自然声景、环境音乐和治愈音频的冥想式音乐体验。

## 运行方式

无需构建。直接在浏览器中打开 `index.html`，或用任意静态文件服务器：

```bash
python -m http.server 8000    # Python 方式
npx http-server                # Node.js 方式
```

Dockerfile 通过 nginx 部署（端口 80）。GitHub Actions 工作流（`.github/workflows/deploy.yml`）在每次推送到 `main` 分支时自动构建并推送 Docker 镜像到 GHCR。

## 架构

### 单体结构

整个应用都在 `index.html` 中（约 921 行），这是有意为之的设计，方便部署和分享：

- **Tailwind 配置 + 自定义 CSS**（第 16-85 行）
- **内联 JavaScript**（第 103-919 行）：所有 React 组件和逻辑，由 Babel Standalone 在浏览器中实时转换（无需构建）

### 关键模式

- **用 `class` 而非 `className`**：所有 React 组件使用 `class` 属性，因为 Babel Standalone 会处理转换
- **浏览器内 JSX**：Babel Standalone 在运行时转换 `<script type="text/babel">`，无需编译步骤
- **PlayStateContext**（第 109 行）：React Context，管理全局播放/暂停状态，在 MiniPlayer、PlayerPage 等组件间共享。通过 `usePlayState()` hook 访问。
- **MemoryRouter**：React Router v6.3.0，使用 `MemoryRouter`（不操作浏览器历史）。路由：`/`、`/discover`、`/profile`、`/artist`、`/album`、`/player`
- **Material Icons**：使用 `<span class="material-symbols-outlined">`，填充图标需加 `style={{fontVariationSettings: "'FILL' 1"}}`

### 外部依赖（全部 CDN，无 npm）

- React 18、React Router DOM 6.3.0、Babel Standalone 6
- Tailwind CSS（通过 CDN 脚本加载）
- Google Fonts：Noto Serif SC（标题）、Manrope（正文）
- **Supabase**：评论后端（匿名、按页面路径隔离）—— anon key 故意暴露在前端
- **外部 API**：`m-api.changgepd.top/api/skeleton`，获取音乐人数据

### 组件分布

**共享组件**（第 167-361 行）：
- `TopAppBar`（167）：导航栏，支持返回按钮
- `MiniPlayer`（188）：底部固定迷你播放条
- `BottomNav`（222）：底部标签导航（首页、发现、我的）
- `CommentButton`（251）：浮动按钮，点击展开评论面板

**页面组件**（第 363-899 行）：
- `HomePage`（363）：首页，展示精选内容
- `DiscoverPage`（474）：发现页，音乐人分类筛选
- `ProfilePage`（574）：个人页，收藏的专辑和关注的音乐人
- `ArtistPage`（648）：音乐人详情和作品列表
- `AlbumDetailPage`（726）：专辑曲目列表
- `PlayerPage`（796）：全屏播放器，带歌词滚动动画
- `App`（901）：根组件，包含路由配置

### 静态资源

所有图片都本地化存放在 `assets/` 目录（头像、专辑封面、音乐人照片、文章配图）。评论头像从 `DEFAULT_ARTIST_AVATARS` 数组中随机选取，使用本地资源路径。

## 设计系统

自定义大地色系 Tailwind 主题（第 17-64 行）：
- 主色绿色：`#34614d`、`#4c7965`
- 辅色棕色：`#8f4122`、`#ae5838`
- 表面色阶：从 `surface-container-lowest` 到 `surface-container-highest`
- 圆角规范：`0.125rem`（默认）→ `0.25rem`（lg）→ `0.75rem`（xl）→ `9999px`（full）
- 毛玻璃效果：`.glass-player` 类，使用 `backdrop-filter: blur(24px)`
- 移动端优先响应式设计，使用 `md:` 断点

## 已知局限

- 没有实际音频播放功能——MiniPlayer 和 PlayerPage 只是 UI 模拟
- DiscoverPage 的搜索框是装饰性的（未实现功能）
- 没有离线支持、PWA 或 Service Worker
- 没有测试
