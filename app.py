from flask import Flask, request, jsonify
import requests
import json

# 从配置文件中获取端口号，go-cqhttp的地址，QQ群号
with open('config.json') as config_file:
        config = json.load(config_file)

port = config['port']
go_cqhttp_url = config['go_cqhttp_url']

# 创建一个 Flask 应用
app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
        # 返回一个简单的HTML页面
        return """
            <html>
                <head>
                    <title>cqhttp-qqimagedeliver Status</title>
                </head>
                <body>
                    <h1>http通知服务启动成功</h1>
                </body>
            </html>
        """

@app.route('/', methods=['POST'])
def handle_notification():
        # 获取请求体中的数据
        data = request.json
        # 判断数据是否合法
        if data and 'image' in data and 'to' in data and 'info' in data:
                # 获取图片的 base64 编码，接收QQ号或群号，和文字信息
                image = data['image']
                to = data['to']
                info = data['info']
                if "每日单抽" not in info:
                    return jsonify(code=-2, msg='invalid data(Not a daily draw)')
                try:
                        # 构造一个 CQ 码，用于发送图片
                        cqcode = f"[CQ:image,file=base64://{image}]"
                        # 构造一个消息内容，包含图片和文字信息
                        message = f"{cqcode}\n{info}"

                        # 发送私信
                        # requests.post(f"{go_cqhttp_url}/send_private_msg", json={
                        #         'user_id': to,
                        #         'message': message,
                        # })
                        # 发送群消息
                        requests.post(f"{go_cqhttp_url}/send_group_msg", json={
                                'group_id': to,
                                'message': message,
                        })

                        # 返回成功的响应
                        return jsonify(code=0, msg='success')
                except Exception as error:
                        # 返回失败的响应
                        return jsonify(code=-1, msg=str(error))
        else:
                # 返回无效数据的响应
                return jsonify(code=-2, msg='invalid data')

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=port)