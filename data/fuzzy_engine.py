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
goalsAttack = ctrl.Antecedent(np.arange(0,6,1), 'Goal scored per game')
winPercentage = ctrl.Antecedent(np.arange(0,101,1), 'Percentage of games won')
scorelessPercentage = ctrl.Antecedent(np.arange(0,101,1), 'Percentage of scoreless games')
shotsAttack = ctrl.Antecedent(np.arange(0,31,1), 'Shots made per game')
offensiveDominance = ctrl.Consequent(np.arange(0,11,1), 'Offensive dominance')

#Defensive sub system
goalsDefense = ctrl.Antecedent(np.arange(0,6,1), 'Goal suffered per game')
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
goalsAttack.automf(5)
winPercentage.automf(5)
goalsDefense.automf(5)
cleansheetPercentage.automf(5)
scorelessPercentage.automf(5)
shotsAttack.automf(5)
shotsDefense.automf(5)
gamesPlayed.automf(5)
homeAdominance.automf(5)
homeDdominance.automf(5)
awayDdominance.automf(5)
awayAdominance.automf(5)
homeW.automf(5)
awayW.automf(5)

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
    ctrl.Rule(goalsAttack['poor'] & winPercentage['poor'] & scorelessPercentage['good'], offensiveDominance['very poor']),
    ctrl.Rule(goalsAttack['poor'] & winPercentage['poor'], offensiveDominance['very poor']),
    ctrl.Rule(goalsAttack['poor'] & winPercentage['mediocre'], offensiveDominance['very poor']),
    ctrl.Rule(goalsAttack['poor'] & winPercentage['decent'], offensiveDominance['poor']),
    ctrl.Rule(goalsAttack['poor'] & winPercentage['good'], offensiveDominance['average']),
    ctrl.Rule(goalsAttack['mediocre'] & winPercentage['poor'], offensiveDominance['very poor']),
    ctrl.Rule(goalsAttack['mediocre'] & winPercentage['mediocre'], offensiveDominance['poor']),
    ctrl.Rule(goalsAttack['mediocre'] & winPercentage['average'], offensiveDominance['poor']),
    ctrl.Rule(goalsAttack['mediocre'] & winPercentage['decent'], offensiveDominance['average']),
    ctrl.Rule(goalsAttack['mediocre'] & winPercentage['good'], offensiveDominance['average']),
    ctrl.Rule(goalsAttack['average'] & winPercentage['poor'], offensiveDominance['poor']),
    ctrl.Rule(goalsAttack['average'] & winPercentage['mediocre'], offensiveDominance['poor']),
    ctrl.Rule(goalsAttack['average'] & winPercentage['decent'], offensiveDominance['average']),
    ctrl.Rule(goalsAttack['average'] & winPercentage['good'], offensiveDominance['good']),
    ctrl.Rule(goalsAttack['decent'] & winPercentage['poor'], offensiveDominance['poor']),
    ctrl.Rule(goalsAttack['decent'] & winPercentage['mediocre'], offensiveDominance['average']),
    ctrl.Rule(goalsAttack['decent'] & winPercentage['average'], offensiveDominance['average']),
    ctrl.Rule(goalsAttack['decent'] & winPercentage['decent'], offensiveDominance['good']),
    ctrl.Rule(goalsAttack['decent'] & winPercentage['good'], offensiveDominance['good']),
    ctrl.Rule(goalsAttack['good'] & winPercentage['poor'], offensiveDominance['average']),
    ctrl.Rule(goalsAttack['good'] & winPercentage['mediocre'], offensiveDominance['average']),
    ctrl.Rule(goalsAttack['good'] & winPercentage['average'], offensiveDominance['good']),
    ctrl.Rule(goalsAttack['good'] & winPercentage['decent'], offensiveDominance['good']),
    ctrl.Rule(shotsAttack['decent'] & goalsAttack['decent'] & scorelessPercentage['mediocre'], offensiveDominance['good']),
    ctrl.Rule(shotsAttack['decent'] & goalsAttack['mediocre'], offensiveDominance['average']),
    ctrl.Rule(goalsAttack['mediocre'] & shotsAttack['mediocre'], offensiveDominance['poor']),
]

rules_defense = [
    ctrl.Rule(goalsDefense['poor'] & cleansheetPercentage['good'], defensiveDominance['good']),
    ctrl.Rule(shotsDefense['good'] & goalsDefense['poor'], defensiveDominance['good']),
    ctrl.Rule(goalsDefense['average'] & cleansheetPercentage['average'], defensiveDominance['average']),
    ctrl.Rule(shotsDefense['poor'] & goalsDefense['average'], defensiveDominance['average']),
    ctrl.Rule(goalsDefense['good'] & cleansheetPercentage['poor'], defensiveDominance['poor']),
    ctrl.Rule(goalsDefense['good'] & shotsDefense['good'] & cleansheetPercentage['poor'], defensiveDominance['very poor']),
    ctrl.Rule(goalsDefense['poor'] & cleansheetPercentage['poor'], defensiveDominance['average']),
    ctrl.Rule(goalsDefense['poor'] & cleansheetPercentage['mediocre'], defensiveDominance['average']),
    ctrl.Rule(goalsDefense['poor'] & cleansheetPercentage['average'], defensiveDominance['good']),
    ctrl.Rule(goalsDefense['poor'] & cleansheetPercentage['decent'], defensiveDominance['good']),
    ctrl.Rule(goalsDefense['mediocre'] & cleansheetPercentage['poor'], defensiveDominance['poor']),
    ctrl.Rule(goalsDefense['mediocre'] & cleansheetPercentage['mediocre'], defensiveDominance['average']),
    ctrl.Rule(goalsDefense['mediocre'] & cleansheetPercentage['average'], defensiveDominance['average']),
    ctrl.Rule(goalsDefense['mediocre'] & cleansheetPercentage['decent'], defensiveDominance['good']),
    ctrl.Rule(goalsDefense['mediocre'] & cleansheetPercentage['good'], defensiveDominance['good']),
    ctrl.Rule(goalsDefense['average'] & cleansheetPercentage['poor'], defensiveDominance['poor']),
    ctrl.Rule(goalsDefense['average'] & cleansheetPercentage['mediocre'], defensiveDominance['poor']),
    ctrl.Rule(goalsDefense['average'] & cleansheetPercentage['decent'], defensiveDominance['average']),
    ctrl.Rule(goalsDefense['average'] & cleansheetPercentage['good'], defensiveDominance['good']),
    ctrl.Rule(goalsDefense['decent'] & cleansheetPercentage['poor'], defensiveDominance['very poor']),
    ctrl.Rule(goalsDefense['decent'] & cleansheetPercentage['mediocre'], defensiveDominance['poor']),
    ctrl.Rule(goalsDefense['decent'] & cleansheetPercentage['average'], defensiveDominance['poor']),
    ctrl.Rule(goalsDefense['decent'] & cleansheetPercentage['decent'], defensiveDominance['average']),
    ctrl.Rule(goalsDefense['decent'] & cleansheetPercentage['good'], defensiveDominance['average']),
    ctrl.Rule(goalsDefense['good'] & cleansheetPercentage['mediocre'], defensiveDominance['very poor']),
    ctrl.Rule(goalsDefense['good'] & cleansheetPercentage['average'], defensiveDominance['poor']),
    ctrl.Rule(goalsDefense['good'] & cleansheetPercentage['decent'], defensiveDominance['poor']),
    ctrl.Rule(goalsDefense['good'] & cleansheetPercentage['good'], defensiveDominance['average']),
    ctrl.Rule(shotsDefense['decent'] & goalsDefense['mediocre'], defensiveDominance['good']),
    ctrl.Rule(shotsDefense['mediocre'] & goalsDefense['decent'], defensiveDominance['average']),
    ctrl.Rule(goalsDefense['decent'] & shotsDefense['decent'] & cleansheetPercentage['poor'], defensiveDominance['very poor']),
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
    ctrl.Rule(awayAdominance['poor'] & homeDdominance['good'], (awayW['poor'], homeW['good'])),
    ctrl.Rule(homeAdominance['poor'] & awayDdominance['mediocre'], (homeW['average'], awayW['decent'])),
    ctrl.Rule(homeAdominance['poor'] & awayDdominance['average'], (homeW['average'], awayW['good'])),
    ctrl.Rule(homeAdominance['poor'] & awayDdominance['decent'], (homeW['mediocre'], awayW['good'])),
    ctrl.Rule(homeAdominance['mediocre'] & awayDdominance['poor'], (homeW['decent'], awayW['average'])),
    ctrl.Rule(homeAdominance['mediocre'] & awayDdominance['mediocre'], (homeW['average'], awayW['average'])),
    ctrl.Rule(homeAdominance['mediocre'] & awayDdominance['average'], (homeW['average'], awayW['decent'])),
    ctrl.Rule(homeAdominance['mediocre'] & awayDdominance['decent'], (homeW['average'], awayW['good'])),
    ctrl.Rule(homeAdominance['mediocre'] & awayDdominance['good'], (homeW['mediocre'], awayW['good'])),
    ctrl.Rule(homeAdominance['average'] & awayDdominance['poor'], (homeW['good'], awayW['average'])),
    ctrl.Rule(homeAdominance['average'] & awayDdominance['mediocre'], (homeW['decent'], awayW['average'])),
    ctrl.Rule(homeAdominance['average'] & awayDdominance['average'], (homeW['average'], awayW['average'])),
    ctrl.Rule(homeAdominance['average'] & awayDdominance['decent'], (homeW['average'], awayW['decent'])),
    ctrl.Rule(homeAdominance['average'] & awayDdominance['good'], (homeW['average'], awayW['good'])),
    ctrl.Rule(homeAdominance['decent'] & awayDdominance['poor'], (homeW['good'], awayW['mediocre'])),
    ctrl.Rule(homeAdominance['decent'] & awayDdominance['mediocre'], (homeW['good'], awayW['average'])),
    ctrl.Rule(homeAdominance['decent'] & awayDdominance['average'], (homeW['decent'], awayW['average'])),
    ctrl.Rule(homeAdominance['decent'] & awayDdominance['decent'], (homeW['average'], awayW['average'])),
    ctrl.Rule(homeAdominance['decent'] & awayDdominance['good'], (homeW['average'], awayW['decent'])),
    ctrl.Rule(homeAdominance['good'] & awayDdominance['mediocre'], (homeW['good'], awayW['mediocre'])),
    ctrl.Rule(homeAdominance['good'] & awayDdominance['decent'], (homeW['decent'], awayW['average'])),
    ctrl.Rule(homeDdominance['poor'] & awayAdominance['mediocre'], (homeW['average'], awayW['decent'])),
    ctrl.Rule(homeDdominance['poor'] & awayAdominance['average'], (homeW['average'], awayW['good'])),
    ctrl.Rule(homeDdominance['poor'] & awayAdominance['decent'], (homeW['mediocre'], awayW['good'])),
    ctrl.Rule(homeDdominance['mediocre'] & awayAdominance['poor'], (homeW['decent'], awayW['average'])),
    ctrl.Rule(homeDdominance['mediocre'] & awayAdominance['mediocre'], (homeW['average'], awayW['average'])),
    ctrl.Rule(homeDdominance['mediocre'] & awayAdominance['average'], (homeW['average'], awayW['decent'])),
    ctrl.Rule(homeDdominance['mediocre'] & awayAdominance['decent'], (homeW['average'], awayW['good'])),
    ctrl.Rule(homeDdominance['mediocre'] & awayAdominance['good'], (homeW['mediocre'], awayW['good'])),
    ctrl.Rule(homeDdominance['average'] & awayAdominance['poor'], (homeW['good'], awayW['average'])),
    ctrl.Rule(homeDdominance['average'] & awayAdominance['mediocre'], (homeW['decent'], awayW['average'])),
    ctrl.Rule(homeDdominance['average'] & awayAdominance['average'], (homeW['average'], awayW['average'])),
    ctrl.Rule(homeDdominance['average'] & awayAdominance['decent'], (homeW['average'], awayW['decent'])),
    ctrl.Rule(homeDdominance['decent'] & awayAdominance['poor'], (homeW['good'], awayW['mediocre'])),
    ctrl.Rule(homeDdominance['decent'] & awayAdominance['mediocre'], (homeW['good'], awayW['average'])),
    ctrl.Rule(homeDdominance['decent'] & awayAdominance['average'], (homeW['decent'], awayW['average'])),
    ctrl.Rule(homeDdominance['decent'] & awayAdominance['decent'], (homeW['average'], awayW['average'])),
    ctrl.Rule(homeDdominance['decent'] & awayAdominance['good'], (homeW['average'], awayW['decent'])),
    ctrl.Rule(homeDdominance['good'] & awayAdominance['mediocre'], (homeW['good'], awayW['mediocre'])),
    ctrl.Rule(homeDdominance['good'] & awayAdominance['average'], (homeW['good'], awayW['average'])),
    ctrl.Rule(homeDdominance['good'] & awayAdominance['decent'], (homeW['decent'], awayW['average'])),
    ctrl.Rule(homeAdominance['mediocre'] & awayAdominance['mediocre'], (homeW['average'], awayW['average'])),
    ctrl.Rule(homeAdominance['decent'] & awayAdominance['decent'], (homeW['average'], awayW['average'])),
    ctrl.Rule(homeDdominance['mediocre'] & awayDdominance['mediocre'], (homeW['average'], awayW['average'])),
    ctrl.Rule(homeDdominance['decent'] & awayDdominance['decent'], (homeW['average'], awayW['average'])),
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

    homeBasepred = simulator_result.output['Home Winning prediction']
    awayBasepred = simulator_result.output['Away Winning prediction']

    aproveitamentoHome = home_team_attack["Percentage of home points won"]
    aproveitamentoFora = away_team_attack["Percentage of away points won"]

    x = Result(
        output1 = homeBasepred + (aproveitamentoHome * homeBasepred), 
        output2 = awayBasepred + (aproveitamentoFora * awayBasepred)
    )
    return x
