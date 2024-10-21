from oemof.solph import views, processing
import pandas as pd
import matplotlib.pyplot as plt
import oemof
import yaml

def get_co2_emissions(energy_system, config):
     results_main = energy_system.results['main']
     results = pd.Series(results_main)
     flow_grid = results.loc[(energy_system.node['grid'], energy_system.node['electricity'])]['sequences']

     co2_emissions = flow_grid * config['co2_emissions']
     return co2_emissions



def main():
    energy_system = oemof.solph.EnergySystem()
    energy_system.restore('C:\\Users\\ann82611\\ownCloud\\U-Platte\\04_Code\\hydrogen_hub\\h2_hub_minimalschnitt\\h2_hub_dumps', 'h2_hub_dump_1.oemof')
    # load config
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    co2_emissions = get_co2_emissions(energy_system, config)


if __name__ == "__main__":
    main() 