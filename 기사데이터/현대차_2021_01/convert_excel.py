import pandas as pd
import os

dir = os.listdir("./")
csv = [file for file in dir if file.endswith(r'.csv')]

for i in csv:
    df = pd.read_csv("./{}".format(i))
    result = df.sample(n = 100)
    result = result.reset_index()
    result.drop(['index', 'media', 'category', 'category_sub'], inplace = True, axis = 1)
    print(result)
    result.to_excel("./엑셀파일/{}.xlsx".format(i.split(".")[0]))