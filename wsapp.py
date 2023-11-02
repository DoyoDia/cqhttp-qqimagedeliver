# Python 代码，用于处理来自速通的http请求，并将图片发送到go-cqhttp
# 需要安装 flask requests  websocket-client 模块
from flask import Flask, request, jsonify
import websocket
import json
import uuid

# 读取配置文件
with open('config.json', 'r') as f:
    config = json.load(f)
#TODO:自动获取蓝蝶ADB端口并开启adb forward
#TODO:QQ重启后自动重建WS连接

# 从配置文件中获取本地监听端口和go-cqhttp的地址
port = config['port']
go_cqhttp_url = config['go_cqhttp_wsurl']


# 创建一个 Flask 应用
app = Flask(__name__)

# 创建一个 WebSocket 连接
ws = websocket.create_connection(f"{go_cqhttp_url}")

@app.route('/status', methods=['GET'])
def status():
    return """
      <html>
        <head>
          <title>1999-qqimagedeliver Status</title>
        </head>
        <body>
          <h1>通知服务启动成功</h1>
        </body>
      </html>
    """

# 定义一个路由，用于接收来自速通的通知
@app.route('/', methods=['POST'])
def handle_notification():
    data = request.json
    #if data and 'to' in data and 'info' in data and data['token'] == 'your_token_here':
    if data and 'to' in data and 'info' in data:
        to = data['to']
        info = data['info']
        if "每日单抽" not in info:
            return jsonify({"status": "ok"}), 200
        try:
            if 'image' in data:
                image = data['image']
                params = {
                    "message_type": 'group',
                    "group_id": to,
                    "message": f"[CQ:image,file=base64://{image}\n{info}]",
                }
            else:
                params = {
                    "message_type": 'group',
                    "group_id": to,
                    "message": f"{info}",
                }
            requestId = str(uuid.uuid4())
            json_data = {
                "action": 'send_msg',
                "params": params,
                "echo": requestId,
            }
            ws.send(json.dumps(json_data))
            while True:
                result = ws.recv()
                result_data = json.loads(result)
                if result_data['echo'] == requestId:
                    if result_data['status'] == "ok":
                        return jsonify({"status": "ok"}), 200
                    else:
                        return jsonify({"error": result_data}), 500
        except Exception as e:
            print(e)
            return jsonify({"error": "Internal Server Error"}), 500
    else:
        print(f"{data}")
        return jsonify({"error": "Bad Request"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)