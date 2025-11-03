import sys
import subprocess
import importlib.util
import locale

def load_student_function():
    """加载学生函数"""
    try:
        # 动态导入学生模块
        spec = importlib.util.spec_from_file_location("student_module", "main.py")
        student_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(student_module)
        return student_module.analyze_text, None
    except ImportError:
        return None, "❌ 错误: 找不到main.py文件"
    except AttributeError:
        return None, "❌ 错误: main.py中没有定义analyze_text函数"
    except SyntaxError as e:
        return None, f"❌ 语法错误: {e}"
    except Exception as e:
        return None, f"❌ 加载学生模块时出错: {e}"

def test_analyze_text(analyze_text):
    """测试文本分析功能"""
    test_cases = [
        # (输入文本, 预期频率字典)
        ("hello", {'l':2, 'h':1, 'e':1, 'o':1}),
        ("Hello World", {'l':3, 'o':2, 'h':1, 'e':1, 'w':1, 'r':1, 'd':1}),
        ("Mississippi", {'s':4, 'i':4, 'p':2, 'm':1}),
        ("你好世界", {'你':1, '好':1, '世':1, '界':1}),
        ("中文测试测试", {'测':2, '试':2, '中':1, '文':1}),
        ("重复字符测试测字符", {'测':3, '字':1, '符':1, '重':1, '复':1, '试':1}),
        ("Hello 你好", {'l':2, 'o':1, 'h':1, 'e':1, '你':1, '好':1}),
        ("Python编程", {'p':1, 'y':1, 't':1, 'h':1, 'o':1, 'n':1, '编':1, '程':1}),
        ("", {}),
        ("123!@#", {}),
        ("a a a a", {'a':4}),
    ]
    
    passed = 0
    total = len(test_cases)
    
    print("\n=== 文本分析功能测试 ===")
    for i, (input_text, expected_freq) in enumerate(test_cases):
        try:
            result = analyze_text(input_text)
            
            # 创建实际频率字典
            actual_freq = {}
            text_lower = input_text.lower()
            for char in text_lower:
                if char.isalpha():
                    actual_freq[char] = actual_freq.get(char, 0) + 1
            
            # 验证字符是否都在结果中
            missing_chars = [char for char in expected_freq if char not in result]
            extra_chars = [char for char in result if char not in expected_freq]
            
            # 验证排序是否正确（宽松验证）
            if result:
                # 获取频率值
                freqs = [expected_freq.get(char, 0) for char in result]
                
                # 检查是否降序（允许相同频率任意顺序）
                sort_valid = True
                for j in range(1, len(freqs)):
                    if freqs[j] > freqs[j-1]:
                        sort_valid = False
                        break
            else:
                sort_valid = True
            
            if not missing_chars and not extra_chars and sort_valid:
                passed += 1
                print(f"✅ 测试 #{i+1} 通过: '{input_text}'")
            else:
                print(f"⚠️ 测试 #{i+1} 失败: '{input_text}'")
                if missing_chars:
                    print(f"   缺少字符: {missing_chars}")
                if extra_chars:
                    print(f"   多余字符: {extra_chars}")
                if not sort_valid:
                    print(f"   排序错误: 非降序排列")
                print(f"   预期频率: {expected_freq}")
                print(f"   实际结果: {result}")
                
        except Exception as e:
            print(f"❌ 测试 #{i+1} 异常: '{input_text}'")
            print(f"   错误: {e}")
    
    score = int((passed / total) * 70)  # 功能测试占70分
    print(f"\n功能测试得分: {score}/70 (通过 {passed}/{total} 个测试)")
    return score

def test_main_program():
    """测试学生的主程序交互"""
    try:
        # 获取系统默认编码
        encoding = locale.getpreferredencoding()
        
        # 测试输入数据
        test_input = "This is a test\nHello World\n\n"
        
        # 运行主程序并提供输入（使用系统默认编码）
        result = subprocess.run(
            [sys.executable, "main.py"],
            input=test_input,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding=encoding
        )
        
        output = result.stdout
        
        # 检查是否有输出
        if not output.strip():
            print("❌ 主程序没有输出")
            return 0
        
        print("\n=== 主程序输出 ===")
        print(output)
        
        # 检查关键输出
        score = 30
        required_phrases = [
            "文本字符频率分析器",
            "请输入一段文本",
            "字符频率降序排列",
            "提示: 尝试输入中英文文章片段"
        ]
        
        missing = [phrase for phrase in required_phrases if phrase not in output]
        if missing:
            print(f"⚠️ 主程序缺少部分输出: {', '.join(missing)}")
            score = 20  # 部分得分
        
        # 检查分析结果
        if "t" in output.lower() and "s" in output.lower() and "l" in output.lower():
            print("✅ 主程序包含分析结果")
        else:
            print("⚠️ 主程序分析结果不完整")
            score = max(score - 10, 0)  # 扣分
        
        print(f"主程序测试得分: {score}/30")
        return score
    except Exception as e:
        print(f"❌ 主程序运行出错: {e}")
        return 0

def main():
    """主测试函数"""
    print("=" * 50)
    print("文本字符分析作业自动评分")
    print("=" * 50)
    
    # 加载学生函数
    analyze_text, error = load_student_function()
    if error:
        print(error)
        sys.exit(1)
    
    # 测试文本分析功能
    func_score = test_analyze_text(analyze_text)
    
    # 测试主程序交互
    main_score = test_main_program()
    
    # 计算总分
    total_score = func_score + main_score
    print("\n" + "=" * 50)
    print(f"最终得分: {total_score}/100")
    print("=" * 50)
    
    # 退出码（0表示通过，1表示失败）
    if total_score >= 60:
        print("🎉 评分通过!")
        sys.exit(0)
    else:
        print("💥 评分未通过")
        sys.exit(1)

if __name__ == "__main__":
    main()
