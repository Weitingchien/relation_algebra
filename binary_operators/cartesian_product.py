import itertools
import numpy as np
import pandas as pd
from binary_operators.set_union import Union



# select customers.Name, orders.Order_No FROM customers CROSS JOIN orders

class Cartesian(Union):
    def __init__(self, columns_and_tablename, path, list_all_csv) -> None:
        super().__init__(columns_and_tablename, path, list_all_csv)
        self.tablename = self.temp_first_table + self.temp_second_table
        self.path = path()
        self.first_df = None
        self.second_df = None
        self.columns_name = []


    def classifier(self) -> None:
        print(f'self.columns_and_tablename: {self.columns_and_tablename}')
        
        for index, val in enumerate(self.columns_and_tablename):
            if val == 'from':
                self.columns = self.columns_and_tablename[:index]
                self.temp_first_table = [self.columns_and_tablename[index+1]]
            elif val == "join":
                self.temp_second_table = [self.columns_and_tablename[index+1]]
                print(f"temp_first_table: {self.temp_first_table}")
                print(f"temp_second_table: {self.temp_second_table}")
                break
        print(f'columns: {self.columns}')

    def data(self):

        # 欄位名稱與值對齊
        pd.set_option('display.unicode.ambiguous_as_wide', True)
        pd.set_option('display.unicode.east_asian_width', True)

        csv_file = [
            f'{self.tablename[i]}.csv'
            for i, j in itertools.product(range(2), list(self.list_all_csv))
            if j == f'{self.tablename[i]}.csv'
        ]

        self.first_df = pd.read_csv(self.path + f"\{csv_file[0]}")
        self.second_df = pd.read_csv(self.path + f"\{csv_file[1]}")
        
        # 取得欄位的所有值，不包括欄位名稱
        first_df_values = self.first_df[:].values
        second_df_values = self.second_df[:].values

        temp = []
        
        for i in range(len(first_df_values)):
            for j in range(len(second_df_values)):
                temp.append(np.append(first_df_values[i], second_df_values[j]))

        # 合併兩個csv檔案的欄位名稱
        self.columns_name = self.first_df.columns.tolist() + self.second_df.columns.tolist()

        for index, val in enumerate(self.columns_name):
            if index >= (len(self.first_df.columns)):
                self.columns_name[index] = f'{self.temp_second_table[0]}.{val}'
            else:
                self.columns_name[index] = f'{self.temp_first_table[0]}.{val}'

        df = pd.DataFrame(data=temp, columns=self.columns_name)

        filter_columns = [] # 找出int64的欄位(用這欄位來作後面的由小到大排序)

        for index,val in enumerate(self.columns):
            if df[val].dtype == 'int64':
                filter_columns.append(val)

        # 由小到大
        df.sort_values(by=filter_columns, inplace=True)

        result = df[self.columns]
        # 重設index
        result.reset_index(drop=True, inplace=True)

        temp_result_columns = []

        # 移除掉之前欄位的標記(標記主要是區隔欄位在哪個csv檔案)
        for index, val in enumerate(result.columns):
            temp_result_columns.append(val.split('.')[1])

        result.columns = temp_result_columns

        return result











        """
        for index in range(2):
            if index == 0:
                select = Select(self.temp_first_table, self.path, self.list_all_csv)
                self.df_first_table = select.data()
            else:
                select = Select(self.temp_second_table, self.path, self.list_all_csv)
                self.df_second_table = select.data()

        for i in self.df_first_table[self.df_first_table.columns[0]]:
            self.set_first_table.add(i)
        for i in self.df_second_table[self.df_second_table.columns[0]]:
            self.set_second_table.add(i)
        
        result = self.set_first_table.union(self.set_second_table)
        return pd.DataFrame({self.df_first_table.columns[0]: list(result)})
        """