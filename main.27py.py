import pandas as pd

# 读取之前保存的 Excel 文件
input_path = "/Users/liuchengjie/Downloads/merged_data_with_cons_vote_share.dta"
data = pd.read_stata(input_path)
print(data.columns)

# 创建年份映射字典
year_mapping = {'1955': 1955, '1959': 1959, '1964': 1964, '1966': 1966, '1970': 1970, '1974F': 1974, '1974O': 1975, '1979': 1979, '1983': 1983, '1987': 1987, '1992': 1992, '1997': 1997, '2001': 2001, '2005':2005, '2010': 2010, '2015': 2015, '2017': 2017, '2019': 2019}

# 将年份转换为整数类型
data['Year'] = data['Year'].map(year_mapping)

# 对数据按选区和年份排序
data = data.sort_values(by=['Constituency', 'Year'])

# 创建新变量：各个选区保守党的 t-1 期得票率
data['ConsVoteshareBack1'] = data.groupby('Constituency')['Conservative_Vote_Share_100'].shift(1)

# 创建新变量：各个选区保守党的 t-2 期得票率
data['ConsVoteshareBack2'] = data.groupby('Constituency')['Conservative_Vote_Share_100'].shift(2)

# 删除包含空白数据的行
data = data.dropna(subset=['ConsVoteshareBack1', 'ConsVoteshareBack2'])

# 将结果保存到新的 Excel 文件
output_path = "/Users/liuchengjie/Downloads/Constituency_Conservative_Vote_Share_with_t1_t2.xlsx"
data.to_excel(output_path, index=False)


import pandas as pd

# 读取ConsVoteshareBack1和ConsVoteshareBack2数据
cons_vote_share_path = "/Users/liuchengjie/Downloads/Constituency_Conservative_Vote_Share_with_t1_t2.xlsx"
cons_vote_share_data = pd.read_excel(cons_vote_share_path)

cons_vote_share_data['ConsVoteshareBack1'] = pd.to_numeric(cons_vote_share_data['ConsVoteshareBack1'], errors='coerce')
cons_vote_share_data['ConsVoteshareBack2'] = pd.to_numeric(cons_vote_share_data['ConsVoteshareBack2'], errors='coerce')

# 仅选择需要合并的列
cons_vote_share_data = cons_vote_share_data[['Constituency', 'Year', 'ConsVoteshareBack1', 'ConsVoteshareBack2']]

# 读取现有数据集
merged_data_path = "/Users/liuchengjie/Downloads/merged_data_with_cons_vote_share.dta"
merged_data = pd.read_stata(merged_data_path)
merged_data['Year'] = merged_data['Year'].map(year_mapping)

# 根据["Constituency", "Year"]列合并数据集
merged_data = pd.merge(merged_data, cons_vote_share_data, on=["Constituency", "Year"], how="left")



# 将合并后的数据集保存为.dta文件
output_path = "/Users/liuchengjie/PycharmProjects/pythonProject22/merged_data_3_cov.dta"
merged_data.to_stata(output_path, write_index=False)
print(merged_data.columns)


