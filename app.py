import os
import certifi
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# --- 数据库连接 (仅用于留言板) ---
MONGO_URI = os.environ.get('MONGO_URI') or "mongodb+srv://yonsei66760555_db_user:gZlCsZ4Gw2wH9Ok0@jialin.q9lhl7j.mongodb.net/?appName=jialin"

try:
    # 使用 certifi 解决 SSL 证书问题，serverSelectionTimeoutMS 设短一点防止卡死
    client = MongoClient(
        MONGO_URI,
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True,
        serverSelectionTimeoutMS=5000
    )
    db = client.jialin_portfolio
    # 尝试检查连接
    client.admin.command('ping')
    print("✅ MongoDB 连接成功 (留言板已就绪)")
except Exception as e:
    print(f"⚠️ 数据库连接异常: {e}")
    db = None

# --- 路由 ---

@app.route('/')
def index():
    return render_template('index.html')

# 这里的项目接口返回空即可，因为前端已经不靠它了
@app.route('/api/projects')
def get_projects():
    return jsonify([])

# --- 留言板 API (保留) ---

@app.route('/api/message', methods=['POST'])
def post_message():
    if db is None: return jsonify({"status": "error", "message": "数据库未连接"})
    try:
        data = request.json
        new_msg = {
            "name": data.get('name', '匿名用户'),
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
        # 获取最近 20 条留言
        msgs = list(db.messages.find({}, {'_id': 0}).sort("time", -1).limit(20))
        return jsonify(msgs)
    except:
        return jsonify([])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)