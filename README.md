# Open Agent Systems website

组织官网：<https://open-agent-systems.github.io>

此站点介绍组织宗旨、建设方向、共建原则与参与方式。项目内容待正式开源后再建设。

## 维护

- `content/en.json`：英文内容，默认首页。
- `content/zh-CN.json`：简体中文内容，访问路径 `/zh/`。
- `scripts/build.py`：使用 Python 3 标准库生成各语言页面、站点地图与 404。
- `docs/assets/`：样式与品牌图片，无第三方字体或运行依赖。
- `docs/`：生成后的发布文件；GitHub Pages 从 `main` 分支的 `/docs` 发布。

修改内容或模板后运行：

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8080 --directory docs
```

设计改动先在 `design/*` 分支完成，发布独立预览供对比，确认采用后才合入 `main` 并发布。版本、预览与回退流程见 [RELEASING.md](RELEASING.md)。不需要手动操作服务器。

新增语言时复制一个内容 JSON，修改 `lang`、`name`、`path` 并完整翻译字段。构建脚本自动增加页面、语言导航及站点地图。项目名和 GitHub 地址保持一致，建设方向与已交付能力应明确区分。

Git 提交遵循维护者的 GitHub 专用邮箱配置。不写入凭据、私有设计资料或本机运行数据。

## 目标架构图

官网架构图是组织的生态目标视图，不是某个产品的部署结构，也不代表相关能力已交付。内容由各语言 JSON 的 `layers` 与 `architecture*` 字段维护。

网页图可点击能力图形或标题查看职责、输入输出与协作关系；选中能力后突出相关路径，其余能力淡出。场景导航支持逐步探索。`scripts/architecture.py` 在构建时同步导出中英文 SVG，可下载用于组织介绍。`scripts/scene.py` 统一维护两块图示的能力形态、坐标与基础连接；`docs/assets/landscape.css` 负责呈现。架构调整后同步检查网页图和 SVG 的标签、关系及规划说明。

## 生态探索与组织愿景

首页节点图用于解释目标生态，不显示或模拟实时运行数据。节点内容与场景标题由 `ecosystemView` 维护；愿景由 `vision*` 字段维护；建设方向选项由 `steps` 维护。交互逻辑位于 `docs/assets/site.js`，均使用原生按钮，支持键盘操作；连线动画遵循系统减少动态效果设置。
