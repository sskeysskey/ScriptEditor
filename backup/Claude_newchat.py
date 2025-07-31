import os
import cv2
import pyautogui
import numpy as np
from time import sleep
from PIL import ImageGrab

def capture_screen():
    # 使用PIL的ImageGrab直接截取屏幕
    screenshot = ImageGrab.grab()
    # 将截图对象转换为OpenCV格式
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot

# 查找图片
def find_image_on_screen(template_path, threshold=0.9):
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"模板图片未能正确读取于路径 {template_path}")
    screen = capture_screen()
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # 释放截图和模板图像以节省内存
    del screen
    if max_val >= threshold:
        return max_loc, template.shape
    else:
        return None, None

def click_image(location, shape):
    # 计算中心坐标
    center_x = (location[0] + shape[1] // 2) // 2
    center_y = (location[1] + shape[0] // 2) // 2
    # 鼠标点击中心坐标
    pyautogui.click(center_x, center_y)

# 主函数
def main():
        template_path1 = '/Users/yanzhang/Documents/python_code/Resource/claude_new_chat.png'
        template_path2 = '/Users/yanzhang/Documents/python_code/Resource/claude_message.png'
        found1 = False  # 初始化一个标志变量
        while not found1:  # 使用标志变量作为循环条件
            location, shape = find_image_on_screen(template_path1)
            if location:
                click_image(location, shape)
                found1 = True  # 找到图片后，更新标志变量
            else:
                print("未找到A图片，继续监控...")
                sleep(1)  # 简短暂停再次监控

        # 点击第一张图片后，检测第二张图片是否出现
        found2 = False  # 初始化一个标志变量
        while not found2:  # 使用标志变量作为循环条件
            location, shape = find_image_on_screen(template_path2)
            if location:
                found2 = True  # 找到图片后，更新标志变量
            else:
                print("未找到第二张图片，继续监控...")
                sleep(1)

if __name__ == '__main__':
    main()