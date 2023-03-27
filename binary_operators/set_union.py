import click
import pandas as pd
from unary_operators.select import Select


# 使用聯集來取出台灣與中國加起來全部的產品: dataset: products_china.csv, products_taiwan.csv
class Union:
    def __init__(self, columns_and_tablename, path, list_all_csv) -> None:
        self.path = path
        self.list_all_csv = list_all_csv
        self.columns_and_tablename = columns_and_tablename
        self.temp_first_table = []
        self.temp_second_table = []
        self.columns = []
        self.df_first_table = None
        self.df_second_table = None
        self.set_first_table = set()
        self.set_second_table = set()
        self.classifier()
    
    def classifier(self):
        for index, val in enumerate(self.columns_and_tablename):
            if val == 'from':
                self.columns = self.columns_and_tablename[:index]
            elif val == "union":
                self.temp_first_table = self.columns_and_tablename[:index]
                self.temp_second_table = self.columns_and_tablename[index + 2 :]
                print(f"temp_first_table: {self.temp_first_table}")
                print(f"temp_second_table: {self.temp_second_table}")
                break

    def data(self):
        print(f"Union: {self.columns_and_tablename}")
        print(f'path: {self.path}')

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
        