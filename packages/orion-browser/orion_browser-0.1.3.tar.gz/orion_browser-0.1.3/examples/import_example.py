#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个示例展示如何从orion_browser包中导入BrowserManager并使用
"""

# 从orion_browser包中导入BrowserManager
from orion_browser import BrowserManager

# 创建BrowserManager实例
def main():
    # 创建浏览器管理器实例
    browser_manager = BrowserManager()
    
    # 初始化浏览器（可选参数）
    browser_manager.initialize(
        headless=False,  # 设置为True可隐藏浏览器界面
        width=1280,
        height=800
    )
    
    # 访问网页
    result = browser_manager.navigate("https://www.baidu.com")
    print(f"导航结果: {result}")
    
    # 浏览器截图
    screenshot = browser_manager.screenshot()
    print(f"截图保存路径: {screenshot.image_path}")
    
    # 关闭浏览器
    browser_manager.close()

if __name__ == "__main__":
    main() 