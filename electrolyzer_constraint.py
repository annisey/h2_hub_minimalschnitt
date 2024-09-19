from pyomo.core import Constraint #benutzerdefinierter Constraint
import oemof.solph as solph


# electrolyzer shall only run if steel mill is covered with power

def limit_electrolyzer_flow(model):
   # access components of modell
   electricity_bus = model.groups['electricity'] 
   steel_mill = model.groups['steel_mill']
   electrolyzer = model.groups['electrolyzer']

   # define solph.model (mathematical model, enthält Variablen, Gleichungen, Constraints)
   model = solph.Model(model)

   # Stelle sicher, dass du auf die nominalen Werte zugreifst, wenn nötig
   steel_max_flow = steel_mill.inputs[electricity_bus].nominal_value  # Maximaler nominaler Wert für den Fluss

   for t in model.TIMESTEPS:
      el_steel_flow = model.flows[electricity_bus, steel_mill]
      el_electrolyzer_flow = model.flows[electricity_bus, electrolyzer]

      # constraint: electricity only running, if steel mill is covered by power
      model.electrolyzer_constraint = Constraint(
          expr=el_electrolyzer_flow <= el_steel_flow * (1 / steel_max_flow))
    
   #print(model.flow.keys())

