import os
import pdb
import imghdr

from bs4 import BeautifulSoup
import requests
import shutil

username = '丰赵'
base_url = 'https://zhidao.baidu.com'

def process_question_from_str(st, folder):
    soup = BeautifulSoup(st)
    if soup.title.text.find('信息提示') > 0:
        return 'deleted'
    try:
        question = soup.find(class_='q-content').find_all('span')[1]
    except Exception as e:
        # account deleted, use title instead
        question = soup.find('title')
    question_text = question.text.rstrip('_百度知道')
    try:
        question_img = soup.find(class_='q-img-ul').find('img')
        if question_img:
            img_url = question_img['src']
            img_name = download_image(img_url, folder)
            if img_name is not None:
                question_text += '\n![](%s)\n' % img_name
    except AttributeError:
        pass

    # whether I am the best replier
    repliers = soup.find_all(class_='wgt-replyer-all-card')
    # find my replier index    
    index = 0
    for i in repliers:
        if i.text.find(username) > 0:
            break
        index += 1

    if index == len(repliers):
        my_answer = soup.find(class_='best-text') # I do not answer this question
    elif index == 0:
        my_answer = soup.find(class_='best-text')
        if my_answer is None:
            my_answer = soup.find(class_='answer-text')
    else:
        index -= 1
        my_answer = soup.find_all(class_='answer-text')[index]

    if my_answer is None:
        my_answer_text = ''
    else:
        my_answer_text = my_answer.text.replace('展开全部','')
        my_answer_text = my_answer_text.replace('\n\n\n','')
        answer_img = my_answer.find('img')
        if answer_img:
            img_url = answer_img['src'].split('?')[0]
            img_name = download_image(img_url, folder)
            my_answer_text += '\n![](%s)\n' % img_name
    return question_text + '\n\n' + my_answer_text

def download_image(img_url, folder):
    img_name_first_part = img_url.split('/')[-1]
    file_name = os.path.join('build', img_name_first_part)
    if not os.path.exists(file_name):
        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            print("Download for %s failed" % img_url)
    img_ext = imghdr.what(file_name)
    if img_ext is None:
        return None
    img_name = img_name_first_part + '.' + img_ext
    new_file = os.path.join(folder, img_name)
    shutil.copy(file_name, new_file)
    return img_name

def process_question_from_file(file_name, folder):
    with open(file_name) as f:
        st = f.read()
    return process_question_from_str(st, folder)
 
def process_question_from_url(url, folder):
    question_id = url.split('/')[-1]
    file_name = os.path.join('build', question_id + '.html')
    if not os.path.exists(file_name):
        whole_url = base_url + url
        r = requests.get(whole_url)
        if r.status_code != 200:
            pdb.set_trace()
        r.encoding = 'gbk'
        with open(file_name, 'w') as f:
            f.write(r.text)
    return process_question_from_file(file_name, folder)
    
