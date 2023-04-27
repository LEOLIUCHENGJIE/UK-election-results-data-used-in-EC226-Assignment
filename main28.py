import pandas as pd

# 读取Excel文件
file_path = "/Users/liuchengjie/Downloads/1918-2019election_results_by_pcon 2.xlsx"
xls = pd.ExcelFile(file_path)

# 指定年份
years = ['1955', '1959', '1964', '1966', '1970', '1974F', '1974O', '1979', '1983', '1987', '1992', '1997', '2001',
         '2005', '2010', '2015', '2017', '2019']

# 提取各年份的Electorate数据
data_list = []
for year in years:
    df = pd.read_excel(xls, sheet_name=str(year), header=None, skiprows=1)

    # 根据年份选择正确的Electorate列
    if year in ['1955', '1959', '1964', '1966', '1970', '1974F', '1979', '1983', '1987', '1992']:
        electorate_col = 5
    else:
        electorate_col = 6

    # 提取选区和Electorate数据
    data = df.loc[:, [2, electorate_col]]
    data.columns = ['Constituency', 'Electorate']
    data['Year'] = year

    data_list.append(data)

# 合并所有年份的数据
combined_data = pd.concat(data_list)

combined_data.dropna(subset=['Constituency', 'Electorate'], inplace=True)

# 读取现有数据集
election_data_path = "/Users/liuchengjie/PycharmProjects/pythonProject22/processed_data_no_zero1.xlsx"
election_data = pd.read_excel(election_data_path)

# 删除保守党得票率为0的选区数据
election_data = election_data[election_data[''] != 0]

# 根据["Constituency", "Year"]列合并数据集
merged_data = pd.merge(election_data, combined_data, on=["Constituency", "Year"], how="left")

merged_data['Electorate'] = pd.to_numeric(merged_data['Electorate'], errors='coerce')

# 保存结果到新的Excel文件
output_path = "/Users/liuchengjie/Downloads/covariate_data.xlsx"
combined_data.to_excel(output_path, index=False)

# 将合并后的数据集保存为.dta文件
output_path = "/Users/liuchengjie/PycharmProjects/pythonProject22/merged_data.dta"
merged_data.to_stata(output_path, write_index=False)

