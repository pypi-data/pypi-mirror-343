# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2025/4/26 08:52
# 文件名称： wechat_mp_article_scraper.py
# 项目描述： 微信公众号群发记录爬虫
# 开发工具： PyCharm
import json
import re
import time
from typing import List
from DrissionPage import Chromium


class PublishHistory:
    def __init__(self, save_file: str = None, hide_browser: bool = False):
        """
        微信公众号文章发布历史数据
        注意：该类仅支持windows下使用，安装命令：pip install -U wechat_draft[windows]

        :param save_file: 保存文件路径，默认为None
        :param hide_browser: 是否隐藏浏览器窗口，默认为False，限制在Windows系统下有效，并且需要安装pypiwin32库
        """

        self.save_file = save_file or './publish_articles.json'
        self.hide_browser = hide_browser
        if hide_browser:
            print('注意：隐藏浏览器窗口只能在Windows系统下使用，请确保安装了 pypiwin32\npip install pypiwin32\n')
        self.browser = Chromium()
        self.tab = self.browser.latest_tab
        # 设置全屏:https://drissionpage.cn/browser_control/page_operation/#%EF%B8%8F%EF%B8%8F-%E7%AA%97%E5%8F%A3%E7%AE%A1%E7%90%86
        self.tab.set.window.max()  # 设置全屏
        self.tab.set.window.show()  # 显示浏览器窗口

    def access_page(self, url: str) -> None:
        """
        访问指定网页
        :param url: 要访问的网页URL
        """
        self.tab.get(url)

    def click_login_button(self) -> None:
        """
        点击登录按钮
        """
        click_login = self.tab.ele('#jumpUrl')
        if click_login:
            click_login.click()

    def click_publish_tab(self) -> None:
        """
        点击全部发表记录标签页
        """
        print('等待登入进入后台主页面...')
        all_publish = self.tab.ele('@text()=全部发表记录')
        # 等待元素出现
        all_publish.wait.displayed(timeout=60 * 5)  # 等待元素出现，最长等待时间设为5分钟
        self.tab = all_publish.click.for_new_tab()
        # 隐藏浏览器窗口:pip install pypiwin32
        if self.hide_browser:
            print('隐藏浏览器窗口...')
            self.tab.set.window.hide()

    @staticmethod
    def extract_image_url(style_string):
        """提取图片URL"""
        pattern = r'url\("(.*?)"\)'
        match = re.search(pattern, style_string)
        if match:
            return match.group(1)
        return None

    def parse_articles(self) -> List[dict]:
        """
        解析文章数据
        :return: 包含文章信息的列表
        """
        publish_data = []
        page_num = 1
        while True:
            # 使用静态元素定位，避免动态加载的元素：https://drissionpage.cn/browser_control/get_elements/find_in_object/#%EF%B8%8F%EF%B8%8F-%E9%9D%99%E6%80%81%E6%96%B9%E5%BC%8F%E6%9F%A5%E6%89%BE
            print(f'\n====================第 {page_num} 页====================')
            for div in self.tab.s_eles('@class=weui-desktop-block__main'):
                try:
                    # 跳过广告文章
                    if div.ele('@class=weui-desktop-mass-appmsg__tips'):
                        continue

                    title = div.ele('@class=weui-desktop-mass-appmsg__title').ele('@tag()=span')
                    info = {
                        'title': title.text,
                        'url': title.parent().attr('href'),
                        'date': div.ele('@tag()=em').text,
                        'img': self.extract_image_url(div.ele('@class=weui-desktop-mass-appmsg__thumb').attr('style'))
                    }
                    print(info)
                    publish_data.append(info)
                except Exception as e:
                    print(f"解析文章数据出错: {e}")
                    continue

            try:
                with open(self.save_file, 'w', encoding='utf-8') as f:
                    json.dump(publish_data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"保存文章数据出错: {e}")

            try:
                if self.tab.ele('下一页'):
                    page_num += 1
                    self.tab.ele('下一页').click()
                    time.sleep(0.5)
                else:
                    break
            except Exception as e:
                print(f"点击下一页出错: {e}")
                break

        print(f'共爬取 {len(publish_data)} 篇文章!')
        return publish_data

    def close_browser(self) -> None:
        """
        关闭浏览器
        """
        time.sleep(3)
        self.tab.close()
        time.sleep(3)
        self.browser.quit()

    def run(self) -> List[dict]:
        """
        执行整个爬取流程
        """
        print("开始访问网页...")
        self.access_page('https://mp.weixin.qq.com/cgi-bin/home')
        print("尝试点击登录按钮...")
        self.click_login_button()
        print("点击全部发表记录标签页...")
        self.click_publish_tab()
        print("开始解析文章数据...")
        publish_data = self.parse_articles()
        print("爬取完成，关闭浏览器...")
        self.close_browser()
        return publish_data
