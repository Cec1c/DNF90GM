<div align="center">

# DNF90GM

![Go](https://img.shields.io/badge/Go-1.26.5-00ADD8?style=flat-square&logo=go&logoColor=white)
![数据库](https://img.shields.io/badge/Database-MariaDB-003545?style=flat-square&logo=mariadb)
![平台](https://img.shields.io/badge/Platforms-Windows%20%7C%20Linux-2563EB?style=flat-square)

面向 ServerS5A3 90CN 的独立 Web GM：管理账号角色、查询 PVF 物品，通过邮件发放可重复补发且自动去重的福利。

[English](README.md) ｜ [快速开始](#快速开始) ｜ [部署说明](docs/DEPLOYMENT.md) ｜ [旧版迁移](docs/MIGRATION.md)

</div>

> [!IMPORTANT]
> 需要兼容的 ServerS5A3 MariaDB 表结构、匹配的 PVF 和游戏私有管理 API v1。仓库不包含游戏素材、玩家数据库或部署凭据。适用版本见[兼容契约](docs/COMPATIBILITY.md)。

## 能做什么

- 浏览器登录、查询账号角色、搜索 PVF 物品和使用既有 GM 管理操作。
- 按物品 ID、数量发送邮件，邮件和持久回执在同一资产事务中提交。
- 预览并补发现有角色，启用/暂停福利规则，自动覆盖符合条件的新角色。
- 复用原规则跳过已发角色；重启、领取或删除邮件后仍保留去重记录。
- 通过鉴权的游戏私有接口查询在线状态、读取和修改活动配置。

当前**每条福利规则包含一种物品**。多个物品可建立多条规则，各发一封邮件。
新建规则表示新一轮奖励，不共享旧规则的发放记录。详见[福利规则说明](docs/BENEFITS.md)。

## 快速开始

安装 Go 1.26.5 和 Python 3.10+：

```sh
git clone https://github.com/Cec1c/DNF90GM.git
cd DNF90GM
python scripts/build.py windows amd64
```

Linux 使用 `python3 scripts/build.py linux amd64`。将 `config/gm.example.json`
复制为 `runtime/gm.json`，填写原数据库映射、PVF SHA256、游戏私有接口密钥及独立管理密码。
提前建立可写的状态目录。

```text
dist/windows-amd64/DNF90GM.exe --config runtime/gm.json --check
dist/windows-amd64/DNF90GM.exe --config runtime/gm.json --init-schema
```

在 GM 主机打开 `http://127.0.0.1:18112/`。Linux 程序路径为
`./dist/linux-amd64/DNF90GM`。`--check` 只检查配置格式；`--init-schema`
初始化 GM 附加表后启动服务。创建和启用奖励规则仍需管理员操作，已有启用规则会恢复扫描。

Windows 也可使用 `BUILD.bat`、`START_GM.bat`。[部署说明](docs/DEPLOYMENT.md)
包含二进制运行、Linux Docker、私有访问方式和各配置字段。

## 独立边界

GM 自己管理 HTTP、鉴权、PVF 索引、批量任务和扫描。游戏负责登录、创建角色、玩法与领取邮件。
GM 通过既有 MariaDB 资产事务访问数据，通过游戏私有接口获取运行时状态。

本仓使用独立 Go module，并保留明确版本的业务/仓储兼容代码，构建无需服务端源码目录或相对路径依赖。
登录器管理 Hub 及其记住 token 功能属于可选外部集成。
已有服务迁移时，按[迁移说明](docs/MIGRATION.md)保留规则 ID、注册额度快照与全部发放回执。

## 开发验证

```sh
python scripts/check_boundary.py
go test -buildvcs=false -count=1 ./...
go vet ./...
python scripts/test_mysql.py
```

最后一条会创建并移除一次性 MariaDB Docker 容器。测试 DSN 不得指向玩家数据库。
页面验证先安装 `playwright` 和 Chromium，再执行 `python scripts/test_browser.py`；
请求使用模拟数据，不向真实玩家发奖。`python scripts/package.py v0.1.0` 生成双平台发行包。

## 来源

提取自 [Cec1c/ServerS5A3](https://github.com/Cec1c/ServerS5A3)，源自
[16ww/servers5a3](https://gitgud.io/16ww/servers5a3)。来源路径和摘要见
[PROVENANCE.md](docs/PROVENANCE.md)，署名与许可现状见 [NOTICE.md](NOTICE.md)；
没有为迁入代码擅自指定新的许可证。
