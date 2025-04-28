# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2025/4/26 08:52
# 文件名称： set_publish_params.py
# 项目描述： 设置微信公众号文章群发参数
# 开发工具： PyCharm
import time
from typing import List, Union
from DrissionPage import Chromium
from wechat_draft.utils.logger import log
from DrissionPage._functions.keys import Keys


class SetPublishParams:
    def __init__(self, titles: Union[str, List[str]] = None, set_digest: str = None, set_original: bool = False,
                 author: str = "XiaoqiangClub", quick_reprint: bool = False, open_comment: bool = False,
                 set_praise: bool = False, set_pay: bool = False, set_collect: list = None, original_link: str = None,
                 hide_browser: bool = False, ):
        """
        设置微信公众号文章群发参数
        注意：该类仅支持windows下使用，安装命令：pip install -U wechat_draft[windows]

        :param titles: 文章标题列表，支持单个标题或列表，为None，表示所有文章
        :param set_digest: 文章摘要，默认为None，不设置摘要
        :param set_original: 是否设置原创，默认为False
        :param author: 文章作者，默认为None，当设置原创的时候需要用到该参数，默认为：XiaoqiangClub
        :param quick_reprint: 是否开启快捷转载，默认为False。注意：当 set_pay 为True 时，该参数自动设置为False
        :param open_comment: 是否开启留言，默认为False
        :param set_praise: 是否开启赞赏，默认为False
        :param set_pay: 是否开启付费，默认为False，该功能作者暂时用不到，以后再写
        :param set_collect: 设置合集，默认为None，支持列表，如：['合集1', '合集2']
        :param original_link: 原文链接，默认为None
        :param hide_browser: 是否隐藏浏览器窗口，默认为False，限制在Windows系统下有效，并且需要安装 pypiwin32库
        """
        self.titles: list = [titles] if isinstance(titles, str) else titles
        self.set_digest = set_digest
        self.set_original = set_original
        self.author = author
        # 作者不能超过8个字符
        if self.author and len(self.author) > 8:
            # 报错
            log.error('作者不能超过8个字符')
            raise ValueError('作者不能超过8个字符')
        self.quick_reprint = quick_reprint
        self.open_comment = open_comment
        self.set_praise = set_praise
        self.set_pay = set_pay
        self.set_collect = set_collect
        # 合集总长度不能超过30个字符
        if self.set_collect and len(''.join(self.set_collect)) > 30:
            log.error('合集总长度不能超过30个字符')
            raise ValueError('合集总长度不能超过30个字符')
        self.original_link = original_link
        self.hide_browser = hide_browser

        if hide_browser:
            log.info('注意：隐藏浏览器窗口只能在Windows系统下使用，请确保安装了 pypiwin32\npip install pypiwin32\n')
        self.browser = Chromium()
        self.tab = self.browser.latest_tab
        self.edit_tab = None  # 编辑标签页
        # 设置全屏:https://drissionpage.cn/browser_control/page_operation/#%EF%B8%8F%EF%B8%8F-%E7%AA%97%E5%8F%A3%E7%AE%A1%E7%90%86
        # self.tab.set.window.max()  # 设置全屏
        self.tab.set.window.show()  # 显示浏览器窗口

    def __access_page(self, url: str, get_latest_tab: bool = True):
        """
        访问指定网页
        :param url: 要访问的网页URL
        :param get_latest_tab: 是否获取最新的标签页，默认为True
        """
        try:
            self.tab.get(url)
            if get_latest_tab:
                self.tab = self.browser.latest_tab
            log.info(f"成功访问网页: {url}")
            return self.tab
        except Exception as e:
            log.error(f"访问网页 {url} 出错: {e}")

    def __click_login_button(self) -> None:
        """
        点击登录按钮
        """
        try:
            click_login = self.tab.ele('#jumpUrl')
            if click_login:
                click_login.click()
                log.info("成功点击登录按钮")
        except Exception as e:
            log.error(f"点击登录按钮出错: {e}")

    def __enter_draft_box(self) -> None:
        """
        进入草稿箱
        """
        log.info('等待手动登入进入后台主页面🚬🚬🚬')
        try:
            # 等待元素出现
            self.tab.wait.ele_displayed('@text()=内容管理', timeout=60 * 5)
            # 点击 内容管理
            self.tab.ele('@text()=内容管理').click()
            # 点击 草稿箱，新建标签页
            self.tab.ele('@text()=草稿箱').click()
            # 切换草稿显示为列表视图
            self.tab.ele('#js_listview').click()
            # 隐藏浏览器窗口:pip install pypiwin32
            if self.hide_browser:
                log.info('隐藏浏览器窗口...')
                self.tab.set.window.hide()
        except Exception as e:
            log.error(f"进入草稿箱出错: {e}")

    def __set_params(self, url) -> List[dict]:
        """设置参数"""

        if self.edit_tab:
            self.edit_tab.get(url)
        else:
            self.edit_tab = self.browser.new_tab(url)

        # 将页面滚动到最底部
        log.info('将页面滚动到最底部...')
        self.edit_tab.ele('.tool_bar__fold-btn fold').click()

        time.sleep(1)
        # 设置文章摘要
        if self.set_digest:
            try:
                log.info(f'设置文章摘要: {self.set_digest}')
                self.edit_tab.actions.click('#js_description').type(Keys.CTRL_A).type(Keys.DELETE).input(
                    self.set_digest).type(Keys.CTRL_A).type(Keys.CTRL_C).type(Keys.CTRL_V)
            except Exception as e:
                log.error(f"设置文章摘要出错: {e}")

        # 设置原创
        if self.set_original:
            try:
                self.edit_tab.ele('.js_unset_original_title').click()

                self.edit_tab.actions.click(
                    'xpath://*[@id="js_original_edit_box"]/div/div[3]/div[2]/div/div/span[2]').type(
                    Keys.CTRL_A).type(Keys.BACKSPACE).input(self.author).type(Keys.CTRL_A).type(Keys.CTRL_C).type(
                    Keys.CTRL_V)

                # 开启 快捷转载
                if self.quick_reprint:
                    not_open = self.edit_tab.ele('@text()=未开启，只有白名单账号才能转载此文章')
                    if not_open:
                        log.info('开启 快捷转载')
                        not_open.prev().click()
                else:
                    is_open = self.edit_tab.ele('@text()=已开启，所有账号均可转载此文章')
                    if is_open:
                        log.info('关闭 快捷转载')
                        is_open.prev().click()

                # 勾选协议和确定
                log.info('点击确定')
                self.edit_tab.ele('@text()=确定').click()
                if self.edit_tab.ele('.js_author_explicit').text != '文字原创':
                    try:
                        # 勾选协议
                        log.info('勾选协议')
                        self.edit_tab.ele('.weui-desktop-icon-checkbox').click()
                        log.info('点击确定')
                        self.edit_tab.ele('@text()=确定').click()
                    except Exception as e:
                        log.error(f"勾选协议出错: {e}")
            except Exception as e:
                log.error(f"设置原创出错: {e}")

        # 打开赞赏
        try:
            if self.set_praise:
                log.info('即将设置打开赞赏，确保已经设置了赞赏账户！')
                if self.edit_tab.ele('.setting-group__switch-tips js_reward_setting_tips').text != '不开启':
                    log.info('原草稿已开启了赞赏，无需设置')
                else:
                    log.info('开启赞赏...')
                    self.edit_tab.ele('.setting-group__switch-tips js_reward_setting_tips').click()
                    # 点击确认
                    self.edit_tab.ele('@text()=确定').click()

            else:
                if self.edit_tab.ele('.setting-group__switch-tips js_reward_setting_tips').text != '不开启':
                    log.info('关闭赞赏...')
                    self.edit_tab.ele('.setting-group__switch-tips js_reward_setting_tips').click()
                    self.edit_tab.ele('@text()=赞赏类型').parent().ele('@text()=不开启').click()

                    # 点击确认
                    self.edit_tab.ele('@text()=确定').click()

        except Exception as e:
            log.error(f"设置赞赏出错: {e}")

        # 付费，暂时用不到，以后再写
        try:
            # 留言
            if self.open_comment:
                if 'selected' not in self.edit_tab.ele('.setting-group__switch-tips_default').parent().attr('class'):
                    log.info('开启留言...')
                    self.edit_tab.ele('.setting-group__switch-tips_default').click()
                    # 点击开启
                    self.edit_tab.ele('@text()=留言开关').parent().ele('@text()=开启').click()
                    # 点击确认
                    self.edit_tab.ele('xpath://*[@id="vue_app"]/div[3]/div[1]/div/div[3]/div/div[1]/button').click()
            else:
                if 'selected' in self.edit_tab.ele('.setting-group__switch-tips_default').parent().attr('class'):
                    log.info('关闭留言...')
                    self.edit_tab.ele('.setting-group__switch-tips js_interaction_content').click()
                    self.edit_tab.ele('@text()=留言开关').parent().ele('@text()=不开启').click()
                    # 点击确认
                    self.edit_tab.ele('xpath://*[@id="vue_app"]/div[2]/div[1]/div/div[3]/div/div[1]/button').click()
        except Exception as e:
            log.error(f"设置赞赏出错: {e}")

        # 设置合集
        try:
            if self.set_collect:
                self.edit_tab.actions.click('xpath://*[@id="js_article_tags_area"]/label/div')

                if self.edit_tab.ele('.weui-desktop-form-tag__input__label').text:
                    # 删除原来的合集
                    for _ in range(10):
                        self.edit_tab.actions.click('.weui-desktop-form-tag__input__label').type(Keys.DELETE)

                for collect in self.set_collect:
                    log.info(f'设置合集: {collect}')
                    self.edit_tab.actions.click('.weui-desktop-form-tag__input__label').input(collect).type(Keys.ENTER)
                # 点击确认
                self.edit_tab.ele('xpath://*[@id="vue_app"]/div[2]/div[1]/div/div[3]/div[1]/button').click()
        except Exception as e:
            log.error(f"设置合集出错: {e}")

        time.sleep(1)
        # 设置原文链接
        if self.original_link:
            try:
                self.edit_tab.actions.click('xpath://*[@id="js_article_url_area"]/label/div')
                self.edit_tab.actions.click('xpath:/html/body/div[17]/div/div[1]/div/div/div/span/input').type(
                    Keys.CTRL_A).type(Keys.DELETE).input(self.original_link)
                time.sleep(0.5)
                # 点击确认
                self.edit_tab.actions.click('xpath:/html/body/div[17]/div/div[2]/a[1]')
                time.sleep(0.5)
            except Exception as e:
                log.error(f"设置原文链接出错: {e}")

        # 点击保存为草稿
        log.info('点击保存为草稿...')
        self.edit_tab.ele('@text()=保存为草稿').click()

        # 等待保存为草稿成功
        self.edit_tab.wait.ele_displayed('@text()=首页')
        log.info('草稿保存成功！')

    def __set_publish_params(self) -> int:
        """
        设置文章群发参数
        :return: 处理的文章数量
        """
        url_params = self.tab.url.split('&action=list_card')[-1]
        # 判断标题是否为None，则获取全部文章

        page_num = 1  # 初始化页码为1
        parse_num = 0  # 初始化解析数量为0
        while True:
            log.info(f'\n====================第 {page_num} 页====================')
            # 使用静态元素定位，避免动态加载的元素：https://drissionpage.cn/browser_control/get_elements/find_in_object/#%EF%B8%8F%EF%B8%8F-%E9%9D%99%E6%80%81%E6%96%B9%E5%BC%8F%E6%9F%A5%E6%89%BE
            for tr in self.tab.s_eles('css:.weui-desktop-media__list-wrp tbody.weui-desktop-table__bd tr'):
                try:
                    # 标题
                    title = tr.ele('css:.weui-desktop-vm_primary span').text
                    # 找到编辑
                    edit = tr.ele('@text()=编辑')
                    # 查找当前元素之前第一个符合条件的兄弟节点
                    div = edit.prev(1, '@tag=a')
                    url = div.attr('href') + url_params
                    if self.titles is None or title in self.titles:
                        log.info(f"正在设置文章:《{title}》的发布参数：\n{url}")
                        # 设置参数
                        self.__set_params(url)
                        parse_num += 1

                except Exception as e:
                    log.error(f"设置文章参数出错: {e}")
                    continue

            try:
                next_page_btn = self.tab.ele('@text()=下一页')
                if next_page_btn:
                    page_num += 1
                    if self.titles is not None and parse_num >= len(self.titles):
                        break

                    next_page_btn.click()
                    time.sleep(0.5)
                else:
                    break
            except Exception as e:
                log.error(f"点击下一页出错: {e}")
                break

        log.info(f'共设置了 {parse_num} 篇文章的发布参数!')
        return parse_num

    def close_browser(self) -> None:
        """
        关闭浏览器
        """
        try:
            self.tab.close()
            self.browser.quit()
            log.info("浏览器已关闭")
        except Exception as e:
            log.error(f"关闭浏览器出错: {e}")

    def run(self) -> List[dict]:
        """
        执行整个爬取流程
        """
        log.info("开始访问网页...")
        self.__access_page('https://mp.weixin.qq.com/cgi-bin/home')
        log.info("尝试点击登录按钮...")
        self.__click_login_button()
        log.info("进入草稿箱...")
        self.__enter_draft_box()
        log.info("开始设置发布参数...")
        publish_data = self.__set_publish_params()
        log.info("爬取完成，关闭浏览器...")
        self.close_browser()
        return publish_data
        #
        # self.__set_params(
        #     'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&appmsgid=100043922&fromview=list&token=158574414&lang=zh_CN&timestamp=1745745904067')
