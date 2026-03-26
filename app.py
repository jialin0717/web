import os
import certifi
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# --- 1. 数据库配置 (仅保留留言板功能) ---
# 既然项目内容已经在 HTML 里了，数据库现在只负责存取访客留言
MONGO_URI = os.environ.get('MONGO_URI') or "mongodb+srv://yonsei66760555_db_user:gZlCsZ4Gw2wH9Ok0@jialin.q9lhl7j.mongodb.net/?appName=jialin"
db = None

try:
    # 使用 certifi 解决 Render 环境下的 SSL 证书问题
    client = MongoClient(
        MONGO_URI,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000
    )
    db = client.jialin_portfolio
    # 仅测试连接，不成功也不影响网页打开
    client.admin.command('ping')
    print("✅ MongoDB 留言板数据库连接成功")
except Exception as e:
    print(f"⚠️ 数据库连接异常 (不影响项目展示): {e}")
    db = None

# --- 2. 核心路由 ---

@app.route('/')
def index():
    # 只要这个在，你的 index.html 就能正常加载
    return render_template('index.html')

@app.route('/api/projects')
def get_projects():
    # 关键修改：返回一个空列表
    # 因为 index.html 里的 fetchProjects 已经不再依赖这个接口了
    return jsonify([])

# --- 3. 留言板 API (保持不变) ---

@app.route('/api/message', methods=['POST'])
def post_message():
    if db is None: return jsonify({"status": "error", "message": "数据库未连接"})
    try:
        data = request.json
        new_msg = {
            "name": data.get('name', '访客'),
            "content": data.get('content', ''),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        db.messages.insert_one(new_msg)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/get_messages')
def get_messages():
    if db is None: return jsonify([])
    try:
        msgs = list(db.messages.find({}, {'_id': 0}).sort("time", -1).limit(20))
        return jsonify(msgs)
    except:
        return jsonify([])

if __name__ == '__main__':
    # 适配 Render 的端口
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)