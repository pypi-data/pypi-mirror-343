# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2025/4/26 10:48
# 文件名称： set_publish_params.py
# 项目描述： 设置微信公众号文章群发参数
# 开发工具： PyCharm

from wechat_draft import SetPublishParams


async def set_publish_params():
    set_publish_params = SetPublishParams(['测试标题', '测试文章2', '测试文章3'], set_digest='测试22摘要', set_original=True,
                                          author='小钱',
                                          quick_reprint=True, set_collect=['工具箱'], open_comment=True,
                                          set_praise=True, original_link='https://www.baidu.com')
    return set_publish_params.run()


if __name__ == '__main__':
    import asyncio

    print(asyncio.run(set_publish_params()))
