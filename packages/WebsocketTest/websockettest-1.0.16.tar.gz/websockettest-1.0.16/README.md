# WebSocket 接口自动化测试工具 (WebSocketTest)

#### 介绍

这是一个基于 WebSocket 协议的接口自动化测试工具。它可以用于自动化测试 WebSocket 接口，确保接口的稳定性和可靠性。

#### 系统要求

**Python 3.10+**：确保你的系统上已经安装了 Python 3.10（推荐使用最新稳定版）。


#### 安装步骤

**1.安装 Python：**
确保你的系统上已经安装了 Python 3.10 或更高版本。你可以从 [Python 官方网站 ](https://www.python.org/downloads/?spm=5176.28103460.0.0.40f75d27PnqPkU)下载并安装。
**2.安装 WebSocketTest 工具：**

```
pip install WebsocketTest
```

**3.安装allure 工具：**
```
install-allure
```
**4.创建测试项目：**
```
ws startproject yourtestProject
cd yourtestProject
```

**5.运行测试：**
  在命令行中运行以下命令：

```
 
<!-- 安徽5.0链路aqua测试： -->
ws test --env uat --app 0f0826ab  --service aqua --project vwa
ws test --env live --app 0f0826ab  --service aqua --project vwa
<!-- 安徽5.4链路sds_gateway测试： -->
ws test --env uat --app 3d7d3ea4  --service gateway_5.4 --project vwa
ws test --env live --app 3d7d3ea4  --service gateway_5.4 --project vwa
<!-- 安徽5.0链路sds_gateway测试： -->
ws test --env uat --app 0f0826ab  --service gateway_5.0 --project vwa
ws test --env live --app 0f0826ab  --service gateway_5.0 --project vwa
<!-- 奥迪aqua测试： -->
ws test --env uat --app 576d9f07  --service aqua --project svm
ws test --env live --app 576d9f07  --service aqua --project svm
<!-- 上汽5.0链路sds_gateway测试： -->
ws test --env uat --app 66ba7ded  --service gateway_5.0 --project svw
ws test --env live --app 66ba7ded  --service gateway_5.0 --project svw

<!-- 指定Gatewaycase -->
ws test --env uat --app 3d7d3ea4  --service gateway_5.4 --project vwa --testcase testcase/test_all.py::TestGateway::test[case_suite0]
<!-- 指定Aquacase -->
ws test --env uat --app 0f0826ab  --service aqua --project vwa testcase/test_all.py::TestAqua::test[case_suite0]
```
