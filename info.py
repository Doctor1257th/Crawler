import requests
from lxml import etree
import pymysql
import logging
import json

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# 加载数据库配置
with open('config.json', 'r') as f:
    config = json.load(f)
mysql_local = config['mysql_local']

BASE_URLS = {
    "1": "https://www.tadu.com/store/98-a-0-15-a-20-p-",
    "2": "https://www.tadu.com/store/98-a-0-15-a-20-p-",
    "3": "https://www.tadu.com/store/122-a-0-15-a-20-p-"
}

class NovelInfo:
    def __init__(self):
        """初始化数据库连接"""
        self.conn = pymysql.connect(**mysql_local)

    def get_response(self, url, user_agent):
        """
        获取网页响应数据。

        Args:
            url (str): 目标网页 URL。
            user_agent (str): 请求头中的 User-Agent。

        Returns:
            requests.Response: 网页响应对象，如果请求失败则返回 None。
        """
        headers = {"User-Agent": user_agent}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logging.error(f"请求失败: {e}")
            return None

    def parse_data(self, response):
        """
        使用 XPath 解析网页数据。

        Args:
            response (requests.Response): 网页响应对象。

        Returns:
            list: 解析后的数据列表。
        """
        if response is None:
            return None

        html = etree.HTML(response.text)
        novel_name = html.xpath('//a[@class="bookNm"]/text()')
        novel_latest = html.xpath('//a[@class="updateNew"]/text()')
        novel_author = html.xpath('//a[@class="authorNm"]/text()')
        novel_genre = html.xpath('//a[@class="classifyLt"]/text()')
        novel_intro = html.xpath('//a[@class="bookIntro"]/text()')

        return list(zip(novel_name, novel_latest, novel_author, novel_genre, novel_intro))

    def save_data(self, data_list):
        """
        将数据存储到数据库。

        Args:
            data_list (list): 包含小说信息的列表。
        """
        if not data_list:
            logging.info("没有数据可存储")
            return

        sql = """
        INSERT INTO novel_info (novel_name, latest_chapter, author, novel_genre, novel_intro)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.executemany(sql, data_list)
            self.conn.commit()
            logging.info("数据存储成功")
        except pymysql.MySQLError as e:
            logging.error(f"存储失败: {e}")
            self.conn.rollback()

    def main(self):
        """主程序逻辑"""
        user_agent = input("请输入 User-Agent: ")
        genre = None
        while genre not in ["1", "2", "3"]:
            genre = input("请选择分类 (1. 男频文创 2. 男频全部 3. 女频): ")
            if genre not in ["1", "2", "3"]:
                logging.warning("输入无效，请重新选择")

        page_count = int(input("请输入页数: ")) + 1

        for page in range(1, page_count):
            url = f"{BASE_URLS[genre]}{page}"
            logging.info(f"正在处理页面: {url}")

            response = self.get_response(url, user_agent)
            if response is None:
                logging.error(f"无法获取页面数据，请检查 URL 是否合法或网络连接是否正常: {url}")
                continue

            data_list = self.parse_data(response)
            if data_list:
                self.save_data(data_list)
            else:
                logging.warning("当前页面没有解析到有效数据")

        logging.info("程序执行完成")


if __name__ == "__main__":
    try:
        novel_info = NovelInfo()
        novel_info.main()
    except Exception as e:
        logging.error(f"程序运行出错: {e}")
    finally:
        if novel_info.conn and novel_info.conn.open:
            novel_info.conn.close()
