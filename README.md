# NovelInfo Crawler

一个用于抓取小说信息并存储到MySQL数据库的Python爬虫项目。

## 项目概述
本项目通过爬取[塔读文学网书库](https://www.tadu.com/store/98-a-0-15-a-20-p-1-909)的小说信息，提取小说名称、最新章节、作者、小说类别和简介，并将这些信息存储到本地MySQL数据库中。项目旨在帮助用户快速收集和管理小说数据。

## 功能特点
- 支持多分类抓取（男频文创、男频全部、女频）。
- 动态页码抓取，可根据用户输入抓取指定页数。
- 数据存储到MySQL数据库，便于后续查询和分析。
- 日志记录功能，方便调试和跟踪运行状态。

## 安装指南
### 1. 克隆项目
通过以下命令克隆项目到本地：
```bash
git clone https://github.com/Doctor1257th/Crawler.git
cd Crawler
```

### 2. 安装依赖
安装项目所需的Python依赖库：
```bash
pip install requests lxml pymysql
```

### 3. 配置数据库
1. 确保你的MySQL服务已启动。
2. 创建数据库和表：
   ```sql
   CREATE DATABASE test;
   USE test;
   CREATE TABLE novel_info (
       id INT AUTO_INCREMENT PRIMARY KEY,
       novel_name VARCHAR(255),
       latest_chapter VARCHAR(255),
       author VARCHAR(255),
       novel_genre VARCHAR(255),
       novel_intro VARCHAR(255)
   );
   ```
3. 创建`config.json`文件：
   在项目根目录下创建一个`config.json`文件，内容如下：
   ```json
   {
       "mysql_local": {
           "host": "localhost",
           "port": 3306,
           "user": "root",
           "password": "your_password",
           "database": "test"
       }
   }
   ```
   **注意**：请将`your_password`替换为你的MySQL数据库密码。

## 使用方法
### 1. 启动程序
运行主程序：
```bash
python info.py
```

### 2. 输入参数
根据提示输入以下信息：
- **User-Agent**：用于模拟浏览器请求的`User-Agent`字符串。你可以通过浏览器开发者工具获取。
- **分类**：选择小说分类（1. 男频文创，2. 男频全部，3. 女频）。
- **页数**：输入需要抓取的页数。

程序将自动抓取指定分类和页数的小说信息，并存储到数据库中。

## 项目结构
```
Crawler/
├── info.py                # 主程序
├── README.md              # 项目说明
├── config.json            # 数据库配置文件（需手动创建）
└── requirements.txt       # 依赖文件
```
