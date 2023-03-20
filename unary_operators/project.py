import pandas as pd
import operator

class Project:
    def __init__(self, df, condition) -> None:
        self.df = df
        self.df_backup = self.df
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
        self.operators_map = {'>': operator.gt, '>=': operator.ge, '<': operator.lt, '<=': operator.le }
        self.count()
        self.classifier()
    
    def show(self) -> None:
        print(self.condition)

    def count(self) -> None:
        for index, val in enumerate(self.condition):
            if val == '>' or val == '<' or val == '>=' or val == '<=':
                self.number_of_comparison_operators += 1
            if val == 'AND' or val == 'OR':
                self.number_of_logical_operators += 1

        self.max_number_of_comparison_operators = self.number_of_comparison_operators
        self.max_number_of_logical_operators = self.number_of_logical_operators

        print(f'max_number_of_comparison_operators: {self.max_number_of_comparison_operators}')
        print(f'max_number_of_logical_operators: {self.max_number_of_logical_operators}')
    

    def classifier(self) -> None:
        print(f'(first): {self.condition}')
        if self.number_of_comparison_operators <= 0:
            return

        for index,val in enumerate(self.condition):
            print(f'(outside)val: {val}')
            if val == '>' or val == '<' or val == '>=' or val == '<=' :
                print(f'(inner)val, index: {val, index}')
                print(f'number: {self.condition[index+1]}')
                self.value.append(int(self.condition[index+1]))
                print(f'(inner)values: {self.value} ')
                self.comparison_operator.append(val)
                self.number_of_comparison_operators -= 1
                self.condition.pop(index)
                self.condition.pop(index+1)
                print(f'(inner)condition: {self.condition}')
                break
            self.columns.append(val)
            self.condition.pop(index)
        print(f'condition: {self.condition}')

        for index, val in enumerate(self.condition):
            if val == 'AND' or val == 'OR':
                self.logical_operator.append(self.condition[index])
                self.condition.pop(index)
                self.number_of_logical_operators -= 1

        #self.classifier()

    def data(self) -> None:
        print(f'logical_operator: {self.logical_operator}')
        print(f'comparison_operator: {self.comparison_operator}')
        print(f'Project_columns: {self.columns}')
        print(f'value: {self.value}')
        """
        temp_index = []

        for index, row in self.df_backup.iterrows():
            if self.operators_map[self.comparison_operator[self.current_iteration]](row[self.columns[self.current_iteration]], self.value[self.current_iteration]):
                temp_index.append(index)
                #print(row[self.columns[0]])
        if self.current_iteration != self.max_number_of_logical_operators:
            self.df_backup = self.df_backup.iloc[temp_index]
            self.current_iteration += 1
            self.data()

        
        print(f'temp_index: {temp_index}')
        # iloc[[]]根據list的索引取(row)資料
        #print(self.df_backup.iloc[temp_index])
        return self.df_backup.iloc[temp_index]
        
        #print(df_new)
        """
        