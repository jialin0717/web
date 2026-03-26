import os
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import certifi

app = Flask(__name__)

# --- 数据库配置 (仅保留留言板功能，如果留言板也不要了，这一块可以全删) ---
MONGO_URI = os.environ.get('MONGO_URI') or "mongodb+srv://yonsei66760555_db_user:gZlCsZ4Gw2wH9Ok0@jialin.q9lhl7j.mongodb.net/?appName=jialin"
db = None

try:
    # 使用最简单的连接方式，不再强制 ping，防止启动时报错导致网站打不开
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=2000)
    db = client.jialin_portfolio
    print("✅ 数据库已连接 (用于留言板)")
except Exception as e:
    print(f"⚠️ 数据库连接跳过 (不影响前端展示): {e}")

# --- 核心路由 ---

@app.route('/')
def index():
    # 只要这个路由在，你的 index.html 就能显示
    return render_template('index.html')

@app.route('/api/projects')
def get_projects():
    # 因为你已经在前端写死了 demoProjects，这个接口返回空即可，防止报错
    return jsonify([])

# --- 留言板 API (可选保留) ---

@app.route('/api/message', methods=['POST'])
def post_message():
    if db is None: return jsonify({"status": "error", "message": "Database disconnected"})
    data = request.json
    new_msg = {
        "name": data.get('name', '匿名用户'),
        "content": data.get('content'),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    db.messages.insert_one(new_msg)
    return jsonify({"status": "success"})

@app.route('/api/get_messages')
def get_messages():
    if db is None: return jsonify([])
    try:
        msgs = list(db.messages.find({}, {'_id': 0}).sort("time", -1).limit(20))
        return jsonify(msgs)
    except:
        return jsonify([])

# --- 启动 ---

if __name__ == '__main__':
    # 统一使用环境变量中的 PORT，Render 默认为 10000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)