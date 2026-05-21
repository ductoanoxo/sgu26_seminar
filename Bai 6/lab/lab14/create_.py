import pandas as pd
import numpy as np

# Tạo mảng 10,000 x 10,000 số thực
data = np.random.rand(10000, 10000)
df = pd.DataFrame(data)
df.to_csv('interactions_10_000.csv', index=False)
print("Đã tạo xong file CSV mẫu!")