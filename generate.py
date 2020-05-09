import os
import argparse
import json

from bs4 import BeautifulSoup

from question import process_question_from_url

ANSWER_FOLDER = 'answer'
QUESTION_FOLDER = 'questions'

def get_soup_obj():
    if not os.path.exists('answer'):
        os.mkdir('answer')
    with open('list.html') as f:
        st = f.read()
    soup = BeautifulSoup(st)
    return soup

def process_answerlist_item(item):
    title = item.find(class_='list-title').text
    if len(title) > 10:
        title_short = title[:10]
    else:
        title_short = title
    createtime = item.find(class_='createtime').text
    url = item.a['href']
    file_name = createtime + '_' + title_short + '.md'
    contents = ''
    contents += '# ' + title + '\n'
    contents += createtime + '\n\n'
    contents += process_question_from_url(url, ANSWER_FOLDER)
    with open(os.path.join(ANSWER_FOLDER, file_name), 'w') as f:
        f.write(contents)

def process_questionlist_item(item):
    title = item['title']
    if len(title) > 10:
        title_short = title[:10]
    else:
        title_short = title
    createtime = item['createTime']
    url = '/question/' + item['qid']
    file_name = createtime + '_' + title_short + '.md'
    contents = ''
    contents += '# ' + title + '\n'
    contents += createtime + '\n\n'
    contents += process_question_from_url(url, QUESTION_FOLDER)
    with open(os.path.join(QUESTION_FOLDER, file_name), 'w') as f:
        f.write(contents)
   
def generate_questions():
    json_file_list = os.listdir('./')
    for file_name in json_file_list:
        if file_name.find('.json') < 0:
            continue
        f = open(file_name)
        js = json.load(f)
        for i in js['data']['question']['list']:
            process_questionlist_item(i)

def generate_answer():
    soup = get_soup_obj()
    for i in soup.find_all(class_='answerlist-item'):
        process_answerlist_item(i)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', choices=['generate_answer', 'generate_questions'],
        default='generate_answer')
    args = parser.parse_args()
    if args.action == 'generate_answer':
        generate_answer()
    elif args.action == 'generate_questions':
        generate_questions()

