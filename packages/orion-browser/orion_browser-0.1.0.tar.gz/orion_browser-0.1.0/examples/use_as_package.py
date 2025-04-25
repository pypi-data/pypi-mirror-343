#!/usr/bin/env python3
"""
示例：如何将Orion作为库导入并使用

此示例展示：
1. 如何导入orion模块
2. 如何使用浏览器管理器
3. 如何使用终端管理器
4. 如何使用文本编辑器
"""

import asyncio
import os
from app import BrowserManager, terminal_manager, text_editor
from app.models import MultipartUploadRequest
from app.types.messages import BrowserActionRequest, TextEditorAction

async def browser_example():
    """浏览器管理器使用示例"""
    print("=== 浏览器管理器示例 ===")
    
    # 创建浏览器管理器实例
    browser = BrowserManager(headless=False)
    
    try:
        # 初始化浏览器
        await browser.initialize()
        print("浏览器已初始化")
        
        # 导航到网页
        action = BrowserActionRequest(
            action="navigate",
            args={"url": "https://www.baidu.com"}
        )
        result = await browser.execute_action(action)
        print(f"导航结果: {result.title} - {result.url}")
        
        # 等待一段时间以便查看页面
        await asyncio.sleep(3)
        
        # 关闭浏览器
        await browser.close()
        print("浏览器已关闭")
    except Exception as e:
        print(f"浏览器错误: {e}")
        await browser.close()

async def terminal_example():
    """终端管理器使用示例"""
    print("\n=== 终端管理器示例 ===")
    
    try:
        # 创建或获取终端
        terminal_id = "example"
        terminal = await terminal_manager.create_or_get_terminal(terminal_id)
        print(f"终端已创建，ID: {terminal_id}")
        
        # 执行命令
        command = "echo 'Hello from Orion Terminal'; ls -la"
        print(f"执行命令: {command}")
        await terminal.execute_command(command)
        
        # 等待命令执行完成
        await asyncio.sleep(2)
        
        # 获取终端历史
        history = terminal.get_history(True, True)
        print("终端输出:")
        for entry in history[-5:]:  # 只显示最后5行
            print(f"  {entry}")
        
        # 重置终端
        await terminal.reset()
        print("终端已重置")
    except Exception as e:
        print(f"终端错误: {e}")

async def text_editor_example():
    """文本编辑器使用示例"""
    print("\n=== 文本编辑器示例 ===")
    
    try:
        # 创建测试文件
        test_file = "/tmp/orion_test.txt"
        with open(test_file, "w") as f:
            f.write("这是一个测试文件\n第二行\n第三行")
        
        # 读取文件
        action = TextEditorAction(
            action="read_file",
            target_file=test_file
        )
        result = await text_editor.run_action(action)
        print(f"读取文件内容: \n{result.output}")
        
        # 编辑文件
        action = TextEditorAction(
            action="write_file",
            target_file=test_file,
            content="这是一个修改后的测试文件\n新的第二行\n新的第三行"
        )
        result = await text_editor.run_action(action)
        print(f"文件修改状态: {result.success}")
        
        # 再次读取文件
        action = TextEditorAction(
            action="read_file",
            target_file=test_file
        )
        result = await text_editor.run_action(action)
        print(f"修改后的文件内容: \n{result.output}")
        
        # 删除测试文件
        os.remove(test_file)
        print(f"测试文件已删除: {test_file}")
    except Exception as e:
        print(f"文本编辑器错误: {e}")

async def main():
    """运行所有示例"""
    print("Orion库使用示例\n")
    
    # 运行浏览器示例
    await browser_example()
    
    # 运行终端示例
    await terminal_example()
    
    # 运行文本编辑器示例
    await text_editor_example()

if __name__ == "__main__":
    asyncio.run(main()) 