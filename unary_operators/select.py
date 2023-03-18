import os
import pandas as pd


class Select:
    def __init__(self, columns_and_tablename, path, list_all_csv) -> None:
        self.columns_and_tablename = columns_and_tablename
        self.path = path()
        self.list_all_csv = list_all_csv
        self.columns = []
        self.tablename = []
        self.columns_and_tablename_filter()

    def show(self) -> list:
        # print(self.list_all_csv)
        if len(self.tablename) < 1:
            return []
        return self.columns_and_tablename

    def columns_and_tablename_filter(self) -> None:
        for index, val in enumerate(self.columns_and_tablename):
            # 去除特殊字元
            self.columns_and_tablename[index] = "".join(
                filter(str.isalnum, self.columns_and_tablename[index])
            )
            if val == "from":
                self.tablename.append(self.columns_and_tablename[-1])
                break
            self.columns.append(self.columns_and_tablename[index])

    def data(self):
        csv_file = [
            i for i in list(self.list_all_csv) if i == self.tablename[0] + ".csv"
        ]
        df = pd.read_csv(self.path + f"\{csv_file[0]}")
        return df
