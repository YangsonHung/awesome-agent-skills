# 浏览器验证流程

完成可见前端修改后，或调试溢出、响应式、视觉回归、交互状态时使用本参考。

## 目录

- 何时需要浏览器验证
- 启动
- 视口
- 极端内容
- 截图检查
- DOM 和控制台检查
- 交互检查
- 有用的自动断言
- 验证报告

## 何时需要浏览器验证

以下修改需要浏览器验证：

- 布局、间距、字体、颜色、边框、阴影或响应式行为。
- 文本渲染、截断、换行、表格、卡片、表单、导航或弹窗。
- dropdown、tooltip、popover、drawer、dialog、sticky 元素或 portal。
- loading、error、empty、disabled、hover、focus、selected、expanded、collapsed 状态。
- canvas、SVG、图表、图片、视频、地图或动画。

## 启动

1. 使用项目现有包管理器和 dev script 启动项目。
2. 优先使用仓库文档里的本地 URL。端口占用时，只有框架支持才换下一个端口。
3. 用内置浏览器或可用浏览器自动化工具打开页面。
4. 观察终端输出、浏览器控制台和网络错误。
5. 验证完成后，不需要继续使用时再停止 dev server。

## 视口

按实际尺寸检查被修改界面：

- `320x700`：最小常见移动端压力场景。
- `375x812`：常见移动端。
- `768x1024`：平板。
- `1024x768`：小桌面或平板横屏。
- `1280x800`：常见笔记本。
- `1440x900` 或更宽：桌面间距。

非常小的修改可以减少视口，但布局类修改至少包含一个窄屏和一个桌面视口。

## 极端内容

可行时注入或创建测试数据：

- 超长无空格 token。
- 长自然语言句子。
- 带 query string 的 URL。
- 中英文混排。
- 超长翻译按钮/标签。
- 很多 tag/badge。
- 空值。
- 缺失图片/头像。
- 长校验错误。
- 大量表格行或列表项。

无法安全改真实数据时，使用 devtools DOM 编辑、本地 mock、storybook stories、fixtures 或临时测试数据。结束前移除临时数据。

## 截图检查

对每个重要视口：

1. 截取被修改界面的截图。
2. 检查横向溢出、文本裁剪、重叠、异常滚动条、布局位移和对齐问题。
3. 如果修改影响交互，比较关键状态。
4. 关注标题、标签、值、按钮和错误信息是否无需猜测即可阅读。

重点看：

- 页面边缘是否有内容超出视口。
- 包含标题、元信息和操作的 flex 行。
- 表格 wrapper 和 sticky 列。
- 弹窗 header/footer 和 body 滚动。
- dropdown/popover 是否贴近视口边缘后错位。
- 图标旁文字的基线。
- loading skeleton 尺寸和最终内容是否一致。

## DOM 和控制台检查

截图不明确时检查 DOM：

- 查看 computed width、`min-width`、`overflow`、`white-space`、`text-overflow`、`word-break`、`overflow-wrap`。
- 判断是溢出节点还是父级需要 `min-width: 0`。
- 浮层异常时检查 portal root 和 z-index。
- 检查纯图标控件的 accessible name。
- 检查 console error/warning。
- 检查网络失败是否导致损坏的 loading/error 状态。

## 交互检查

执行真实流程：

- 输入长文本。
- 触发表单校验错误。
- 打开和关闭 dropdown、popover、drawer、modal。
- hover 和键盘 focus 控件。
- 切换 tab 和 filter。
- 排序并滚动表格。
- 在组件打开时调整视口。
- 在 loading 和 error 场景提交表单。

## 有用的自动断言

Playwright 或类似工具中优先使用简单断言：

- 断言文档级没有横向溢出：
  `document.documentElement.scrollWidth <= document.documentElement.clientWidth`
- 断言目标文本容器尺寸没有超出父容器。
- 断言关键控件按预期可见、启用或禁用。
- 项目已有视觉回归设施时，为关键响应式界面加截图断言。

除非项目已有视觉回归基础设施，否则不要写脆弱的像素级测试。

## 验证报告

最终回复说明：

- 检查过的视口。
- 检查过的主要状态。
- 是否发现相关浏览器/控制台错误。
- 未验证的状态或视口，以及原因。

只做代码检查时，不要声称已经完成视觉验证。
