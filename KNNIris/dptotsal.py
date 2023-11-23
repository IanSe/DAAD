import pandas as pd

def top_three_salaries(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    tmp = ans = pd.DataFrame({'Department' : [], 'Employee' : [], 'Salary' : []})
    if(employee.empty or department.empty): return tmp
    for i in range(len(employee)):
        ans = pd.concat([ans, pd.DataFrame({'Department' : [department.loc[department['id'] == employee['departmentId'][i], 'name'].iloc[0]], 
                                            'Employee' : [employee['name'][i]],
                                            'Salary' : [int(employee['salary'][i])]})], ignore_index=True)
    ans.sort_values(by=['Salary'], inplace=True, ascending=False)
    ans.sort_values(by=['Department'], inplace=True, ascending=True)
    ans.reset_index(inplace=True)
    for i in range(0, len(department)):
        nrows = ans.loc[ans['Department'] == department['name'][i],'Salary'].drop_duplicates(keep='first').index
        rows = nrows[0:3]
        tmp = pd.concat([tmp, pd.DataFrame({'Department' : ans['Department'][rows[0]:rows[-1]+1], 
                                            'Employee' : ans['Employee'][rows[0]:rows[-1]+1],
                                            'Salary' : ans['Salary'][rows[0]:rows[-1]+1]})], ignore_index=True)
    return tmp

employee = pd.DataFrame({'id' : [1, 4], 
                         'name' : ['Joe', 'Max'], 
                         'salary' : [85000, 85000], 
                         'departmentId' : [1, 1]})
department = pd.DataFrame({'id' : [1], 'name' : ['IT']})

print(top_three_salaries(employee, department))