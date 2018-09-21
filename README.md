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

One required file that I do not have on GitHub is the username/password keeper. Please create this file and place it in the same directory to use this program. Follow the format in espn_creds_example.yaml to create the new file with filename: espn_creds.yaml.

#Desired Methods organized within Files (this is all still hypothetical)

###TeamManagement.py

--------4 MODULES---------
*future

Manage
    main
        team
Browse
    __init__
        import_yaml_file (could also exist in Manage)
        open_browser
        login (frontpage)
            from_cookies
            from_creds
    waiver
        open_waiver(position)
    external_ranking
    save_source
    pickup_waiver
    sort_team
        multispot
        move
    trade*
Parse
    print
    create
        open_source
        update_table
            add_position
            add_id
            add_here        
Logic
    team_sort (put best player in)
    waiver_sort (choose waiver player to trade)
Communication*
    Taunt*
    

------ACTION OUTLINE--------

def Manage.main():  # run Manage.team at specific times
    def Manage.team():  # all team management occur here
        Browse.frontpage(): # get browser object and frontpage source
            Browse.import_yaml_file
            Browse.open_browser
            Browse.login (frontpage)
            Browse.save_source (get rid of this eventually)
        Parse.create  # Create team table
            Parse.open_source (get rid of this eventually)
            Parse.update_table
                Parse.add_position
                Parse.add_id
                Parse.add_here
        Browse.waiver
            Browse.open_waiver
            Browse.get_waivers
        Browse.eternal_ranking  # return ranking from 3rd party (yahoo, http://www.borischen.co/)
        Logic.waiver_sort(team_table, waivers, external_rankings(optional))
            Browser.pickup_waiver
        Logic.team_sort(team_table, external_rankings(optional))
            Browser.sort_team
                Browser.multispot
                Browser.move


Communication
    Communication.taunt_bot(): #find losses or low projections
        return team, msg
    Communication.msg_bot(team, msg):
    send msg to team
    
Broswer.trade

-------- Required Assets -------------
yaml
tabulate
os
requests
selenium
pandas 0.23.4
re
BeautifulSoup4

chrome webdriver