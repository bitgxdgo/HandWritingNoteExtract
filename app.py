from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime
from Doubao_handwriting_Rec import upload_file, chat_with_image

app = Flask(__name__)

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# API配置
API_KEY = 'app-KU3LpTtE2J2eR0QmPqxegm7H'
USER_ID = 'abc-123'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_images():
    if 'files[]' not in request.files:
        return jsonify({'error': '没有文件上传'}), 400
    
    files = request.files.getlist('files[]')
    query = request.form.get('query', '请抽取这张图片中的文字')
    
    results = []
    for file in files:
        if file.filename:
            # 保存上传的文件
            temp_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(temp_path)
            
            try:
                # 上传文件到API
                upload_result = upload_file(temp_path, API_KEY, USER_ID)
                file_id = upload_result['id']
                
                # 处理图片
                chat_result = chat_with_image(query, file_id, API_KEY, USER_ID)
                
                # 保存结果
                result = {
                    'filename': file.filename,
                    'file_id': file_id,
                    'answer': chat_result['answer'],
                    'metadata': chat_result.get('metadata', {})
                }
                results.append(result)
                
            except Exception as e:
                results.append({
                    'filename': file.filename,
                    'error': str(e)
                })
            finally:
                # 清理临时文件
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    
    # 保存结果到JSON文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    result_file = f'results_{timestamp}.json'
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return jsonify({
        'message': '处理完成',
        'result_file': result_file,
        'results': results
    })

if __name__ == '__main__':
    app.run(debug=True)
