import os

from flask import Flask
from flask import render_template, url_for
from flask import request


app = Flask(__name__)

# from the flask documentation, because typically the route only answers to GET but we can change that providing the methods argument

@app.route('/', methods=['GET', 'POST'])
def firstpage():
    if request.method == 'POST':
        data, form = register_players(request.form)
        # receives data submited
    else:
        data, form = [], None  # does not save any data
    return render_template('index.html', data=data, form=form)

def register_players(form):
    player2_name = form['name_player2']
    player1_name = form['name_player1']
    player2_strategy1 = form['strategy1_player2']
    player2_strategy2 = form['strategy2_player2']
    player1_strategy1 = form['strategy1_player1']
    player1_strategy2 = form['strategy2_player1']

@app.route('/game', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data, form = evaluate_payoff(request.form)
        # receives data submited
    else:
        data, form = [], None  # does not save any data
    return render_template('game.html', data=data, form=form)




def evaluate_payoff(form):
    player1_ul = float(form['player1-UL'])
    player1_dl = float(form['player1-DL'])
    player1_ur = float(form['player1-UR'])
    player1_dr = float(form['player1-DR'])

    player2_ul = float(form['player2-UL'])
    player2_ur = float(form['player2-UR'])
    player2_dl = float(form['player2-DL'])
    player2_dr = float(form['player2-DR'] )

    p1_choice_1 = case_player2_deny(player1_ul, player1_dl)
    p1_choice_2 = case_player2_dilate(player1_ur, player1_dr)

    p2_choice_1 = case_player1_deny(player2_ul, player2_ur)
    p2_choice_2 = case_player1_dilate(player2_dl, player2_dr)

    choice_list = []
    choice_list.extend(p1_choice_1)
    choice_list.extend(p1_choice_2)
    choice_list.extend(p2_choice_1)
    choice_list.extend(p2_choice_2)

    equilibrios = []
    if choice_list.count('UL') >= 2:
        equilibrios.append('UL')

    if choice_list.count('UR') >= 2:
        equilibrios.append('UR')

    if choice_list.count('DL') >= 2:
        equilibrios.append('DL')

    if choice_list.count('DR') >= 2:
        equilibrios.append('DR')

    return equilibrios, form


def case_player1_deny(player2_ul, player2_ur):
    if player2_ul > player2_ur:
        return [player2_strategy1 +  " e "  + player1_strategy1]
    elif player2_ul < player2_ur:
        return [player2_strategy1 + " e " + player1_strategy2]
    else:
        return [player2_strategy1  + " e " + player1_strategy1, player2_strategy1 + " e " + player1_strategy2]


def case_player2_deny(player1_ul, player1_dl):
    if player1_ul > player1_dl:
        return [player2_strategy1 + " e " + player1_strategy1]
    elif player1_ul < player1_dl:
        return [player2_strategy2 + " e " + player1_strategy1]
    else:
        return [player2_strategy1 + " e " + player1_strategy1,player2_strategy2 + " e " + player1_strategy1]


def case_player1_dilate(player2_dl, player2_dr):
    if player2_dl > player2_dr:
        return [player2_strategy2 + " e " + player1_strategy1]
    elif player2_dl < player2_dr:
        return [player2_strategy2 + " e " + player1_strategy2]
    else:
        return [player2_strategy2  + " e " + player1_strategy1,player2_strategy2 + " e " + player1_strategy2]


def case_player2_dilate(player1_ur, player1_dr):
    if player1_ur > player1_dr:
        return [player2_strategy1 + " e " + player1_strategy2]
    elif player1_ur < player1_dr:
        return [player2_strategy2 + " e " + player1_strategy2]
    else:
        return [player2_strategy1 + " e " + player1_strategy2,player2_strategy2 + " e " + player1_strategy2]


# app.debug = True
PORT = int(os.getenv('PORT', 8000))

app.run(host='', port=PORT)
