# 从服务端仓库迁移 GM

本次是源码与发布边界迁移。现有 GM 进程、接口路径、配置格式和数据格式保持兼容；
清理服务端 Git 仓库不会自动停止正在运行的 GM。

1. 记录旧 GM 镜像/二进制摘要、实际配置路径、端口、运行用户、网络和挂载目录。
   备份配置、GM 状态目录以及注册库和游戏库；不要把备份或凭据提交 Git。
2. 从新仓库构建或下载 GM。沿用原数据库映射、PVF SHA256、管理密码和 gameToken。
   用 `--check` 核对配置格式；该命令不证明数据库/API 连通。
3. 保留原政策表、注册额度快照、批次、规则 ID、账号/邮件回执与角色创建时间。
   不清空表、不新建同内容规则替代旧规则、不恢复旧数据库覆盖玩家进度。
4. 如果旧 GM 由游戏的 Compose 项目管理，先准备新 GM 专用项目并核对端口和网络；
   在切换时只停止旧 GM，再启动新 GM。旧私有 bridge 网络可作为 external network
   继续使用，或采用本仓 Linux host 网络模板并按真实地址调整。不要启动两个争用
   相同端口的实例，也不要对旧游戏项目运行 `down` 或 `--remove-orphans`。
5. GM 已迁出后，才从游戏 instance.json 移除 `gm_*` 设置；保留
   `player_admin_secret`，其值必须与 GM `gameToken` 一致。
   Windows 旧 `server.gmListen` 也需移除。新版游戏生成器会在写入前拒绝未迁移配置。
6. 验证 GM 登录、状态、物品查询、规则列表、预览和只读在线/API 查询；迁移验证
   不向真实玩家发奖。已有启用规则会继续正常扫描。记录实际运行镜像/二进制摘要。

需要回退时只恢复旧 GM 二进制/镜像和匹配配置，继续使用当前数据库与发放回执。
现有管理 Hub 可以继续代理同一 GM 地址，外层 token 和记住登录机制无需重置。

The migration preserves existing data and receipts. Repository cleanup is not
a deployment. Cut over only GM, retain current databases, and never recreate
campaigns as a substitute for migrating their original IDs and history.
