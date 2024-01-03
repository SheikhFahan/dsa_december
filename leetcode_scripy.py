import requests
import pandas as pd
import datetime

# change it to your min questions requirements
min_days_needed = 25
eligible_candidates = []
invalid_usernames = []
# change it to your month requirements
month = 12 
ineligible_students = 0

def get_column_data(file_path, sheet_name, column_name):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        column_data = df[column_name].tolist()
        return column_data
    except Exception as e:
        print(f"Error: {e}")
        return None
# change file path to your file path
file_path = '/home/e-lec-tron/Downloads/DSA-DECEMBER (Responses).xlsx'
# change sheetname to your sheet name
sheet_name = 'sheet1'
# change column_name to your column name containing the leedcode_ids
column_name = 'LEETCODE ID'
candidate_name = get_column_data(file_path, sheet_name, column_name)

def find_rows_by_values_and_save(file_path, sheet_name, column_name, target_values, output_file):
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        result_rows = pd.DataFrame()

        # Iterate through each target value i.e list of eligible students
        for target_value in target_values:
            # Find the row where the specified column has the target value
            target_row = df[df[column_name] == target_value]

            # Append the result to the overall DataFrame
            # result_rows = result_rows.append(target_row, ignore_index=True)
            # df =     pd.DataFrame(df).append(new_row, ignore_index=True)
            result_rows = pd.concat([result_rows, target_row], ignore_index=True)


        # Save the result to a new Excel file
        result_rows.to_excel(output_file, index=False)
        print(f"Result saved to {output_file}")

        return result_rows

    except Exception as e:
        print(f"Error: {e}")
        return None


def get_api_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        data = response.json()  
        return data
    except requests.exceptions.RequestException as e:
        # print(f"Error fetching data from API: {e}")
        return None


if candidate_name:
    for i in candidate_name:
        count = 0
        # run the api a few times just to be sure
        api_url = f'https://leetcode-stats-api.herokuapp.com/{i}'
        api_data = get_api_data(api_url)
        if api_data:
            if api_data['status'] == 'success':
                data_dict = api_data['submissionCalendar']
                
                december_submissions = {timestamp: count for timestamp, count in data_dict.items() if datetime.datetime.fromtimestamp(int(timestamp)).month == month}
                # some students were missing by a day or two -> to filter them out for a second chance
                if len(december_submissions) >= 23 and len(december_submissions) <25:
                    print(f'{i}  missed by ', 25 -len(december_submissions), " day(s)" )

                if len(december_submissions) >= min_days_needed:
                    eligible_candidates.append(i)

                if len(december_submissions) < 25:
                    ineligible_students +=1

            else:
                invalid_usernames.append(i)
        else:
            print('something wrong with ', {i})
            

print('eligible_candidates are:', )
print(eligible_candidates)

print('invalid usernames are')
print(invalid_usernames)

print('total_eligible candidates are' ,len(eligible_candidates) )
print('in-eligible candidates are ', ineligible_students)
print('total error requests are ', len(invalid_usernames))

print('total entries in the form are ',len(eligible_candidates) + ineligible_students + len(invalid_usernames))

find_rows_by_values_and_save(file_path = file_path,sheet_name = sheet_name, column_name = column_name, target_values = eligible_candidates, output_file = 'final_list.xlsx')
