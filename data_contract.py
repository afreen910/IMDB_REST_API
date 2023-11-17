movies_endpoint_1 = ['GET /movies', 'POST /movies']

get_request_param = 'movie_name=Iron Man'
post_request_json = {"movie_names": ["Iron Man", "The Shawshank Redemption"]}

get_response = {'movie_id': '',
                'movie_name': '',
                'movie_url': '',
                'user_reviews': '',
                'awards_nominees': ''
                }

post_response = {'movie_data': [{'movie_id': 1,
                                 'movie_name': '',
                                 'movie_url': '',
                                 'user_reviews': '',
                                 'awards_nominees': ''
                                 },
                                {'movie_id': 2,
                                 'movie_name': '',
                                 'movie_url': '',
                                 'user_reviews': '',
                                 'awards_nominees': ''
                                 }
                                ]}

#############################################

dir_movie_endpoint_2 = ['GET /directors_to_movies', 'POST /directors_to_movies']

get_request_param = 'director_name  = Frank Darabont'
post_request_json = {"director_name": ["Frank Darabont", 'Christopher Nolan']}

get_response = {'movie_names': ['The shawshank redemption', 'The Green Mile']}

post_response = {'movies_names': {'Frank Darabont': ['The shawshank redemption', 'The Green Mile'],
                                  'Christopher Nolan': ['The shawshank redemption', 'The Green Mile']}}

#############################################

role_movie_endpoint_3 = ['GET /role_to_movies', 'POST /role_to_movies']

get_request_param = 'role_name = Andy Dufresne'
post_request_json = {"roles": ["Andy Dufresne", "Thor"]}

get_response = {'movie_names': ['The shawshank redemption', 'The Green Mile']}

post_response = {'movies_names': {'Andy Dufresne': ['The shawshank redemption', 'The Green Mile'],
                                  'Captain Hadley': ['The shawshank redemption', 'The Green Mile']}}


##############################################

actors_movie_role_endpoint_4 = ['GET /actors_to_movies_and_roles', 'POST /actors_to_movies_and_roles']

get_request_param = 'actor_name = Tim Robbins'
post_request_json = {"actor_names": ["Tim Robbins", "Thor"]}

get_response = {'movie_name' : ['The Shawshank Redemption', 'Mystic River'],
                'Roles': ['Andy Duferson','Dave Boyle']}

post_response = {'actor_names': {'Tim Robbins': {'movie_name': ['The shawshank Redemption','Mystic River'],
                                                 'Roles': ['Andy Duferson','Dave Boyle']},
                                 'Robert Downey Jr': {'movie_name': ['Iron Man','Avengers'],
                                                  'Roles': ['Tony Stark','Tony Stark']}}
                 }

###############################################

movies_cast_endpoint_5 = ['GET /movies_to_cast', 'POST /movies_to_cast']

get_request_param = 'movie_name = The shawshank Redemption'
post_request_json = {"movie_name": ["The shawshank redemption", "The Green Mile"]}

get_response = {'cast': ['Andy Duffereson', 'Morgan Freeman']}

post_response = {'cast': {'The shawshank Redemption': ['Andy Duferson', 'Morgan Freeman']},
                 {'The Green Mile': ['Andy Duferson','Morgan Freeman']}
                 }

###############################################

movie_reviews_endpoint_6 = ['GET /movie_to_review', 'POST /movie_to_review']

get_request_param = 'movie_name = The Shawshank Redemption'
post_request_json = {"movie_name" : ["The shawshank Redemption", "The Green Mile"]}

get_response = {'user_reviews': 11000,
                 'critic_reviews':174}

post_response = {'movie_name': {'The shawshank redemption': {'user_reviews':11000,
                                                             'critic_reviews': 174},
                                'The Green Mile' : {'user_reviews': 1233,
                                                    'critic_reviews': 890}
                                }
                 }

###############################################

