import os

from bs4 import BeautifulSoup

from question import process_question_from_url

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
    contents += process_question_from_url(url)
    with open(os.path.join('answer', file_name), 'w') as f:
        f.write(contents)

def generate_answer():
    soup = get_soup_obj()
    for i in soup.find_all(class_='answerlist-item'):
        process_answerlist_item(i)

if __name__ == '__main__':
    generate_answer()

