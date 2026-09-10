# Windows 日常使用

首次在仓库运行：`powershell -NoProfile -ExecutionPolicy Bypass -File tools\windows\create_desktop_shortcuts.ps1`。无需管理员权限。

- **每天看论文**：双击桌面「Daily Paper Reader - 今日论文」。
- **修改研究方向**：双击「Daily Paper Reader」→ [2] 打开后台管理 → 修改并保存。
- **保存后运行**：菜单 [3] 保存配置并运行论文检索。常规备份、同步、提交、推送自动完成。
- **查看运行结果**：菜单 [4]。没有安装或登录 GitHub CLI 时，配置仍会同步，请在打开的页面点击 **Run workflow**。
- **更新项目**：菜单 [5] 先检查 upstream，确认后合并；冲突停止并保留版本。上游代码更新不会自动推送，需审阅。
- **检查环境**：菜单 [6] 查看分支、远端更新、后台与 gh 状态。

现有 GitHub Actions 每日调度保留：北京时间 02:30 开始，现有随机延迟最多约一小时；实际排队可能更晚。平时直接看 GitHub Pages 即可。

运行默认参数在 `user_settings.json`：默认 30 天、standard、全部词条；profile_tag 可填写现有词条的 tag。参数仅用于手动运行，不修改定时调度。不要在此文件放密钥。

后台仅安装管理依赖；若在网页中触发本地检索，仍需要原项目完整依赖。正常检索请使用菜单 [3]。后台日志在 `logs/local_admin.log`，关闭菜单不会关闭后台。重复启动直接复用同仓库后台。

同步要求处于 main，且没有其它代码改动/暂存内容。配置和本地 docs/archive 改动保存在 `.local_backup/时间戳/`，生成结果以远端为准。配置双方发生无法合并的冲突、其它代码修改、未完成合并、Git 登录失效或分支保护可能需要人工处理。失败不会强推；保留备份与提交后可重试。

安全：不要提交 `.env`，不要公开 DeepSeek API Key 或 GitHub Token。`secret.private` 是现有加密配置文件，仅校验加密结构后显式提交；请使用可靠密码。不要使用 `git add .`、`git push -f`。备份和日志只保留本地。
