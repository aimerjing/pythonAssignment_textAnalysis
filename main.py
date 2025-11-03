# -*- coding: utf-8 -*-
# 在此文件处编辑代码
def analyze_text(text):
    """
    分析文本中字符频率并按频率降序排列
    
    参数:
    text - 输入的字符串
    
    返回:
    list - 按字符频率降序排列的字符列表
    """
    # 在此处增加代码
    

# 主程序，已完整
if __name__ == "__main__":
    print("文本字符频率分析器")
    print("====================")
    print("请输入一段文本（输入空行结束）：")
    
    # 读取多行输入
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break
    
    # 合并输入文本
    text = "\n".join(lines)
    
    if not text.strip():
        print("未输入有效文本！")
    else:
        # 分析文本
        sorted_chars = analyze_text(text)
        
        # 打印结果
        print("\n字符频率降序排列:")
        print(", ".join(sorted_chars))
        
        # 提示用户比较不同语言
        print("\n提示: 尝试输入中英文文章片段，比较不同语言之间字符频率的差别")
