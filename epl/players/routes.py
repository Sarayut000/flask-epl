from flask import Blueprint, render_template, redirect, url_for,request, flash
from epl.extensions import db
from epl.models import Player, Club

player_bp= Blueprint('players', __name__, template_folder='templates')

@player_bp.route('/')
def index():
  players = db.session.scalars(db.select(Player)).all()
  return render_template('players/index.html',
                         title='Players Page',
                         players=players)

@player_bp.route('/new', methods=['GET', 'POST'])
def new_player():
  clubs = db.session.scalars(db.select(Club)).all()
  if request.method == 'POST':
    name = request.form['name']
    position = request.form['position']
    nationality = request.form['nationality']
    goals_input = request.form['goals']
    squad_no = int(request.form['squad_no'])
    img = request.form['img']
    club_id = int(request.form['club_id'])
    clean_input = request.form['clean_sheet']

    goals = int(goals_input) if goals_input != "0" else None
    clean_sheet = int(clean_input) if clean_input != "0" else None

    player = Player(name=name, position=position, nationality=nationality,
                    goals=goals, squad_no=squad_no, img=img, club_id=club_id, clean_sheet=clean_sheet)
    db.session.add(player)
    db.session.commit()
    flash('add new player successfully', 'success')
    return redirect(url_for('players.index'))

  return render_template('players/new_player.html',
                         title='New Player Page',
                         clubs=clubs)

@player_bp.route('/search', methods=['POST'])
def search_player():
  if request.method == 'POST':
    player_name = request.form['player_name']
    players = db.session.scalars(db.select(Player).where(Player.name.like(f'%{player_name}%'))).all()
    return render_template('players/search_player.html',
                           title='Search Player Page',
                           players=players)

@player_bp.route('/<int:id>/info')
def info_player(id):
  player = db.session.get(Player, id)
  return render_template('players/info_player.html',
                         title='Info Player Page',
                         player=player)

@player_bp.route('/<int:id>/update', methods=['GET','POST'])
def update_player(id):
  player = db.session.get(Player, id)
  query = db.select(Club)
  clubs = db.session.scalars(query).all()
  if request.method == 'POST':
    name = request.form['name']
    position = request.form['position']
    nationality = request.form['nationality']
    goals = request.form.get('goals', type=int)
    squad_no = int(request.form['squad_no'])
    img = request.form['img']
    club_id = int(request.form['club_id'])
    clean_sheet = request.form.get('clean_sheet', type=int)


    player.name = name
    player.position = position
    player.nationality = nationality
    player.goals = int(goals) if goals  else None
    player.squad_no = squad_no
    player.img = img
    player.club_id = club_id
    player.clean_sheet = int(clean_sheet) if clean_sheet else None

    db.session.add(player)
    db.session.commit()
    flash('update player successfully', 'success')
    return redirect(url_for('players.index'))

  return render_template('players/update_player.html',
                         title='Update Player Page',
                         player=player,
                         clubs=clubs)

@player_bp.route('/<int:id>/clean_sheet', methods=['POST'])
def clean_sheet_player(id):
  player = db.session.get(Player, id)
  if request.method == 'POST':
    player.clean_sheet += 1

    db.session.add(player)
    db.session.commit()
    flash('update clean sheet successfully', 'success')
    return redirect(url_for('players.index'))
