# cqhttp-qqimagedeliver
[qqimagedeliver](https://github.com/tkkcc/qqimagedeliver)的go-cqhttp+node实现

## 说明

[qqimagedeliver](https://github.com/tkkcc/qqimagedeliver)的go-cqhttp+node实现实现，使用go-cqhttp 的扫码登录特性，简化登录难度

## 快速部署

### 安装需要的软件

安装[go-cqhttp](https://docs.go-cqhttp.org/guide/quick_start.html)
请将配置文件中你的http地址填入config.json中
然后进入文件夹运行以安装依赖

```shell
npm install express axios
```

### 启动

建议先使用`screen`等软件将程序挂起

```
node app
```

## 检查运行状态

**部分服务器需要主动放行端口**

访问 `http://你的IP:49875/status` ，此时应显示

```
通知服务启动成功

```

说明通知服务已经部署好了，可以在速通填写 `你的IP:49875` 接收来自速通的通知

### 参考

- [mirai-qqimagedeliver](https://github.com/DazeCake/mirai-qqimagedeliver)
