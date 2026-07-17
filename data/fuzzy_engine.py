import numpy as np
import skfuzzy as fuzz

from skfuzzy import control as ctrl

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

#Control sub system
ballPossesion = ctrl.Antecedent(np.arange(0,11,1), 'Ball possesion')

#Functions 
goalsAttack.automf(3)
chancesAttack.automf(3)
cornersAttack.automf(3)
goalsDefense.automf(3)
chancesDefense.automf(3)
cornersDefense.automf(3)
ballPossesion.automf(3)

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
    ctrl.Rule(ballPossesion['good'] & chancesAttack['good'] & cornersAttack['good'], offensiveDominance['good']),
    ctrl.Rule(ballPossesion['poor'] & chancesAttack['good'] & goalsAttack['average'], offensiveDominance['average']),
    ctrl.Rule(goalsAttack['average'] & chancesAttack['average'], offensiveDominance['average']),
    ctrl.Rule(ballPossesion['average'] & chancesAttack['average'] & cornersAttack['average'], offensiveDominance['average']),
    ctrl.Rule(ballPossesion['good'] & chancesAttack['poor'] & goalsAttack['poor'], offensiveDominance['poor']),
    ctrl.Rule(goalsAttack['poor'] & chancesAttack['average'], offensiveDominance['poor']),
    ctrl.Rule(goalsAttack['poor'] & chancesAttack['poor'] & cornersAttack['poor'], offensiveDominance['very poor'])
]

rules_defense = [
    ctrl.Rule(goalsDefense['poor'] & chancesDefense['poor'], defensiveDominance['good']),
    ctrl.Rule(ballPossesion['good'] & chancesDefense['poor'] & cornersDefense['poor'], defensiveDominance['good']),
    ctrl.Rule(ballPossesion['poor'] & goalsDefense['poor'] & chancesDefense['average'], defensiveDominance['average']),
    ctrl.Rule(goalsDefense['average'] & chancesDefense['average'], defensiveDominance['average']),
    ctrl.Rule(ballPossesion['good'] & chancesDefense['good'], defensiveDominance['poor']),
    ctrl.Rule(goalsDefense['good'] | chancesDefense['good'], defensiveDominance['poor']),
    ctrl.Rule(goalsDefense['good'] & chancesDefense['good'] & cornersDefense['good'], defensiveDominance['very poor']),
    ctrl.Rule(ballPossesion['poor'] & goalsDefense['good'] & chancesDefense['good'], defensiveDominance['very poor'])
]

attack_control_sys = ctrl.ControlSystem(rules_attack)
defense_control_sys = ctrl.ControlSystem(rules_defense)


simulator_attack = ctrl.ControlSystemSimulation(attack_control_sys)
simulator_defense = ctrl.ControlSystemSimulation(defense_control_sys)
