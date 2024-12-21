from cnocr import CnOcr
from datetime import datetime

# 指定图片路径
img_fp = '/Users/Zhuanz1/Ollama/text.png'
ocr = CnOcr()  # 所有参数都使用默认值
out = ocr.ocr(img_fp)

# 生成包含时间戳的文件名
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"ocr_result_{timestamp}.txt"

# 将结果保存到txt文件
with open(output_path, "w", encoding="utf-8") as f:
    f.write("OCR识别结果：\n")
    for line in out:
        if isinstance(line, str):
            f.write(line + "\n")
        else:
            f.write(str(line) + "\n")

print(f"OCR识别结果已保存到 {output_path}")
print(out)  # 保留原有的打印输出