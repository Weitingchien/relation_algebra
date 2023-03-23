import os
import pandas as pd

class Rename:
    def __init__(self, columns_and_tablename, path, list_all_csv) -> None:
        self.old_table_name = ''
        self.new_table_name = ''
        self.path = path()
        self.columns_and_tablename = columns_and_tablename
    def alter(self) -> None:

        print(self.columns_and_tablename)

        
    def columns_and_tablename_filter(self) -> None:
        self.columns_and_tablename = [i.lower() for i in self.columns_and_tablename]
        for index, val in enumerate(self.columns_and_tablename):
            # 去除字串前後的特殊字元
            if self.columns_and_tablename[index] != "*":
                self.columns_and_tablename[index] = re.sub(
                    r"^[^_\w]+|[^_\w]+$", "", self.columns_and_tablename[index]
                ).strip()

            if val == "from":
                index_of_from = index
                self.columns = self.columns_and_tablename[:index_of_from]
                self.tablename.append(self.columns_and_tablename[index+1])
            if val == 'where':
                self.condition = self.columns_and_tablename[index+1:]
                
                
        print(f"columns: {self.columns}")
        print(f"tablename: {self.tablename}")