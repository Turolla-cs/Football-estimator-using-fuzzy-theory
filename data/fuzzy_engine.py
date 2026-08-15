import numpy as np
import skfuzzy as fuzz

from skfuzzy import control as ctrl
from dataclasses import dataclass

@dataclass
class Result:
    output1: float
    output2: float


#Games played
gamesPlayed = ctrl.Antecedent(np.arange(0,39,1), 'Number of games played so far')

#Attack sub system
goalsAttack = ctrl.Antecedent(np.arange(0,101,1), 'Goal scored per game')
winPercentage = ctrl.Antecedent(np.arange(0,101,1), 'Percentage of games won')
scorelessPercentage = ctrl.Antecedent(np.arange(0,101,1), 'Percentage of scoreless games')
shotsAttack = ctrl.Antecedent(np.arange(0,31,1), 'Shots made per game')
offensiveDominance = ctrl.Consequent(np.arange(0,11,1), 'Offensive dominance')

#Defensive sub system
goalsDefense = ctrl.Antecedent(np.arange(0,101,1), 'Goal suffered per game')
cleansheetPercentage= ctrl.Antecedent(np.arange(0,101,1), 'Percentage of clean sheet games')
shotsDefense = ctrl.Antecedent(np.arange(0,31,1), 'Shots suffered per game')
defensiveDominance = ctrl.Consequent(np.arange(0,11,1), 'Defensive dominance')

#Result sub system
homeAdominance = ctrl.Antecedent(np.arange(0,11,1), 'Home team offensive dominance')
homeDdominance = ctrl.Antecedent(np.arange(0,11,1), 'Home team defensive dominance')
awayAdominance = ctrl.Antecedent(np.arange(0,11,1), 'Away team offensive dominance')
awayDdominance = ctrl.Antecedent(np.arange(0,11,1), 'Away team defensive dominance')
homeW = ctrl.Consequent(np.arange(0,11,1), 'Home Winning prediction')
awayW = ctrl.Consequent(np.arange(0,11,1), 'Away Winning prediction')

#Functions 
goalsAttack.automf(3)
winPercentage.automf(3)
goalsDefense.automf(3)
cleansheetPercentage.automf(3)
scorelessPercentage.automf(3)
shotsAttack.automf(3)
shotsDefense.automf(3)
gamesPlayed.automf(3)
homeAdominance.automf(3)
homeDdominance.automf(3)
awayDdominance.automf(3)
awayAdominance.automf(3)
homeW.automf(3)
awayW.automf(3)

offensiveDominance['very poor'] = fuzz.trimf(offensiveDominance.universe, [0,2,4])
offensiveDominance['poor'] = fuzz.trimf(offensiveDominance.universe, [0,4,6])
offensiveDominance['average'] = fuzz.trimf(offensiveDominance.universe, [4,6,8])
offensiveDominance['good'] = fuzz.trimf(offensiveDominance.universe, [5,10,10])

defensiveDominance['very poor'] = fuzz.trimf(defensiveDominance.universe, [0,2,4])
defensiveDominance['poor'] = fuzz.trimf(defensiveDominance.universe, [0,4,6])
defensiveDominance['average'] = fuzz.trimf(defensiveDominance.universe, [4,6,8])
defensiveDominance['good'] = fuzz.trimf(defensiveDominance.universe, [5,10,10])

#Rules
rules_attack = [
    ctrl.Rule(goalsAttack['good'] & winPercentage['good'], offensiveDominance['good']),
    ctrl.Rule(shotsAttack['good'] & goalsAttack['average'] & scorelessPercentage['poor'], offensiveDominance['good']),
    ctrl.Rule(goalsAttack['average'] & winPercentage['average'], offensiveDominance['average']),
    ctrl.Rule(shotsAttack['good'] & goalsAttack['poor'], offensiveDominance['average']),
    ctrl.Rule(goalsAttack['poor'] & winPercentage['average'], offensiveDominance['poor']),
    ctrl.Rule(goalsAttack['poor'] & shotsAttack['poor'], offensiveDominance['poor']),
    ctrl.Rule(goalsAttack['poor'] & winPercentage['poor'] & scorelessPercentage['good'], offensiveDominance['very poor'])
]

rules_defense = [
    ctrl.Rule(goalsDefense['poor'] & cleansheetPercentage['good'], defensiveDominance['good']),
    ctrl.Rule(shotsDefense['good'] & goalsDefense['poor'], defensiveDominance['good']),
    ctrl.Rule(goalsDefense['average'] & cleansheetPercentage['average'], defensiveDominance['average']),
    ctrl.Rule(shotsDefense['poor'] & goalsDefense['average'], defensiveDominance['average']),
    ctrl.Rule(goalsDefense['good'] & cleansheetPercentage['poor'], defensiveDominance['poor']),
    ctrl.Rule(goalsDefense['good'] & shotsDefense['good'] & cleansheetPercentage['poor'], defensiveDominance['very poor'])
]

rules_result = [
    ctrl.Rule(homeAdominance['good'] & awayDdominance['poor'], (homeW['good'], awayW['poor'])),
    ctrl.Rule(homeDdominance['good'] & awayAdominance['poor'], (homeW['good'], awayW['poor'])),
    ctrl.Rule(awayAdominance['good'] & homeDdominance['poor'], (awayW['good'], homeW['poor'])),
    ctrl.Rule(awayDdominance['good'] & homeAdominance['poor'], (awayW['good'], homeW['poor'])),
    ctrl.Rule(homeAdominance['good'] & awayDdominance['average'], (homeW['good'], awayW['average'])),
    ctrl.Rule(awayAdominance['good'] & homeDdominance['average'], (awayW['good'], homeW['average'])),
    ctrl.Rule(homeAdominance['good'] & awayDdominance['good'], (homeW['average'], awayW['average'])),
    ctrl.Rule(awayAdominance['good'] & homeDdominance['good'], (homeW['average'], awayW['average'])),
    ctrl.Rule(homeAdominance['average'] & awayAdominance['average'], (homeW['average'], awayW['average'])),
    ctrl.Rule(homeDdominance['average'] & awayDdominance['average'], (homeW['average'], awayW['average'])),
    ctrl.Rule(homeAdominance['poor'] & awayDdominance['poor'], (homeW['average'], awayW['average'])),
    ctrl.Rule(awayAdominance['poor'] & homeDdominance['poor'], (homeW['average'], awayW['average'])),
    ctrl.Rule(homeAdominance['poor'] & awayDdominance['good'], (homeW['poor'], awayW['good'])),
    ctrl.Rule(awayAdominance['poor'] & homeDdominance['good'], (awayW['poor'], homeW['good']))
]

attack_control_sys = ctrl.ControlSystem(rules_attack)
defense_control_sys = ctrl.ControlSystem(rules_defense)
result_control_sys = ctrl.ControlSystem(rules_result)

simulator_attack = ctrl.ControlSystemSimulation(attack_control_sys)
simulator_defense = ctrl.ControlSystemSimulation(defense_control_sys)
simulator_result = ctrl.ControlSystemSimulation(result_control_sys)

def calculate_fuzzy_prediction(home_team_attack, home_team_defense, away_team_attack, away_team_defense):
    simulator_attack.input['Goal scored per game'] = home_team_attack["goals_scored_per_game"]
    simulator_attack.input['Percentage of games won'] = home_team_attack["wins_percentage"]
    simulator_attack.input['Percentage of scoreless games'] = home_team_attack["scoreless_percentage"]
    simulator_attack.input['Shots made per game'] = home_team_attack["shots_made_per_game"]
    simulator_defense.input['Goal suffered per game'] = home_team_defense["goals_suffered_per_game"]
    simulator_defense.input['Percentage of clean sheet games'] = home_team_defense["clean_sheets_percentage"]
    simulator_defense.input['Shots suffered per game'] = home_team_defense["shots_suffered_per_game"]
    simulator_attack.compute()
    simulator_defense.compute()
    simulator_result.input['Home team offensive dominance'] = simulator_attack.output['Offensive dominance']
    simulator_result.input['Home team defensive dominance'] = simulator_defense.output['Defensive dominance']


    simulator_attack.input['Goal scored per game'] = away_team_attack["goals_scored_per_game"]
    simulator_attack.input['Percentage of games won'] = away_team_attack["wins_percentage"]
    simulator_attack.input['Percentage of scoreless games'] = away_team_attack["scoreless_percentage"]
    simulator_attack.input['Shots made per game'] = away_team_attack["shots_made_per_game"]
    simulator_defense.input['Goal suffered per game'] = away_team_defense["goals_suffered_per_game"]
    simulator_defense.input['Percentage of clean sheet games'] = away_team_defense["clean_sheets_percentage"]
    simulator_defense.input['Shots suffered per game'] = away_team_defense["shots_suffered_per_game"]
    simulator_attack.compute()
    simulator_defense.compute()
    simulator_result.input['Away team offensive dominance'] = simulator_attack.output['Offensive dominance']
    simulator_result.input['Away team defensive dominance'] = simulator_defense.output['Defensive dominance']
    

    simulator_result.compute()
    x = Result(
        output1=simulator_result.output['Home Winning prediction'], 
        output2=simulator_result.output['Away Winning prediction']
    )
    return x





