from docx import Document
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)
# 파일 경로 지정
docx_file_path = 'C:/Users/rhksa/Downloads/1.ESG모범규준 개정판(2021.08) - G.docx'  # 파일 경로를 실제 파일의 경로로 변경해야 합니다.
# 함수 호출하여 텍스트 추출
extracted_text = extract_text_from_docx(docx_file_path)
# 추출된 텍스트 출력 또는 다른 용도로 사용
print(extracted_text)

# Specify the file path where you want to save the text file
text_file_path = 'C:/Users/rhksa/Documents/extracted_text-G.txt'  # Change this to your desired file path

# Function to save extracted text to a text file
def save_text_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

# Save the extracted text to a file
save_text_to_file(extracted_text, text_file_path)
