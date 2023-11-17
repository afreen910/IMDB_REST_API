import json


def load_file(movie_name=None):
    with open('level_2_data.json', 'r') as f:
        movie_data = f.readlines()
    movies = []
    for i in movie_data:
        # print(json.loads(i))
        movies.append(json.loads(i))

    if movie_name:
        for i in movies:
            if movie_name.lower() == i['movie_name'].lower():
                return i
        print('movie not found')
        return
    return movies
    # return movies
    # print(i['movie_name'])
    # print(movies[0])
    # return movies


def movie_finder(movie_name):
    data = load_file()

    for i in data:
        if movie_name.lower() in i['movie_name'].lower():
            print(f"The movie name is {i['movie_name']}")
            print(f"The no of awards won is {i['awards_and_nominees']}")
            print(f"The stars are {i['stars']}")
            print(f"The user ratings are {i['user_reviews']}")


def highest_movie_rating():
    data = load_file()
    max_rating = converter(data[0]['user_reviews'])
    movie_name = ''
    print(max_rating)
    for i in data:
        if max_rating < converter(i['user_reviews']):
            max_rating = converter(i['user_reviews'])
            movie_name = i['movie_name']

    return f"The movie is {movie_name} and the review is {max_rating}"


def converter(review):
    if 'K' in review:
        number = float(review.replace('K', ''))
        number = number * 1000
    else:
        number = float(review)

    return number


if __name__ == '__main__':
    print(load_file())
# movie_finder('The Shawshank Redemption')
# # # converter()
# # print(highest_movie_rating())
