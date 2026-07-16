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
possesionDominance = ctrl.Consequent(np.arange(0,11,1), 'Possesion dominance')

#Attack system rules
attackRule1 = ctrl.Rule(goalsAttack['low'] & chancesAttack['low'] & cornersAttack['low'], offensiveDominance['very low'])