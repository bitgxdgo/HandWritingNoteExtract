from paddleocr import PaddleOCR
ocr = PaddleOCR(lang='en') # need to run only once to load model into memory
img_path = '/Users/Zhuanz1/Ollama/text.png'
output_txt_path = '/Users/Zhuanz1/Ollama/article.txt'  # 定义输出txt文件的路径

result = ocr.ocr(img_path, det=True, cls=False)
with open(output_txt_path, 'w', encoding='utf-8') as f:
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            text = line[1][0]  # 提取识别的文本
            print(text)
            f.write(text + '\n')  # 将文本写入txt文件，每行一个识别结果

