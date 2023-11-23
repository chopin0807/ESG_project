import pandas as pd
import os

# CSV 파일이 있는 폴더
# folder_path = 'C:/Users/rhksa/OneDrive/바탕 화면/ESG_project/기사데이터/우리은행/'
folder_path = './기사데이터/우리은행/' # 프로젝트 폴더(ESG_PROJECT) 내의 최상위 폴더에서 VSCode로 실행해서 파이썬 파일을 실행하면 됩니다.

# 폴더 내의 모든 CSV 파일 목록을 가져옵니다.
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# 모든 CSV 파일을 DataFrame으로 읽어서 리스트에 저장합니다.
dataframes = [pd.read_csv(os.path.join(folder_path, file)) for file in csv_files]

# 모든 데이터프레임을 하나로 합칩니다.
combined_csv = pd.concat(dataframes, ignore_index=True)

combined_csv.to_csv('./기사데이터/우리은행/combined_file.csv', index=False)

