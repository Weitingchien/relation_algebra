import re
import os
import click
import pandas as pd

# 更改column名稱: alter TABLE classroom RENAME COLUMN building TO building_a
# 更改table名稱: alter TABLE classroom RENAME TO classroom_a
class Rename:
    def __init__(self, columns_and_tablename, path, list_all_csv) -> None:
        self.list_all_csv = list_all_csv
        self.old_table_name = ''
        self.new_table_name = ''
        self.old_column_name = ''
        self.new_column_name = ''
        self.path = path()
        self.columns_and_tablename = columns_and_tablename
        self.columns_and_tablename_filter()
    
    def alter_column(self) -> None:
        print('alter_column')
        csv_file = [
            i for i in list(self.list_all_csv) if i == f'{self.old_table_name}.csv'
        ]
        df = pd.read_csv(self.path + f"\{csv_file[0]}")
        df.rename(columns={self.old_column_name: self.new_column_name}, inplace=True)
        df.to_csv(self.path + f"\{csv_file[0]}", index=False)
        click.echo(f"Column {self.old_column_name} renamed to {self.new_column_name}.")

    
    def alter_table(self) -> None:
        print('alter_table')
        print(f'old_column_name: {self.old_column_name}')
        print(f'new_column_name: {self.new_column_name}')

        if len(self.old_column_name) > 0 and len(self.new_column_name) > 0:
            self.alter_column()

        # copilot
        if len(self.old_table_name) < 1 or len(self.new_table_name) < 1:
            return
        
        csv_file = [
            i for i in list(self.list_all_csv) if i == f'{self.old_table_name}.csv'
        ]
        os.rename(self.path + f"\{csv_file[0]}", self.path + f"\{self.new_table_name}.csv")
        click.echo(f"Table {self.old_table_name} renamed to {self.new_table_name}.")

    def columns_and_tablename_filter(self) -> None:
        for index, val in enumerate(self.columns_and_tablename):
            # 去除字串前後的特殊字元
            if self.columns_and_tablename[index] != "*":
                self.columns_and_tablename[index] = re.sub(
                    r"^[^_\w]+|[^_\w]+$", "", self.columns_and_tablename[index]
                ).strip()

            if val == "table":
                self.old_table_name = self.columns_and_tablename[index+1]
            if val == 'column':
                self.old_column_name = self.columns_and_tablename[index+1]
                self.new_column_name = self.columns_and_tablename[index+3]
                return
            if val == 'to':
                self.new_table_name = self.columns_and_tablename[index+1]
                
            