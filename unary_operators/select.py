import re
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
        if len(self.tablename) < 1:
            return []
        return self.columns_and_tablename

    def columns_and_tablename_filter(self) -> None:
        for index, val in enumerate(self.columns_and_tablename):
            # 去除字串前後的特殊字元
            if self.columns_and_tablename[index] != "*":
                self.columns_and_tablename[index] = re.sub(
                    r"^[^_\w]+|[^_\w]+$", "", self.columns_and_tablename[index]
                ).strip()
            if val == "from":
                self.tablename.append(self.columns_and_tablename[-1])
                break
            self.columns.append(self.columns_and_tablename[index])
        print(f"columns: {self.columns}")
        print(f"tablename: {self.tablename}")

    # 回應使用者指定的columns, table資料
    def data(self):
        csv_file = [
            i for i in list(self.list_all_csv) if i == self.tablename[0] + ".csv"
        ]

        df = pd.read_csv(self.path + f"\{csv_file[0]}")

        if self.columns[0] == "*":
            return df
        else:
            df = df.loc[:, [i for i in self.columns]]
            return df
