import numpy as np
import skfuzzy as fuzz

from skfuzzy import control as ctrl
from dataclasses import dataclass

@dataclass
class Result:
    output1: float
    output2: float

#Attack sub system
goalsAttack = ctrl.Antecedent(np.arange(0,11,1), 'Goal scored per game')
chancesAttack = ctrl.Antecedent(np.arange(0,11,1), 'Big chances created per game')
cornersAttack = ctrl.Antecedent(np.arange(0,11,1), 'Offensive corners earned per game')
offensiveDominance = ctrl.Consequent(np.arange(0,11,1), 'Offensive dominance')

#Defensive sub system
goalsDefense = ctrl.Antecedent(np.arange(0,11,1), 'Goal suffered per game')
chancesDefense= ctrl.Antecedent(np.arange(0,11,1), 'Big chances conceded per game')
cornersDefense = ctrl.Antecedent(np.arange(0,11,1), 'Defensive corners earned per game')
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
chancesAttack.automf(3)
cornersAttack.automf(3)
goalsDefense.automf(3)
chancesDefense.automf(3)
cornersDefense.automf(3)
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
    ctrl.Rule(goalsAttack['good'] & chancesAttack['good'], offensiveDominance['good']),
    ctrl.Rule(chancesAttack['good'] & cornersAttack['good'], offensiveDominance['good']),
    ctrl.Rule(chancesAttack['good'] & goalsAttack['average'], offensiveDominance['average']),
    ctrl.Rule(goalsAttack['average'] & chancesAttack['average'], offensiveDominance['average']),
    ctrl.Rule(chancesAttack['average'] & cornersAttack['average'], offensiveDominance['average']),
    ctrl.Rule(chancesAttack['poor'] & goalsAttack['poor'], offensiveDominance['poor']),
    ctrl.Rule(goalsAttack['poor'] & chancesAttack['average'], offensiveDominance['poor']),
    ctrl.Rule(goalsAttack['poor'] & chancesAttack['poor'] & cornersAttack['poor'], offensiveDominance['very poor'])
]


rules_defense = [
    ctrl.Rule(goalsDefense['poor'] & chancesDefense['poor'], defensiveDominance['good']),
    ctrl.Rule(chancesDefense['poor'] & cornersDefense['poor'], defensiveDominance['good']),
    ctrl.Rule(goalsDefense['poor'] & chancesDefense['average'], defensiveDominance['average']),
    ctrl.Rule(goalsDefense['average'] & chancesDefense['average'], defensiveDominance['average']),
    ctrl.Rule(chancesDefense['good'], defensiveDominance['poor']),
    ctrl.Rule(goalsDefense['good'] | chancesDefense['good'], defensiveDominance['poor']),
    ctrl.Rule(goalsDefense['good'] & chancesDefense['good'] & cornersDefense['good'], defensiveDominance['very poor']),
    ctrl.Rule(goalsDefense['good'] & chancesDefense['good'], defensiveDominance['very poor'])
]

rules_result = [
    ctrl.Rule(homeAdominance['good'] & awayDdominance['poor'], homeW['good']),
    ctrl.Rule(homeAdominance['good'] & awayDdominance['poor'], awayW['poor']),
    
    ctrl.Rule(awayAdominance['good'] & homeDdominance['poor'], awayW['good']),
    ctrl.Rule(awayAdominance['good'] & homeDdominance['poor'], homeW['poor']),
    
    ctrl.Rule(homeDdominance['good'] & awayAdominance['poor'], homeW['good']),
    ctrl.Rule(homeDdominance['good'] & awayAdominance['poor'], awayW['poor']),
    
    ctrl.Rule(awayDdominance['good'] & homeAdominance['poor'], awayW['good']),
    ctrl.Rule(awayDdominance['good'] & homeAdominance['poor'], homeW['poor']),
    
    ctrl.Rule(homeAdominance['average'] & awayDdominance['average'], homeW['average']),
    ctrl.Rule(awayAdominance['average'] & homeDdominance['average'], awayW['average']),
    
    ctrl.Rule(homeAdominance['good'] & awayDdominance['good'], homeW['average']),
    ctrl.Rule(awayAdominance['good'] & homeDdominance['good'], awayW['average']),
    
    ctrl.Rule(homeAdominance['poor'] & awayDdominance['poor'], homeW['average']),
    ctrl.Rule(awayAdominance['poor'] & homeDdominance['poor'], awayW['average'])
]

attack_control_sys = ctrl.ControlSystem(rules_attack)
defense_control_sys = ctrl.ControlSystem(rules_defense)
result_control_sys = ctrl.ControlSystem(rules_result)

simulator_attack = ctrl.ControlSystemSimulation(attack_control_sys)
simulator_defense = ctrl.ControlSystemSimulation(defense_control_sys)
simulator_result = ctrl.ControlSystemSimulation(result_control_sys)

def calculate_fuzzy_prediction(home_team_attack, home_team_defense, away_team_attack, away_team_defense):
    simulator_attack.input['Goal scored per game'] = home_team_attack["goals_scored_per_game"]
    simulator_attack.input['Big chances created per game'] = home_team_attack["shots_pro"]
    simulator_attack.input['Offensive corners earned per game'] = home_team_attack["corners_pro"]
    simulator_defense.input['Goal suffered per game'] = home_team_defense["goals_suffered_per_game"]
    simulator_defense.input['Big chances conceded per game'] = home_team_defense["shots_against"]
    simulator_defense.input['Defensive corners earned per game'] = home_team_defense["corners_against"]
    simulator_attack.compute()
    simulator_defense.compute()
    simulator_result.input['Home team offensive dominance'] = simulator_attack.output['Offensive dominance']
    simulator_result.input['Home team defensive dominance'] = simulator_defense.output['Defensive dominance']


    simulator_attack.input['Goal scored per game'] = away_team_attack["goals_scored_per_game"]
    simulator_attack.input['Big chances created per game'] = away_team_attack["shots_pro"]
    simulator_attack.input['Offensive corners earned per game'] = away_team_attack["corners_pro"]
    simulator_defense.input['Goal suffered per game'] = away_team_defense["goals_suffered_per_game"]
    simulator_defense.input['Big chances conceded per game'] = away_team_defense["shots_against"]
    simulator_defense.input['Defensive corners earned per game'] = away_team_defense["corners_against"]
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





