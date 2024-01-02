import requests
import pandas as pd
import datetime

total_success_request = 0
total_error_requests = 0
# change it to your min questions requirements
min_questions_needed = 25
eligible_candidates = []
invalid_usernames = []
# change it to your month requirements
month = 12 

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
        api_url = f'https://leetcode-stats-api.herokuapp.com/{i}'
        api_data = get_api_data(api_url)
        if api_data:
            if api_data['status'] == 'success':
                data_dict = api_data['submissionCalendar']
                december_submissions = {timestamp: count for timestamp, count in data_dict.items() if datetime.datetime.fromtimestamp(int(timestamp)).month == month}
                total_success_request += 1
                if len(december_submissions) >= min_questions_needed:
                    eligible_candidates.append(i)
            else:
                invalid_usernames.append(i)
                total_error_requests += 1
            

        else:
            invalid_usernames.append(i)
            print('this is working as well ')
            total_error_requests += 1
            

print('eligible_candidates are')
print(eligible_candidates)
print('total_eligible candidates ' ,len(eligible_candidates) )

print('invalid usernames are')
print(invalid_usernames)
    
print('total_success_requests', total_success_request)
print('total_error_requests', total_error_requests)
                
