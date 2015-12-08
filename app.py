import os

from flask import Flask
from flask import render_template, url_for
from flask import request


app = Flask(__name__)

# from the flask documentation, because typically the route only answers to GET but we can change that providing the methods argument


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['GET','POST'])
def game():
    form = request.form
    if request.method == 'POST':
        player2_name = form['name_player2']
        player1_name = form['name_player1']
        player2_strategy1 = form['strategy1_player2']
        player2_strategy2 = form['strategy2_player2']
        player1_strategy1 = form['strategy1_player1']
        player1_strategy2 = form['strategy2_player1']
        return render_template('game.html',form = form, player1_name = player1_name, player2_name = player2_name, player1_strategy1 = player1_strategy1, player1_strategy2 = player1_strategy2, player2_strategy1 = player2_strategy1, player2_strategy2 = player2_strategy2, is_result=False )

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        #deveríamos ter usado sessions para não precisar repetir as informações, porém não conseguimos aprender a tempo.
        form = request.form
        player2_name = form['name_player2']
        player1_name = form['name_player1']
        player2_strategy1 = form['strategy1_player2']
        player2_strategy2 = form['strategy2_player2']
        player1_strategy1 = form['strategy1_player1']
        player1_strategy2 = form['strategy2_player1']

        data, form = evaluate_payoff(form)
        control_variable2 = 2
        # receives data submited
    else:
        data, form = [], {}  # does not save any data

    return render_template('results.html', data=data, form=form, is_result=True)

def evaluate_payoff(form):
    player1_ul = float(form['player1-UL'])
    player1_dl = float(form['player1-DL'])
    player1_ur = float(form['player1-UR'])
    player1_dr = float(form['player1-DR'])

    player2_ul = float(form['player2-UL'])
    player2_ur = float(form['player2-UR'])
    player2_dl = float(form['player2-DL'])
    player2_dr = float(form['player2-DR'])

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
        equilibrios.append(player1_strategy1 + ',' + player2_strategy1)

    if choice_list.count('UR') >= 2:
        equilibrios.append(player1_strategy1 + ',' + player2_strategy2)

    if choice_list.count('DL') >= 2:
        equilibrios.append(player1_strategy2 + ',' + player2_strategy1)

    if choice_list.count('DR') >= 2:
        equilibrios.append(player1_strategy2 + ',' + player2_strategy2)

    return equilibrios, form


def case_player1_deny(player2_ul, player2_ur):
    if player2_ul > player2_ur:
        return ['UL']
    elif player2_ul < player2_ur:
        return ['UR']
    else:
        return ['UR', 'UL']


def case_player2_deny(player1_ul, player1_dl):
    if player1_ul > player1_dl:
        return ['UL']
    elif player1_ul < player1_dl:
        return ['DL']
    else:
        return ['DL', 'UL']


def case_player1_dilate(player2_dl, player2_dr):
    if player2_dl > player2_dr:
        return ['DL']
    elif player2_dl < player2_dr:
        return ['DR']
    else:
        return ['DL', 'DR']


def case_player2_dilate(player1_ur, player1_dr):
    if player1_ur > player1_dr:
        return ['UR']
    elif player1_ur < player1_dr:
        return ['DR']
    else:
        return ['UR', 'DR']
# app.debug = True
PORT = int(os.getenv('PORT', 8000))

app.run(host='', port=PORT)
