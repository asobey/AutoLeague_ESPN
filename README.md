# AutoLeague_ESPN
ESPN Fantasy Football Robot in Python3

After the draft, let the AutoLeague take care of your team for you. You have too much
on your plate. Sit back and relax while AutoLeage takes care of the thinking. Starting
with ESPN.


Automate_Team_Management is the main file used to handle ESPN Fantasy Football (FF)
Team Management. This is meant to handle an entire season without users input.
GOALS:
1) Set weekly line-ups (put high scorers in, take low scorers/non players out)
2) Frequent the waiver wire and pickup better players
3) Offer trades (offset to owners team)
4) Auto Shittalk - Pregame
4) Auto Brag - Postgame

=======
After the draft, let the AutoLeague take care of your team for you. You have too much on your plate. Sit back and relax while
AutoLeague takes care of the thinking. Starting with ESPN.

Atomate_Team_Management is the main file used to handle ESPN Fantasy Football (FF) Team Management.

One required file that I do not have on GitHub is the username/password keeper. Please create this file and place it in the same directory to use this program. It consists of only two lines (below) and requires your ESPN username and password.
Filename: espn_creds.yaml
File Contents: "
ESPNUserName: xxxxxxxxxx@xxxxxxxxx.com
routerPassword: xxxxxxxxxxxx
"

#Desired Methods organized within Files

###TeamManagement.py

def __main__():
    loops manage team at specific times (daily)
    manage_team()
    taunt_bot()

def manage_team():
    get_team()
    get_free_agents()
        optimize_free_agents()
            pickup_free_agents()
    
    get_team()
        optimize_team()
        switch_players_in_roster()
    
def get_team():
    return position_chart

def optimize_team(get_team()):
    switches = []
    for player in roaster[playing positions]:
        for possible_replacement in replacement_hierarchy:
            if player_side_by_side(player, possible_replacement):
                switch_players_in_roster()
    return list of switch x for y

def player_side_by_side(current, possible_replacement):
    if evaluate_player(current) < evaluate_player(possible_replacement):
        return True
    else:
        return False

def evaluate_player():
    return player_score

def switch_players_in_roster():

def get_free_agents():
    return free_agent_chart

def optimize_free_agents(get_team(), get_free_agents()):
    return list of switch x for y
    
def pickup_free_agent(optimize_free_agents())


###LeagueComm.py

def taunt_bot():
find losses or low projections
return team, msg

def msg_bot(team, msg):
    send msg to team
    
####LeagueTrade.py

