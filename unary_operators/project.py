import click
import pandas as pd
import operator

class Project:
    def __init__(self, df, condition, df_filter=None) -> None:
        self.df = df
        self.df_filter = df_filter
        self.df_backup = df.copy(deep=True)
        self.columns = []
        self.condition = condition
        self.value = []
        self.current_iteration = 0
        self.max_number_of_comparison_operators = 0
        self.max_number_of_logical_operators = 0
        self.number_of_comparison_operators = 0
        self.number_of_logical_operators = 0
        self.comparison_operator = []
        self.logical_operator = []
        self.operators_map = {'>': operator.gt, '>=': operator.ge, '<': operator.lt, '<=': operator.le, '==': operator.eq, '!=': operator.ne }
        self.temp_index = []
        self.count()
        self.classifier()
    

    def count(self) -> None:
        for index, val in enumerate(self.condition):
            if val == '>' or val == '<' or val == '>=' or val == '<=' or val == '==' or val == '!=':
                self.number_of_comparison_operators += 1
            if val == 'and' or val == 'or':
                self.number_of_logical_operators += 1

        self.max_number_of_comparison_operators = self.number_of_comparison_operators
        self.max_number_of_logical_operators = self.number_of_logical_operators

        print(f'max_number_of_comparison_operators: {self.max_number_of_comparison_operators}')
        print(f'max_number_of_logical_operators: {self.max_number_of_logical_operators}')
    

    def classifier(self) -> None:
        temp_condition = self.condition.copy()
        print(f'condition: {self.condition}')

        # 遞迴中斷條件
        if self.number_of_comparison_operators <= 0:
            return

        for index,val in enumerate(temp_condition):
            if val == '>' or val == '<' or val == '>=' or val == '<=' or val == '==' or val == '!=':
                self.value.append(int(self.condition[2]))
                self.comparison_operator.append(val)
                self.number_of_comparison_operators -= 1
                break
            self.columns.append(val)
            if index == 2:
                break

        self.condition = self.condition[3:]

        for index, val in enumerate(self.condition):
            if val == 'and' or val == 'or':
                self.logical_operator.append(self.condition[index])
                self.condition.pop(0)
                self.number_of_logical_operators -= 1
                break

        self.classifier()

    def data(self):
        print(f'number_of_comparison_operators: {self.number_of_comparison_operators}')
        print(f'number_of_logical_operators: {self.number_of_logical_operators}')
        print(f'comparison_operator: {self.comparison_operator}')
        print(f'logical_operator: {self.logical_operator}')
        print(f'columns: {self.columns}')
        print(f'value: {self.value}')
        if(self.logical_operator[0] == 'and'):
            self.temp_index.clear()

        for index, row in self.df_backup.iterrows():
            if self.operators_map[self.comparison_operator[self.current_iteration]](row[self.columns[self.current_iteration]], self.value[self.current_iteration]):
                self.temp_index.append(index)

        print(f'temp_index: {self.temp_index}')
        # iloc[[]]根據list的索引取(row)資料
        
        if self.current_iteration == self.max_number_of_logical_operators:
            print('迭代完畢')
            #print(f'df_filter: {self.df_filter.shape}')
            #print(f'df: {self.df.shape}')
            if not isinstance(self.df_filter, pd.DataFrame):
                result = self.df.iloc[self.temp_index]
                print(f'欄位不用過濾')
                click.echo(result)
            else:
                print(f'欄位過濾')
                result = self.df_filter.iloc[self.temp_index]
                click.echo(result)

        if self.current_iteration != self.max_number_of_logical_operators:
            if self.logical_operator[0] == 'and':
                self.df_backup = self.df_backup.iloc[self.temp_index]
            elif self.logical_operator[0] == 'or':
                self.df_backup = self.df
            self.current_iteration += 1
            self.data()
        
        