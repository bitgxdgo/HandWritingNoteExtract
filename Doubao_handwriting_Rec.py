import requests
import json
import os

def upload_file(file_path, api_key, user_id):
    """
    上传文件到服务器
    
    Args:
        file_path (str): 本地文件路径
        api_key (str): API密钥
        user_id (str): 用户标识
        
    Returns:
        dict: 服务器响应数据
    """
    # API端点
    url = 'http://localhost/v1/files/upload'
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    # 检查文件类型
    allowed_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.gif')
    if not file_path.lower().endswith(allowed_extensions):
        raise ValueError(f"不支持的文件类型。支持的类型: {allowed_extensions}")
    
    # 获取文件的MIME类型
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.webp': 'image/webp',
        '.gif': 'image/gif'
    }
    
    file_ext = os.path.splitext(file_path)[1].lower()
    mime_type = mime_types.get(file_ext)
    
    # 设置请求头
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    file_object = None
    try:
        file_object = open(file_path, 'rb')
        files = {
            'file': (
                os.path.basename(file_path),  # 文件名
                file_object,                  # 文件对象
                mime_type                     # MIME类型
            )
        }
        
        data = {
            'user': user_id
        }
        
        # 发送POST请求
        response = requests.post(
            url,
            headers=headers,
            files=files,
            data=data
        )
        
        # 检查响应状态
        response.raise_for_status()
        
        # 返回响应数据
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"上传失败: {str(e)}")
        raise
    finally:
        # 确保文件被关闭
        if file_object:
            file_object.close()

def chat_with_image(query, file_id, api_key, user_id, conversation_id=None):
    """
    使用上传的图片进行对话
    
    Args:
        query (str): 用户的问题
        file_id (str): 上传文件后获得的文件ID
        api_key (str): API密钥
        user_id (str): 用户标识
        conversation_id (str, optional): 会话ID
        
    Returns:
        dict: 服务器响应数据
    """
    url = 'http://localhost/v1/chat-messages'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",  # 使用阻塞模式便于演示
        "user": user_id,
        "files": [
            {
                "type": "image",
                "transfer_method": "local_file",
                "upload_file_id": file_id
            }
        ]
    }
    
    # 如果有会话ID，添加到请求中
    if conversation_id:
        payload["conversation_id"] = conversation_id
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {str(e)}")
        raise

def main():
    # 配置参数
    API_KEY = 'app-KU3LpTtE2J2eR0QmPqxegm7H'
    USER_ID = 'abc-123'
    FILE_PATH = '/Users/Zhuanz1/Ollama/note.png'  # 替换为实际的图片路径
    QUERY = "请抽取这张图片中的文字"  # 替换为你的问题
    
    try:
        # 第一步：上传文件
        print("正在上传文件...")
        upload_result = upload_file(FILE_PATH, API_KEY, USER_ID)
        file_id = upload_result['id']
        print(f"文件上传成功，ID: {file_id}")
        
        # 第二步：发送聊天请求
        print("\n发送问题...")
        chat_result = chat_with_image(QUERY, file_id, API_KEY, USER_ID)
        
        # 打印结果
        print("\n回答:")
        print(chat_result['answer'])
        
        # 打印使用情况
        if 'metadata' in chat_result and 'usage' in chat_result['metadata']:
            usage = chat_result['metadata']['usage']
            print("\n使用统计:")
            print(f"总Token数: {usage.get('total_tokens', 'N/A')}")
            print(f"总费用: ${usage.get('total_price', 'N/A')} {usage.get('currency', 'USD')}")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()