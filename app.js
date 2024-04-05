// node.js 代码，用于处理来自速通的http请求，并将图片发送到go-cqhttp
// 需要安装 express 和 axios 模块
const express = require('express');
const axios = require('axios');

// 引入配置文件
const config = require('./config.json');

// 从配置文件中获取端口号，go-cqhttp的地址，QQ群号
const port = config.port;
const go_cqhttp_url = config.go_cqhttp_url;

// 创建一个 express 应用
const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true, limit: '10mb' }));
app.get('/status', (req, res) => {
    // 返回一个简单的HTML页面
    res.send(`
      <html>
        <head>
          <title>cqhttp-qqimagedeliver Status</title>
        </head>
        <body>
          <h1>通知服务启动成功</h1>
        </body>
      </html>
    `);
});

// 定义一个路由，用于接收来自速通的通知
app.post('', async (req, res) => {
  // 获取请求体中的数据
  const data = req.body;
  // console.log(data);
  // 判断数据是否合法
  if (data && data.image && data.to && data.info) {
    // 获取图片的 base64 编码，接收QQ号或群号，和文字信息
    const image = data.image;
    const to = data.to;
    const info = data.info;
    // 检查 info 是否包含 "每日单抽"
    if (!info.includes("每日单抽")) {
      return res.json({ code: -3, msg: 'invalid data(Not a daily draw)' });
    }
    try {
      // 构造一个 CQ 码，用于发送图片
      const cqcode = `[CQ:image,file=base64://${image}]`;
      // 构造一个消息内容，包含图片和文字信息
      const message = `${cqcode}\n${info}`;

    //别TM判断了，都发得了
    // await axios.post(`${go_cqhttp_url}/send_private_msg`, {
    //     user_id: to,
    //     message,
    // });    
    await axios.post(`${go_cqhttp_url}/send_group_msg`, {
        group_id: to,
        message,
    });
    console.log("发送成功")

      // 返回成功的响应
      res.json({ code: 0, msg: 'success' });
    } catch (error) {
      // 返回失败的响应
      res.json({ code: -1, msg: error.message });
    }
  } else {
    // 返回无效数据的响应
    res.json({ code: -2, msg: 'invalid data' });
  }
});

// 启动应用，监听端口号
app.listen(port, '0.0.0.0',() => {
  console.log(`${go_cqhttp_url}`);
  console.log(`App listening at http://localhost:${port}`);
});