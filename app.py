import os
import certifi
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# ==========================================
# 1. 数据库配置 (优先尝试本地连接)
# ==========================================
# 如果是在你电脑上跑，它连 localhost；如果在 Render 上跑，它尝试连环境变量里的地址
MONGO_URI = os.environ.get('MONGO_URI') or "mongodb://localhost:27017/"
db = None

try:
    # 设置 2 秒超时，防止数据库连不上时卡住整个网页加载
    client = MongoClient(
        MONGO_URI,
        tlsCAFile=certifi.where() if "mongodb+srv" in MONGO_URI else None,
        serverSelectionTimeoutMS=2000
    )
    db = client.jialin_portfolio
    # 简单的连接测试
    client.admin.command('ping')
    print("✅ 数据库连接成功！")
except Exception as e:
    print(f"⚠️ 数据库未就绪 (不影响项目展示): {e}")
    db = None

# ==========================================
# 2. 页面路由
# ==========================================

@app.route('/')
def index():
    # 核心：直接返回你的 index.html
    # 你的延世大学经历现在全在这个 HTML 里的 demoProjects 数组中
    return render_template('index.html')

@app.route('/api/projects')
def get_projects():
    # 既然项目已经写死在前端，这个接口返回空即可
    return jsonify([])

# ==========================================
# 3. 留言板功能接口 (保留)
# ==========================================

@app.route('/api/message', methods=['POST'])
def post_message():
    if db is None:
        return jsonify({"status": "error", "message": "数据库未连接，无法留言"})
    try:
        data = request.json
        new_msg = {
            "name": data.get('name', '匿名访客'),
            "content": data.get('content', ''),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        db.messages.insert_one(new_msg)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/get_messages')
def get_messages():
    if db is None:
        return jsonify([])
    try:
        # 获取最新的 20 条留言
        msgs = list(db.messages.find({}, {'_id': 0}).sort("time", -1).limit(20))
        return jsonify(msgs)
    except:
        return jsonify([])

# ==========================================
# 4. 启动配置
# ==========================================

if __name__ == '__main__':
    # 自动识别 Render 端口，本地默认为 5000
    port = int(os.environ.get('PORT', 5000))
    # 生产环境 debug 应设为 False
    app.run(host='0.0.0.0', port=port, debug=False)