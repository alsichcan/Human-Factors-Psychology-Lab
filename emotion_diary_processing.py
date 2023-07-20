import json
import csv

# CSV Column
COLUMN = ["doc_id", "start_time", "end_time", "age", "gender", "OS", "remote_work", "avoid_contact",
          "family_type", 'family_type_other', "family_number", "income", "education", "education_other",
          "str_q1", "str_q2", "str_q3", "str_q4",
          "lonely_q1", "lonely_q2", "lonely_q3", "lonely_q4", "lonely_q5", "lonely_q6",
          "pers_q1", "pers_q2", "pers_q3", "pers_q4", "pers_q5", "pers_q6", "pers_q7", "pers_q8", "pers_q9", "pers_q10", "pers_q11", "pers_q12",
          "emp_q1", "emp_q2", "emp_q3", "emp_q4", "emp_q5", "emp_q6", "emp_q7", "emp_q8", "emp_q9",
          "day1_title", "day1_contents", "day1_tags_sum", "day1_tags_1", "day1_tags_1_text", "day1_tags_2", "day1_tags_2_text", "day1_tags_3", "day1_tags_3_text", "day1_emo1", "day1_emo1_code", "day1_emo1_text", "day1_emo2", "day1_emo2_code", "day1_emo2_text", "day1_stress", "day1_focus",
          "day2_title", "day2_contents", "day2_tags_sum", "day2_tags_1", "day2_tags_1_text", "day2_tags_2", "day2_tags_2_text", "day2_tags_3", "day2_tags_3_text", "day2_emo1", "day2_emo1_code", "day2_emo1_text", "day2_emo2", "day2_emo2_code", "day2_emo2_text", "day2_stress", "day2_focus",
          "day3_title", "day3_contents", "day3_tags_sum", "day3_tags_1", "day3_tags_1_text", "day3_tags_2", "day3_tags_2_text", "day3_tags_3", "day3_tags_3_text", "day3_emo1", "day3_emo1_code", "day3_emo1_text", "day3_emo2", "day3_emo2_code", "day3_emo2_text", "day3_stress", "day3_focus",
          "day4_title", "day4_contents", "day4_tags_sum", "day4_tags_1", "day4_tags_1_text", "day4_tags_2", "day4_tags_2_text", "day4_tags_3", "day4_tags_3_text", "day4_emo1", "day4_emo1_code", "day4_emo1_text", "day4_emo2", "day4_emo2_code", "day4_emo2_text", "day4_stress", "day4_focus",
          "day5_title", "day5_contents", "day5_tags_sum", "day5_tags_1", "day5_tags_1_text", "day5_tags_2", "day5_tags_2_text", "day5_tags_3", "day5_tags_3_text", "day5_emo1", "day5_emo1_code", "day5_emo1_text", "day5_emo2", "day5_emo2_code", "day5_emo2_text", "day5_stress", "day5_focus"
          ]


# 데이터 읽기
with open('Data.jsonl', 'r') as jsonl_file:
    jsonl_list = list(jsonl_file)

# 데이터 처리
user_keys = list(json.loads(jsonl_list[0]).keys())
user2_keys = list(json.loads(jsonl_list[28613]).keys()) # Key는 같은데 순서만 다른 데이터
diary_keys = list(json.loads(jsonl_list[1]).keys())

data = []
row = 0
while row < len(jsonl_list):
    obj = json.loads(jsonl_list[row])

    # 응답자 정보 처리
    new_user = [f"doc_{len(data)+1}", obj['start_time'], obj['end_time'], obj['age'], obj['gender'], obj['OS'], obj['remote_work'], obj['avoid_contact'],
                obj['family_type'], obj['family_type_other'], obj['family_number'], obj['income'], obj['education'], obj['education_other']]

    # 설문조사 결과 처리
    for survey_type in ['stress', 'lonely', 'personality', 'empathy']:
        for survey_data in obj['survey']:
            if survey_data['type'] == survey_type:
                for k, v in sorted(survey_data['resp'].items()):
                    new_user.append(v)

    # 일기 정보 처리
    diary_data_list = []

    for diary in sorted(obj['diary'], key=(lambda x: x['day'])):
        diary_data = [diary['title'], diary['contents'],
                      diary['emo'][0]['name'], diary['emo'][0]['code'], diary['emo'][0]['text'],
                      diary['emo'][1]['name'], diary['emo'][1]['code'], diary['emo'][1]['text'],
                      diary['task_stress'], diary['task_focus']
                      ]
        diary_data_list.append(diary_data)

    # 태깅 정보 처리
    row += 1
    diary_obj = json.loads(jsonl_list[row])

    while list(diary_obj.keys()) == diary_keys: # Diary에 관한 json 객체일 때
        if obj['taskrunId'] != diary_obj['taskrun_id']:
            raise Exception("User-Diary Match Error")

        for diary in diary_data_list:
            if diary_obj['diary_title'] == diary[0]: # Json객체에 해당하는 Diary를 찾는다
                tag_list = diary_obj['tom_tags'] # 모든 태그들 담는 리스트 객체
                tag_sum = {'Level 1': 0, 'Level 2': 0, 'Level 3': 0} # 공감 수준 별 개수를 집계하기 위한 Dict 객체
                tag_group = [[], [], []] # 공감 수준 별 문장을 넣기 위한 리스트 객체
                tag_group_text = [[], [], []] # 공감 수준 별 문장 텍스트를 넣기 위한 리스트 객체
                for tag in tag_list:
                    level = tag['level']
                    if level == 0:
                        tag_sum = "타인에 대한 언급 없음"
                    else:
                        tag_sum[f"Level {level}"] += 1
                        tag_group[level-1].append(tag)
                        tag_group_text[level-1].append(tag['span_text'])
                diary.insert(2, tag_sum)
                for i in range(len(tag_group)):
                    if len(tag_group[i]) == 0:
                        diary.insert(3+2*i, "")
                        diary.insert(4+2*i, "")
                    else:
                        diary.insert(3+2*i, tag_group[i])
                        diary.insert(4+2*i, tag_group_text[i])

        row += 1
        if row < len(jsonl_list):
            diary_obj = json.loads(jsonl_list[row])
        else:
            break

    for diary_data in diary_data_list:
        new_user += diary_data
    data.append(new_user)

# 데이터 쓰기
with open('Result.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(COLUMN)
    for line in data:
        writer.writerow(line)
