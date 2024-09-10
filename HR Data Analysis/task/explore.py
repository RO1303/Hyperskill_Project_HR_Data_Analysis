import pandas as pd
import requests
import os


# scroll down to the bottom to implement your solution

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
            'B_office_data.xml' not in os.listdir('../Data') and
            'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    # write your code here
    a_office_data = pd.read_xml("../Data/A_office_data.xml")
    b_office_data = pd.read_xml("../Data/B_office_data.xml")
    hr_data = pd.read_xml("../Data/hr_data.xml")

    a_office_data.index = "A" + a_office_data.employee_office_id.astype(str)
    b_office_data.index = "B" + b_office_data.employee_office_id.astype(str)
    hr_data.index = hr_data.employee_id

    ab_office_data = pd.concat([a_office_data, b_office_data])
    office_and_hr_data = ab_office_data.merge(hr_data, how="inner", left_index=True, right_index=True, indicator=True)
    office_and_hr_data = office_and_hr_data.drop(columns=["employee_id", "employee_office_id", "_merge"])
    office_and_hr_data = office_and_hr_data.sort_index()

    # Step 5
    pivoted1 = office_and_hr_data.pivot_table(index = "Department", columns=["left", "salary"],
                                             values="average_monthly_hours", aggfunc="median")
    #print(pivoted1.head())
    #print(pivoted1.columns)
    res1 = pivoted1[(pivoted1[(0,'high')] < pivoted1[(0,'medium')]) | (pivoted1[(1,'low')] < pivoted1[(1,'high')])]
    #print(res.head())

    pivoted2 = office_and_hr_data.pivot_table(index = "time_spend_company", columns="promotion_last_5years",
                                             values=["satisfaction_level", "last_evaluation"],
                                             aggfunc=["min", "max", "mean"])
    #print(pivoted2.head())
    #print(pivoted2.columns)
    res2 = pivoted2[pivoted2[('mean', 'last_evaluation', 0)] > pivoted2[('mean', 'last_evaluation', 1)]]
    print(res1.round(2).to_dict())
    print(res2.round(2).to_dict())

"""
    # Step 4
    def count_bigger_5(series):
        return len(series[series > 5])

    office_and_hr_data = office_and_hr_data[
        ["left", "number_project", "time_spend_company", "Work_accident", "last_evaluation"]]
    agg_dict = {"number_project": ["median", count_bigger_5],
                "time_spend_company": ["mean", "median"],
                "Work_accident": ["mean"],
                "last_evaluation": ["mean", "std"]}
    print(office_and_hr_data.groupby("left").agg(agg_dict).round(2).to_dict())
"""

"""
    # Step 3    
    office_and_hr_data = office_and_hr_data.sort_values("average_monthly_hours", ascending=False)
    print(list(office_and_hr_data.head(10).Department))
    print(office_and_hr_data.query("Department=='IT' and salary=='low'").number_project.sum())
    employees_wanted = ["A4", "B7064", "A3033"]
    res = office_and_hr_data.loc[employees_wanted, ["last_evaluation", "satisfaction_level"]]
    print(res.values.tolist())
"""
