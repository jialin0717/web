from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime


import os
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# 使用 os.environ 获取变量
uri = os.environ.get('MONGO_URI')

try:
    client = MongoClient(uri)
    # 强制进行一次连接测试
    client.admin.command('ping')
    db = client.get_database('jialin_portfolio') # 确保数据库名正确
    print("MongoDB 连接成功！")
except Exception as e:
    print(f"MongoDB 连接失败: {e}")

    
app = Flask(__name__)

# ==========================================
# 1. 数据库配置 (NoSQL - MongoDB Atlas)
# ==========================================
# 你的云端连接字符串
MONGO_URI = "mongodb+srv://yonsei66760555_db_user:gZlCsZ4Gw2wH9Ok0@jialin.q9lhl7j.mongodb.net/?appName=jialin"

try:
    # 建立连接
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # 指定数据库名称
    db = client.jialin_portfolio
    client.server_info()  # 检查连接是否成功
    print("✅ 成功连接到 MongoDB Atlas 云数据库！")
except Exception as e:
    print(f"❌ MongoDB 连接失败: {e}")
    db = None

# ==========================================
# 2. 数据库初始化函数
# ==========================================
def init_db():
    """初始化数据库：强制更新为最新的学联工作经历"""
    if db is not None:
        # 强制删除旧集合，确保你的新文字能显示出来
        db.projects.drop()

        # 模块 1 的详细经历文字
        detailed_exp_1 = """2024年09月-2025年07月
担任延世大学中国学人学者联谊会（原）组织部部员

2024年2学期
延世大学国际处GOSC新生说明会活动策划案撰写和活动所需物品采购

2025年1学期
参与组织延世大学中国学人学者联谊会“大同节”活动，负责联谊会“鹰花会”策划案撰写

2025年09月-2025年12月
担任延世大学中国学人学者联谊会组织部副部长

2025年12月—至今

担任延世大学中国学人学者联谊会战略运营部部长
主要负责学联财务管理、文书秘书以及活动组织策划工作


"""
        # 模块 4 的详细经历文字
        detailed_exp_4 = """2013年
荣获由文化部中国儿童戏剧研究会、中国艺术家协会、中国人生科学学会共同主办的德艺双馨第九届中国文艺展示活动黑龙江选区钢琴专业组银奖
“华夏艺术风采国际交流展演”活动黑龙江赛区书画类银奖
2015年
参与由黑龙江军旅小战术训练营组委会组织的黑龙江军旅训练活动
2017年
荣获红领巾广播电视“希望杯”校园学生英语演讲大赛优胜奖
2018年
荣获德强学校初中部主办的德强学校校园艺术节美术作品大赛一等奖
2023年
考取中国商业联合会计算机信息技术专像技能，计算机信息技术四级（中级）证书
2024年
参与新教育时代杂志编辑部主办的2024高校青年爱国主义教育宣传活动，获得“奋进青年”荣誉称号
2025年
参与“亚东有我，加油中国”2025全国青年助力第九届亚冬会宣传活动
延世大学中国学人学者联谊会研究决定，聘任本人为2025年秋季学期“中国日”活动执行总导演、总策划。聘期自2025年9月1日至2025年11月14日


        """
        # 模块5的详细经历文字
        detailed_exp_5 = """
1.简单计算机编程能力

2.大型活动策划与执行能力：
作为学联组织部成员及副部长，多次负责或参与撰写活动策划案，这是项目管理初步体现。特担任“中国日”活动总导演的经历体现了具备全方位的项目领导能力：
从前期的创意策划、方案撰写，到中期的节目编排、灯光音响等技术协调，再到活动当天的人员调度与现场指挥。这涵盖了项目规划、资源协调、团队管理、风险控制
和应急处理等高级管理技能。

3.团队协作与组织能力：
在学联的组织部工作中，参与组织了新生说明会、MT、大同节、鹰花会、欢迎会等多种活动，展现了优秀的团队合作精神和在集体中完成复杂任务的能力。
从部员晋升为副部长，体现了您的责任感、可靠性和组织内部的认可。

4.卓越的中文沟通与文案能力：
具备出色的书面表达能力、逻辑思维和方案构思能力。在韩国高校的中国学生组织中担任核心职务，需要极强的中文沟通协调能力。

5.跨文化环境适应与协作能力：
在韩国顶尖大学求学，并在国际处合作开展GOSC活动中证明了能熟练适应国际化环境，与不同文化背景的师生、机构进行有效沟通和协作。
作为连接中国学生与学校、乃至韩国社会的桥梁。

6.优秀的学习能力以及艺术修养与创造力：
从活动参与者成长为大型项目的总导演，主动承担责任并推动执行。艺术获奖经历培养了审美与创造力，这对策划活动和技术设计都有帮助。
能适应不同的教育环境并完成高强度学业，证明了出色的学习能力。积极参与社会宣传活动，展现了团队精神和集体荣誉感。
   
                """

        demo_projects = [
            {
                "id": 1,
                "title": "延世大学中国学人学者联谊会 工作经历",
                "tags": ["学联", "工作经历"],
                "hits": 0,
                "desc": detailed_exp_1
            },
            {
                "id": 2,
                "title": "CSSA 主要活动",
                "tags": ["学联", "主要活动"],
                "hits": 0,
                "desc": "2025-2学期 “中国日”大型晚会总导演，晚会执行总导演、总策划。负责前期策划案撰写、灯光音响编排、节目编排及人员调动。"
            },
            {
                "id": 3,
                "title": "Linux Automation Tool",
                "tags": ["Bash", "Git"],
                "hits": 0,
                "desc": "基于 Bash 的自动化运维脚本，集成 Git 内部数据结构分析功能，用于自动化部署服务器环境。"
            },
            {
                "id": 4,
                "title": "所获奖项",
                "tags": ["所获奖项"],
                "hits": 0,
                "desc":  detailed_exp_4
            },
            {
                "id": 5,
                "title": "个人能力",
                "tags": ["个人能力"],
                "hits": 0,
                "desc": detailed_exp_5
            }
        ]
        db.projects.insert_many(demo_projects)
        print(">>> 数据库已成功初始化：最新的学联经历已录入。")
pass

# ==========================================
# 2. 核心路由
# ==========================================
@app.route('/')
def index():
    return render_template('index.html')


# ==========================================
# 3. 项目 API
# ==========================================
@app.route('/api/projects')
def get_projects():
    if db is None: return jsonify([])
    projects = list(db.projects.find({}, {'_id': 0}))
    return jsonify(projects)


@app.route('/api/click', methods=['POST'])
def record_click():
    if db is None: return jsonify({"status": "error"})
    project_id = request.json.get('id')
    db.projects.update_one({"id": project_id}, {"$inc": {"hits": 1}})
    return jsonify({"status": "success"})


@app.route('/api/recommend')
def recommend():
    if db is None: return jsonify(None)
    top_project = db.projects.find_one({}, {'_id': 0}, sort=[("hits", -1)])
    return jsonify(top_project)


# ==========================================
# 4. 留言板 API
# ==========================================
@app.route('/api/message', methods=['POST'])
def post_message():
    if db is None: return jsonify({"status": "error"})
    data = request.json
    new_msg = {
        "name": data.get('name', '匿名用户') or '匿名用户',
        "content": data.get('content'),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    db.messages.insert_one(new_msg)
    return jsonify({"status": "success"})


@app.route('/api/get_messages')
def get_messages():
    if db is None: return jsonify([])
    msgs = list(db.messages.find({}, {'_id': 0}).sort("time", -1))
    return jsonify(msgs)


# ==========================================
# 5. 启动
# ==========================================
if __name__ == '__main__':
    init_db()
    # 使用 127.0.0.1 确保本地访问稳定性
    app.run(host='127.0.0.1', port=5000, debug=True)