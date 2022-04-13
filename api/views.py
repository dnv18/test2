from flask import Blueprint, jsonify
from sqlalchemy import select
from .models import Team, League, TeamLeague

api = Blueprint('api', __name__)


@api.route('/leagues', methods=['GET'])
def get_leagues():
    data = []
    leagues = select([League.c.idleague, League.c.strleague]).order_by(League.c.idleague).execute()

    for league in leagues:
        d_league = dict(league.items())
        teams = select([Team.c.idteam, Team.c.strteam])\
            .join(TeamLeague, onclause=Team.c.idteam == TeamLeague.c.idteam)\
            .where(league.idleague == TeamLeague.c.idleague).execute()
        d_teams_in_league = []
        for team in teams:
            d_teams_in_league.append(dict(team.items()))
        d_league['Teamsset'] = d_teams_in_league
        data.append(d_league)
    return jsonify(data[:5])
