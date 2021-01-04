from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, redirect
from collections import defaultdict
import spoonacular as sp
import os

api = sp.API(os.environ.get('SPOONACULAR_KEY'))

app = Flask(__name__)


def welcome_message():
    """
    Returns a simple welcome message
    :return: welcome message
    """
    return 'Hello! Welcome to the very simple recipe finder. Please enter an ingredient or cuisine:'


def goodbye_message():
    """
    Returns a goodbye message
    :return: goodbye message
    """
    return 'Thank you, Goodbye!'


def help_message():
    """
    Returns a help message. Provides possible endpoints for the user
    :return: a help message
    """
    return '"hello": welcome message\n' \
           '"bye": goodbye message\n' \
           '"help?": help message\n' \
           '"random": random recipe\n' \
           'Text whatever recipe you are looking for, example:\n' \
           'I am looking for a cheeseburger recipe.'


def random_recipe_message() -> (str, str):  # (formatted message, image url)
    """
    Returns a random recipe message
    :return: a random recipe
    """
    response = api.get_random_recipes()
    data = response.json()
    r_title = data['recipes'][0]['title']               # recipe title
    r_url = data['recipes'][0]['spoonacularSourceUrl']  # recipe url
    r_img = data['recipes'][0]['image']                 # image url

    return 'Random Recipe:\n{title}\n{url}'.format(title=r_title, url=r_url), r_img


def looking_for_message(data: dict) -> str:
    """"
    Takes a dict returned by call to Spoonacular API and returns a formatted message with
    only the food items
    :food_items dict of parsed search query
    :return formatted message
    """
    print(data)

    params = {
                'includeIngredients': [],
                'excludeIngredients': []
                # 'cuisines': [],
                # 'modifiers': []
             }
    dish_query = {'query': ''}

    for k, v in data.items():
        if k == 'ingredients':
            for i in v:
                if i['include']:
                    params['includeIngredients'].append(i['name'])
                else:
                    params['excludeIngredients'].append(i['name'])

        elif k == 'dishes':
            for i in v:
                dish_query['query'] = i['name']

        elif k == 'cuisines':
            pass

        elif k == 'modifiers':
            pass

    print(params)
    print(dish_query['query'])
    #response = api.search_recipes_complex(dish_query['query'], params)
    #print(response)

    return 'stub'


@app.route('/sms', methods=['GET', 'POST'])
def sms_reply():
    # get message
    body = request.values.get('Body', None).lower()

    # start TwiML response
    resp = MessagingResponse()

    if body == 'hello':
        resp.message(welcome_message())

    elif body == 'bye':
        resp.message(goodbye_message())

    elif body == 'help?':
        resp.message(help_message())

    elif body == 'random':
        random_recipe = random_recipe_message()
        msg = resp.message(random_recipe[0])
        msg.media(random_recipe[1])

    else:
        # we will analyze the text for food items, such as dish names and ingredients
        response = api.analyze_a_recipe_search_query(body)
        data = response.json()
        resp.message(looking_for_message(data))

    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)
