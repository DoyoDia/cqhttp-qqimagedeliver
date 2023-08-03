// node.js 代码，用于处理来自速通的http请求，并将图片发送到go-cqhttp
// 需要安装 express、axios 和 ws 模块
const express = require('express');
const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid');
// 引入配置文件
const config = require('./config.json');

// 从配置文件中获取本地监听端口和go-cqhttp的地址
const port = config.pubport;
const go_cqhttp_url = config.go_cqhttp_wsurl;

// 创建一个 express 应用
const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true, limit: '10mb' }));
app.get('/status', (req, res) => {
    // 返回一个简单的HTML页面
    res.send(`
      <html>
        <head>
          <title>1999-qqimagedeliver Status</title>
        </head>
        <body>
          <h1>通知服务启动成功</h1>
        </body>
      </html>
    `);
});

// 创建一个 WebSocket 连接
const ws = new WebSocket(`${go_cqhttp_url}/ws`);



// 定义一个路由，用于接收来自速通的通知
app.post('', async (req, res) => {
  // 获取请求体中的数据
  const data = req.body;
  // 判断数据是否合法
  if (data && data.to && data.info && data.token === 'your_token_here') {
    // 获取图片的 base64 编码，接收QQ号或群号，和文字信息
    const to = data.to;
    const info = data.info;
    try {
      // 构造一个消息内容，包含图片和文字信息
    // 构造一个参数对象，用于发送图片
    let message;
    if (data.image) {
      const image = data.image;
      const params = {
        "message_type": 'private',
        "user_id": to,
        "message": `[CQ:image,file=base64://${image}\n${info}]`,
      };
      message=params;
    } else {
      const params = {
        "message_type": 'private',
        "user_id": to,
        "message": `${info}`,
      };
      message=params;
    }
    // 构造一个 JSON 对象，用于发送 WebSocket 消息
    const requestId = uuidv4();
    const json = {
        "action": 'send_msg',
        "params": message,
        "echo": requestId, // 将请求 ID 添加到请求中
    };

      // 发送 WebSocket 消息
      ws.send(JSON.stringify(json));
      // 等待接收方的响应消息
      const responsePromise = new Promise((resolve, reject) => {
        const responseHandler = (data) => {
          //console.log(`收到 WebSocket 消息: ${data}`);
          const wsdata = JSON.parse(data);
          if (wsdata.echo === requestId) {
            //console.log('echo ok')
            if (wsdata.status === "ok") {
              //console.log('status ok')
              // 发送成功，返回 resolve
              resolve();
            } else {
              // 发送失败，返回 reject
              reject(new Error(data));
            }
            // 取消监听
            ws.off("message", responseHandler);
          }
        };
        // 监听 WebSocket 消息
         ws.on("message", responseHandler);
      });

      // 等待响应 Promise 的结果
      try {
        await Promise.race([
          responsePromise,
          new Promise((resolve, reject) => {
            setTimeout(() => {
              reject(new Error("Response Timeout"));
            }, 5000); // 等待 5 秒钟
          }),
        ]);
        // 发送成功，返回 200
        res.status(200).send("OK");
      } catch (error) {
        // 发送失败，返回 522
        console.error(error);
        res.status(522).send(`{server error: ${error}}`);
      }
    } catch (error) {
      console.error(error);
      // 返回错误响应
      res.status(500).send('Internal Server Error');
    }
  } else {
    // 返回错误响应
    console.log(`{data.image: ${data.image}, data.to: ${data.to}, data.info: ${data.info}, data.token: ${data.token}}`)
    res.status(400).send('Bad Request');
  }
});

// 监听本地端口
app.listen(port, () => {
    console.log(`cqhttp(ws)-qqimagedeliver 服务已启动，监听端口 ${port}`);
});