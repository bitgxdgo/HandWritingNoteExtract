import requests
import base64
import json

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_path):
    # 将图片转换为base64编码
    base64_image = encode_image_to_base64(image_path)
    
    # 准备请求数据
    payload = {
        "model": "llama3.2-vision",  # 使用支持视觉的模型
        "messages": [
            {
                "role": "user",
                "content": "识别文本内容",
                "images": [base64_image]
            }
        ],
        "stream": False
    }

    # 发送请求到Ollama API
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload
        )
        response.raise_for_status()
        
        # 修改响应处理逻辑
        result = response.json()
        if "message" in result and "content" in result["message"]:
            return result["message"]["content"]
        else:
            return "无法解析响应内容"
            
    except json.JSONDecodeError as e:
        return f"JSON解析错误: {str(e)}"
    except requests.exceptions.RequestException as e:
        return f"请求错误: {str(e)}"

if __name__ == "__main__":
    # 指定图片路径
    image_path = "/Users/Zhuanz1/Ollama/text.png"
    
    # 分析图片
    result = analyze_image(image_path)
    
    # 将结果保存到txt文件
    output_path = "analysis_result.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("模型分析结果：\n")
        f.write(result)
    
    print(f"分析结果已保存到 {output_path}")
