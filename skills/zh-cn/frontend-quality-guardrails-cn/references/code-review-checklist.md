# 前端代码审查清单

编辑或审查项目 UI 代码前使用本参考。保持修改外科手术式：指出具体缺陷，只修当前受影响界面，保留现有模式。

## 目录

- 审查顺序
- React 和 Next.js
- Vue 和 Nuxt
- Svelte
- HTML 和 CSS
- 数据和内容
- 表单
- 表格和高密度数据
- 组件库
- 状态和交互
- 性能风险
- 审查输出格式

## 审查顺序

1. 明确被修改的用户可见界面。
2. 找到组件边界、wrapper、设计系统组件、数据结构和 CSS 来源。
3. 追踪每个动态文本值进入 DOM 的路径。
4. 从父到子检查布局约束，特别是 flex/grid 容器。
5. 检查关键状态：loading、empty、error、disabled、readonly、focus、hover、selected、expanded、collapsed、权限受限。
6. 可行时用极端文本和至少一个窄屏视口验证。

## React 和 Next.js

- 检查 flex/grid 内含文本子项是否在正确层级有 `min-w-0`、`flex-1`、`shrink-0` 或等价写法。
- 截断应放在文本节点上，不要放在同时包含按钮或 badge 的高层 row 上。
- 避免条件渲染插入/移除 wrapper 导致布局不稳定；loading/error 状态尽量复用稳定槽位。
- 可重排、可筛选、动态列表不要使用数组 index 作为 key。
- Next.js 中不要为了样式把组件无谓变成 client component。
- 避免浏览器专属值、日期、随机 ID、视口依赖渲染导致 hydration mismatch。
- 截断时保持 `aria-label`、`title`、tooltip 和可见标签一致。
- 简单派生显示值不要用 `useEffect`。
- memoization 要局部且有理由，不要用 `useMemo`/`useCallback` 掩盖结构问题。
- Suspense、skeleton、loading 状态应保持最终布局尺寸。

## Vue 和 Nuxt

- 检查 `v-if`/`v-show` 选择：`v-if` 会移除布局和焦点目标，`v-show` 保留 DOM 和尺寸。
- 校验 `v-for` 的 `:key` 稳定性。
- 多处依赖的展示字符串放在 `computed`，不要反复写复杂模板表达式。
- scoped CSS 不要依赖脆弱 deep selector，除非组件库没有公开 API。
- 检查 slot 长内容；父组件必须约束 slot 布局。
- 翻译标签和校验文本外层避免固定高度。
- Nuxt 中检查 SSR/client-only 逻辑是否造成布局位移。

## Svelte

- 动态列表 `{#each}` 使用稳定 key。
- reactive declaration 不要无谓重复计算昂贵布局数据。
- 条件块不要替换焦点元素导致焦点丢失。
- 检查 slotted content 约束，特别是卡片头、表格单元格和工具栏操作。

## HTML 和 CSS

- 语义和行为匹配：action 用 `button`，导航用 `a`，字段用 `label`，表格数据用 `table`。
- 不要用 `position: absolute` 修正常文档流，除非 UI 本身就是覆盖层。
- 加 `z-index` 前先检查 stacking context，常见来源包括 transform、opacity、filter 和 positioned ancestor。
- `overflow: hidden` 不应裁剪 focus ring、dropdown、sticky 子项或校验消息。
- 文本密集容器避免固定 `height`，优先 `min-height`、自然流或内部滚动。
- 全局 CSS 修改必须有作用域，不能影响无关组件。
- 只有可打印界面才检查 print styles。

## 数据和内容

- 后端内容默认长度和格式都不可信。
- empty/null/undefined 不应渲染成 `undefined`、`null`、`NaN` 或破碎标点。
- 可选字段拼接要避免多余分隔符。
- 数字、日期、货币和百分比使用项目现有格式化工具。
- 重要的原始 ID、URL、hash、文件路径要可复制。
- 只有日志/代码/预格式文本才保留空白，普通标签不要保留。

## 表单

- 每个输入都有可见或可访问 label。
- 校验消息靠近字段且可换行。
- checkbox、radio、switch、select option、segmented control 的长标签要能处理。
- 保留 autocomplete、input type、required、disabled、readonly、invalid 等浏览器语义。
- 不要禁用提交按钮却不解释阻塞原因。
- 异步提交状态要防止重复提交且不改变布局。
- API 返回的错误不能撑破 toast、dialog 或 form 容器。

## 表格和高密度数据

- 每列明确 wrap、truncate、fixed、flexible、sticky 或小屏隐藏策略。
- 横向滚动放在 table wrapper 上，不放整页。
- 窄屏下行操作仍要可触达。
- scroll、sticky 或虚拟列表后表头和单元格仍要对齐。
- 如果单元格可换行，检查虚拟列表是否支持可变行高。
- empty/filter/no-permission 状态保持表格外框一致。
- 不要隐藏决策必需列，除非有详情行或钻取路径。

## 组件库

- 优先使用项目 wrapper 组件，再考虑原始库组件。
- 读取附近现有用法，匹配尺寸、密度、variant、语气和位置。
- 使用文档化 props 控制 ellipsis、tooltip、placement、popup container、scroll、虚拟列表和 status。
- 除非没有公开 API，不要覆盖生成类名或内部结构。
- 检查 dropdown、popover、modal、select、date picker 的 portal 容器。
- 确认抽屉/弹窗内浮层不会出现在父级背后或被错误裁剪。

## 状态和交互

- 每个点击目标都要检查键盘交互。
- hover-only 操作也要能被键盘和触摸用户发现。
- 乐观 UI 要可回滚或明确处于 pending。
- dialog 关闭、筛选应用、tab 切换、行展开、异步操作完成后要保留合理焦点。
- 展开详情、排序、筛选或出现校验消息时避免布局位移。
- 危险操作使用项目确认模式。

## 性能风险

- 大列表不要无分页、无虚拟列表、无懒加载直接渲染。
- 不要在 render 循环中反复测量布局。
- 大数据搜索/筛选输入要 debounce。
- 检查图片尺寸、懒加载和 object fit。
- 不要为一个小图标或小图表引入大型图标包/图表库。
- 重复元素动画不要动画 `width`、`height`、`top`、`left` 或昂贵 filter。

## 审查输出格式

审查时先列缺陷：

- 严重程度和简短标题。
- 文件和行号。
- 说明在真实内容或视口下为什么会坏。
- 最小修复方向。
- 最后说明缺失的验证或测试风险。
