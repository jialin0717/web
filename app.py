import os
import certifi
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# ==========================================
# 1. 数据库配置 (优先使用云端 URI)
# ==========================================
# 在 Render 的 Environment Variables 中添加 MONGO_URI 变量
MONGO_URI = os.environ.get('MONGO_URI') or "mongodb+srv://yonsei66760555_db_user:gZlCsZ4Gw2wH9Ok0@jialin.q9lhl7j.mongodb.net/?appName=jialin"
db = None

try:
    client = MongoClient(
        MONGO_URI,
        tlsCAFile=certifi.where() if "mongodb+srv" in MONGO_URI else None,
        serverSelectionTimeoutMS=5000
    )
    db = client.jialin_portfolio
    client.admin.command('ping')
    print("✅ 成功连接到云端数据库！")
except Exception as e:
    print(f"⚠️ 数据库连接失败: {e}")
    db = None

@app.route('/')
def index():
    return render_template('index.html')

# ==========================================
# 2. 修复后的项目接口 (从数据库读取)
# ==========================================
@app.route('/api/projects')
def get_projects():
    if db is None:
        return jsonify([])
    try:
        # 获取所有项目，并排除掉 MongoDB 自动生成的 _id (JSON 不支持直接传输 ObjectId)
        projs = list(db.projects.find({}, {'_id': 0}))
        return jsonify(projs)
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify([])

# 留言板功能保持不变...
@app.route('/api/message', methods=['POST'])
def post_message():
    if db is None: return jsonify({"status": "error", "message": "数据库未连接"})
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
    if db is None: return jsonify([])
    try:
        msgs = list(db.messages.find({}, {'_id': 0}).sort("time", -1).limit(20))
        return jsonify(msgs)
    except: return jsonify([])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)