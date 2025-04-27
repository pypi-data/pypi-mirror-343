# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2025/4/26 08:52
# 文件名称： wechat_mp_article_scraper.py
# 项目描述： 微信公众号群发记录爬虫
# 开发工具： PyCharm
import json
import re
import time
import logging
from typing import List
from DrissionPage import Chromium

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PublishHistory:
    def __init__(self, save_file: str = None, not_save: bool = False, pages_num=None, stop_to_date=None,
                 hide_browser: bool = False, pass_delete=True):
        """
        微信公众号文章发布历史数据
        注意：该类仅支持windows下使用，安装命令：pip install -U wechat_draft[windows]

        :param save_file: 保存文件路径，默认为 ./publish_articles.json
        :param not_save: 是否不保存数据到文件，默认为False
        :param pages_num: 爬取页数，默认为None，爬取全部页数。stop_to_date 比 pages_num 优先级高
        :param stop_to_date: 停止爬取的日期（不爬取设定时间的数据），默认为None，爬取全部日期，日期是发表记录页面显示的日期不要时间，例如：2024年05月21日、昨天、星期四
        :param hide_browser: 是否隐藏浏览器窗口，默认为False，限制在Windows系统下有效，并且需要安装pypiwin32库
        :param pass_delete: 跳过已删除的文章，默认为True
        """
        self.save_file = save_file or './publish_articles.json'
        self.not_save = not_save
        self.pages_num = pages_num
        self.stop_to_date = stop_to_date
        self.hide_browser = hide_browser
        self.pass_delete = pass_delete
        if hide_browser:
            logging.info('注意：隐藏浏览器窗口只能在Windows系统下使用，请确保安装了 pypiwin32\npip install pypiwin32\n')
        self.browser = Chromium()
        self.tab = self.browser.latest_tab
        # 设置全屏:https://drissionpage.cn/browser_control/page_operation/#%EF%B8%8F%EF%B8%8F-%E7%AA%97%E5%8F%A3%E7%AE%A1%E7%90%86
        self.tab.set.window.max()  # 设置全屏
        self.tab.set.window.show()  # 显示浏览器窗口

    def __access_page(self, url: str) -> None:
        """
        访问指定网页
        :param url: 要访问的网页URL
        """
        try:
            self.tab.get(url)
            logging.info(f"成功访问网页: {url}")
        except Exception as e:
            logging.error(f"访问网页 {url} 出错: {e}")

    def __click_login_button(self) -> None:
        """
        点击登录按钮
        """
        try:
            click_login = self.tab.ele('#jumpUrl')
            if click_login:
                click_login.click()
                logging.info("成功点击登录按钮")
        except Exception as e:
            logging.error(f"点击登录按钮出错: {e}")

    def __click_publish_tab(self) -> None:
        """
        点击全部发表记录标签页
        """
        logging.info('\n等待手动登入进入后台主页面...')
        logging.info('等待手动登入进入后台主页面...\n')
        try:
            # 等待元素出现
            self.tab.wait.ele_displayed('@text()=全部发表记录', timeout=60 * 5)
            # 新建标签页
            self.tab = self.tab.ele('@text()=全部发表记录').click.for_new_tab()
            # 隐藏浏览器窗口:pip install pypiwin32
            if self.hide_browser:
                logging.info('隐藏浏览器窗口...')
                self.tab.set.window.hide()
        except Exception as e:
            logging.error(f"点击全部发表记录标签页出错: {e}")

    @staticmethod
    def __extract_image_url(style_string):
        """提取图片URL"""
        pattern = r'url\("(.*?)"\)'
        match = re.search(pattern, style_string)
        if match:
            return match.group(1)
        return None

    def __save_data(self, publish_data):
        """保存数据到文件"""
        try:
            if not self.not_save:
                with open(self.save_file, 'w', encoding='utf-8') as f:
                    json.dump(publish_data, f, ensure_ascii=False, indent=4)
                logging.info(f"成功保存 {len(publish_data)} 条文章数据到 {self.save_file}")
        except Exception as e:
            logging.error(f"保存文章数据出错: {e}")

    def __parse_articles(self) -> List[dict]:
        """
        解析文章数据
        :return: 包含文章信息的列表
        """
        publish_data = []
        page_num = 1
        stop = False  # 添加标志变量
        while True:
            logging.info(f'\n====================第 {page_num} 页====================')
            # 使用静态元素定位，避免动态加载的元素：https://drissionpage.cn/browser_control/get_elements/find_in_object/#%EF%B8%8F%EF%B8%8F-%E9%9D%99%E6%80%81%E6%96%B9%E5%BC%8F%E6%9F%A5%E6%89%BE
            for div in self.tab.s_eles('@class=weui-desktop-block__main'):
                try:
                    # 发表的时间
                    date = div.ele('@tag()=em').text
                    if self.stop_to_date and date.startswith(self.stop_to_date):
                        logging.info(f'爬取到 {date} 停止（不包含{date}的数据）！')
                        stop = True  # 设置标志变量
                        break

                    title = div.ele('@class=weui-desktop-mass-appmsg__title').ele('@tag()=span')
                    # 跳过已删除的文章
                    if self.pass_delete and div.ele(
                            '@class=weui-desktop-mass-media weui-desktop-mass-appmsg weui-desktop-mass-media_del'):
                        logging.info(f'跳过已删除的文章: {title.text}')
                        continue

                    info = {
                        'title': title.text,
                        'url': title.parent().attr('href'),
                        'date': date,
                        'img': self.__extract_image_url(div.ele('@class=weui-desktop-mass-appmsg__thumb').attr('style'))
                    }
                    logging.info(info)
                    publish_data.append(info)

                except Exception as e:
                    logging.error(f"解析文章数据出错: {e}")
                    continue

            self.__save_data(publish_data)

            if stop:  # 检查标志变量
                break

            try:
                next_page_btn = self.tab.ele('下一页')
                if next_page_btn:
                    page_num += 1
                    if self.pages_num and page_num > self.pages_num:
                        break

                    next_page_btn.click()
                    time.sleep(0.5)
                else:
                    break
            except Exception as e:
                logging.error(f"点击下一页出错: {e}")
                break

        logging.info(f'共爬取 {len(publish_data)} 篇文章!')
        return publish_data

    def close_browser(self) -> None:
        """
        关闭浏览器
        """
        try:
            self.tab.close()
            self.browser.quit()
            logging.info("浏览器已关闭")
        except Exception as e:
            logging.error(f"关闭浏览器出错: {e}")

    def run(self) -> List[dict]:
        """
        执行整个爬取流程
        """
        logging.info("开始访问网页...")
        self.__access_page('https://mp.weixin.qq.com/cgi-bin/home')
        logging.info("尝试点击登录按钮...")
        self.__click_login_button()
        logging.info("点击全部发表记录标签页...")
        self.__click_publish_tab()
        logging.info("开始解析文章数据...")
        publish_data = self.__parse_articles()
        logging.info("爬取完成，关闭浏览器...")
        self.close_browser()
        return publish_data
