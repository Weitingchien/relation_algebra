import re
import pandas as pd
from unary_operators.project import Project


class Select:
    def __init__(self, columns_and_tablename, path, list_all_csv) -> None:
        self.columns_and_tablename = columns_and_tablename
        self.path = path()
        self.list_all_csv = list_all_csv
        self.columns = []
        self.tablename = []
        self.condition = []
        self.columns_and_tablename_filter()

    def columns_and_tablename_filter(self) -> None:
        for index, val in enumerate(self.columns_and_tablename):
            # 去除字串前後的特殊字元
            if self.columns_and_tablename[index] != "*":
                self.columns_and_tablename[index] = re.sub(
                    r"^[^_\w]+|[^_\w]+$", "", self.columns_and_tablename[index]
                ).strip()

            if val == "from":
                index_of_from = index
                self.columns = self.columns_and_tablename[:index_of_from]
                self.tablename.append(self.columns_and_tablename[index + 1])
            if val == "where":
                self.condition = self.columns_and_tablename[index + 1 :]

        print(f"columns: {self.columns}")
        print(f"tablename: {self.tablename}")

    # 回應使用者指定的columns, table資料
    def data(self):
        csv_file = [
            i for i in list(self.list_all_csv) if i == self.tablename[0] + ".csv"
        ]

        df = pd.read_csv(self.path + f"\{csv_file[0]}")

        if self.columns[0] == "*" and len(self.condition) <= 0:
            print("select(1)")
            return df

        elif self.columns[0] == "*" and len(self.condition) > 0:
            print("select(2)")
            project = Project(df, self.condition)
            result = project.data()
            return result

        elif self.columns[0] != "*" and len(self.condition) <= 0:
            print("select(3)")
            df_filter = df.loc[:, [i for i in self.columns]]
            return df_filter

        else:
            print("select(4)")
            df_filter = df.loc[:, [i for i in self.columns]]
            project = Project(df, self.condition, df_filter)
            result = project.data()
            return result
