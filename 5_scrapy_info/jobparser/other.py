# # salary
# salary = item['salary']
# joined_salary = ''.join(salary).replace('\xa0', '')
# numbers_in_sal = re.findall('\d+', joined_salary)

# if joined_salary.find('з/п не указана') != -1:
#     item['min_salary'], item['max_salary'], item['salary_curr'] = None, None, None
# else:
#     if joined_salary.find('от') != -1 and joined_salary.find('до') != -1:
#         item['min_salary'] = int(numbers_in_sal[0])
#         item['max_salary'] = int(numbers_in_sal[1])
#         item['salary_curr'] = salary[5]
#     elif joined_salary.find('от') != -1:
#         item['min_salary'] = int(numbers_in_sal[0])
#         item['max_salary'] = None
#         item['salary_curr'] = salary[3]
#     elif joined_salary.find('до') != -1:
#         item['min_salary'] = None
#         item['max_salary'] = int(numbers_in_sal[0])
#         item['salary_curr'] = salary[3]
#
# # удаляем поле c необработанной зп
# del item['salary']
#
# # employer
# item['employer'] = ''.join(item['employer']).replace('\xa0', ' ')
