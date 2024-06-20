input_correct_data = [
    {'question_id': 22098, 'question_name': 'Квалификация лида', 'answer_id': 24014920, 'answer_values': ['ЮЛ+ГЕО']},
    {'question_id': 22097, 'question_name': 'Тип лида', 'answer_id': 24014919, 'answer_values': ['ипотека']},
    {'question_id': 22096, 'question_name': 'Комментарий к лиду', 'answer_id': 24014918, 'answer_values': ['1111']},
    {'question_id': 22095, 'question_name': 'Имя лида', 'answer_id': 24014917, 'answer_values': ['1111']}]

output_correct_data = '''Квалификация лида
ЮЛ+ГЕО

Тип лида
ипотека

Комментарий к лиду
1111

Имя лида
1111'''

input_data_without_question_name = [
    {'question_id': 22098, 'answer_id': 24014920, 'answer_values': ['ЮЛ+ГЕО']},
    {'question_id': 22097, 'answer_id': 24014919, 'answer_values': ['ипотека']},
    {'question_id': 22096, 'answer_id': 24014918, 'answer_values': ['1111']},
    {'question_id': 22095, 'answer_id': 24014917, 'answer_values': ['1111']}]

output_data_without_question_name = '''
ЮЛ+ГЕО


ипотека


1111


1111'''


input_data_without_answer_values = [
    {'question_id': 22098, 'question_name': 'Квалификация лида', 'answer_id': 24014920, },
    {'question_id': 22097, 'question_name': 'Тип лида', 'answer_id': 24014919, },
    {'question_id': 22096, 'question_name': 'Комментарий к лиду', 'answer_id': 24014918, },
    {'question_id': 22095, 'question_name': 'Имя лида', 'answer_id': 24014917, }]

output_data_without_answer_values = '''Квалификация лида


Тип лида


Комментарий к лиду


Имя лида
'''

input_empty_data = []
output_empty_data = ''
