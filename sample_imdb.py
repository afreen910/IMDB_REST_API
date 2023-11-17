from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from time import sleep
from selenium.webdriver.common.by import By
import json

service = Service(executable_path='/Users/rzameer/Downloads/geckodriver')
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(service=service, options=options)


all_movies = []
urls='https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=101&ref_=adv_nxt'
url_list=[]
num = 101
for i in range(101,1001,100):
    url_list.append(f'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start={i}&ref_=adv_nxt')



def find_movies():
    for card in driver.find_elements(By.CLASS_NAME, 'lister-item.mode-advanced'):
        movie = {}
        movie_name_header = card.find_element(By.CLASS_NAME, 'lister-item-header')
        movie['name'] = movie_name_header.find_element(By.TAG_NAME, 'a').text
        movie['url'] = movie_name_header.find_element(By.TAG_NAME, 'a').get_attribute('href')
        movie['movie_id'] = movie['url'].split('/')[4]
        print(movie,'\n')
        all_movies.append(movie)


def next_click():
    try:
        next_button = driver.find_element(By.CLASS_NAME,'lister-page-next.next-page').get_attribute('href')
        # Click the next button
        driver.get(next_button)
        print('NEXT clicked')
        return True
    except Exception as e:
        print(e)
        return False

def movie_details(level_1_dict):
    """
    {"cast": [{"actor": "Tim", "role": "andy"}, {"actor": "Morgan", "role": "Ellis"}],
    "director": ["stephen", "frank"],
    "writers": ["Stephen","frank"],
    "user_reviews":114,
    "critic_reviews":174
    "nominations":42,
    "awards":21,
    "movie_name":"The Shawshank Redemption",
    "url": ,
    movie_id='t66565'
    }
    """

    url = level_1_dict['url']
    driver.get(url)
    sleep(0.5)
    movie_details = {}
    movie_details['movie_name'] = level_1_dict['name']
    movie_details['url'] = url
    movie_details['movie_id'] = level_1_dict['movie_id']

    all_cast = []
    for actors in driver.find_elements(By.CLASS_NAME, 'sc-bfec09a1-5.kUzsHJ'):
        actor_header = actors.find_element(By.CLASS_NAME, 'sc-bfec09a1-7.dpBDvu')
        actor={}
        actor['actor_name'] = actor_header.find_element(By.TAG_NAME,'a').text
        actor['role'] = actor_header.find_element(By.CLASS_NAME, 'title-cast-item__characters-list').text
        all_cast.append(actor)
    movie_details['cast'] = all_cast
    director=[]
    writers = []
    stars = []
    top_dir_wr_star = driver.find_element(By.CLASS_NAME,
                        'ipc-metadata-list.ipc-metadata-list--dividers-all.title-pc-list.ipc-metadata-list--baseAlt')
    directors_tag = top_dir_wr_star.find_elements(By.CLASS_NAME, 'ipc-metadata-list__item')[0]
    for el in directors_tag.find_elements(By.CLASS_NAME, 'ipc-inline-list__item'):
        director.append(el.text)

    writer_tag = top_dir_wr_star.find_elements(By.CLASS_NAME, 'ipc-metadata-list__item')[1]
    for el in writer_tag.find_elements(By.CLASS_NAME, 'ipc-inline-list__item'):
        writers.append(el.text)

    stars_tag = top_dir_wr_star.find_elements(By.CLASS_NAME, 'ipc-metadata-list__item')[2]
    for el in stars_tag.find_elements(By.CLASS_NAME, 'ipc-inline-list__item'):
        stars.append(el.text)

    movie_details['directors'] = director
    movie_details['writers'] = writers
    movie_details['stars'] = stars
    movie_details['user_reviews'] = driver.find_elements(By.CLASS_NAME, 'score')[0].text
    movie_details['critic_reviews'] = driver.find_elements(By.CLASS_NAME, 'score')[1].text
    movie_details['awards_and_nominees'] = driver.find_element(By.CLASS_NAME, 'ipc-metadata-list.ipc-metadata-list--dividers-none.sc-fcdc3619-2.oEiKO.ipc-metadata-list--base').text

    return movie_details

# for url in url_list:
#     driver.get(url)
#     print(driver.current_url)
#     sleep(2)
#     find_movies()
#     print(len(all_movies))


def save_data(file_name, data):
    with open(file_name, 'a') as f:
        json.dump(data, f)


if __name__ == '__main__':
    with open('sample.json', 'r') as f:
        all_movies = json.load(f)

    f = open('level_2_data.json', 'a')
    for movie in all_movies:
        try:
            data = movie_details(movie)
            f.write(json.dumps(data))
            f.write('\n')

        except Exception as e:
            print(e)
            continue
    f.close()






