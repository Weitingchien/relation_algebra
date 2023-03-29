import pandas as pd
from unary_operators.select import Select
from binary_operators.set_union import Union

# select P_Name FROM products_china intersect select P_Name FROM products_taiwan
class Intersection(Union):
    def __init__(self, columns_and_tablename, path, list_all_csv) -> None:
        super().__init__(columns_and_tablename, path, list_all_csv)


    def classifier(self) -> None:
        for index, val in enumerate(self.columns_and_tablename):
            if val == 'from':
                self.columns = self.columns_and_tablename[:index]
            elif val == "intersect":
                self.temp_first_table = self.columns_and_tablename[:index]
                self.temp_second_table = self.columns_and_tablename[index + 2 :]
                print(f"temp_first_table: {self.temp_first_table}")
                print(f"temp_second_table: {self.temp_second_table}")
                break

    def data(self):
        print(f"intersect: {self.columns_and_tablename}")
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

        # 差集
        result = self.set_first_table.intersection(self.set_second_table)
        return pd.DataFrame({self.df_first_table.columns[0]: list(result)})