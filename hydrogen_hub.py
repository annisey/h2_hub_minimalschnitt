import oemof.solph as solph
from oemof.solph.components import Sink, Source, Converter, GenericStorage
from oemof.solph import create_time_index, Bus, Flow, Model, processing

#for plotting
from plot_graph import plot_energy_system
# import pprint as pp
from plot_results import plot_result
 
#for config file and opening data
import yaml
import pandas as pd

import sys

#load config file (where parameters are set)
def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def get_csv_data(data_path, column_name):
    df = pd.read_csv(data_path)
    fixed_value = df[column_name]
    return fixed_value


def create_energy_system(config):

    index = create_time_index(2019) #range of a year, hourly

    #create system
    h2_hub = solph.EnergySystem(timeindex=index, infer_last_interval=False) #einlesen ob infer_last_interval true or false

    #add buses
    electricity_bus = Bus(label='electricity') 
    h2_bus = Bus(label='h2_bus') 
    co2_emissions_bus = Bus(label='co2_emissions_bus')

    h2_hub.add(electricity_bus, h2_bus, co2_emissions_bus)

    #open and get data from csv
    pv_data = get_csv_data(config['pv_data_path'], config['pv_data_column']) 
    wind_data = get_csv_data(config['wind_data_path'], config['wind_data_column'])

    #add sources
    pv_source = Source(label='pv', outputs={electricity_bus: Flow(fix=pv_data, nominal_value=config['pv_nominal_value'], variable_costs=config['pv_variable_costs'])})
    wind_source = Source(label='wind', outputs={electricity_bus: Flow(fix=wind_data, nominal_value=config['wind_nominal_value'],variable_costs=config['wind_variable_costs'])})
    grid_source = Source(label='grid', outputs={electricity_bus: Flow(nominal_value=config['grid_nominal_value'], variable_costs=config['grid_variable_costs']),
                                                co2_emissions_bus: Flow(nominal_value=(config['grid_nominal_value']*config['co2_emissions']))})

    h2_ship_source = Source(label='h2_ship', outputs={h2_bus:Flow(nominal_value=config['h2_ship_nominal_value'], variable_costs=config['h2_ship_variable_costs'])}) 
    electrolyzer = Converter(label='electrolyzer', inputs={electricity_bus: Flow(nominal_value=config['electrolyzer_nominal_value'], variable_costs=config['electrolyzer_variable_costs'])},
                             outputs={h2_bus: Flow()},
                             conversion_factors={electricity_bus: config['electrolyzer_nominal_value'] / config['h2_produced']})

    h2_hub.add(pv_source, wind_source, grid_source, h2_ship_source, electrolyzer)

    #add storage
    h2_storage = GenericStorage(label= 'h2_storage',
                                inputs={h2_bus: Flow()},
                                outputs={h2_bus: Flow()},
                                loss_rate=config['h2_storage_loss_rate'],
                                nominal_storage_capacity=config['h2_storage_nominal_storage_capacity'])
    steel = Sink(label='steel')

    h2_hub.add(h2_storage, steel)

    #add sink
    steel_mill = Converter(label='steel_mill',
                           inputs={h2_bus: Flow(), electricity_bus: Flow()},
                           outputs={steel: Flow(nominal_value =config['steel_produced'], variable_costs=config['steel_price'])},
                           conversion_factors={h2_bus: config['h2_for_steel'],  # Wasserstoff pro kg Stahl
                                               electricity_bus: config['electricity_for_steel']})  # Strom pro kg Stahl
                           
    
    
    electricity_slack = Sink(label='electricity_slack', inputs={electricity_bus: Flow(variable_costs=config['electricity_slack_variable_costs'])})
    co2_emissions = Sink(label='co2_emissions', inputs= {co2_emissions_bus: Flow(nominal_value=(config['grid_nominal_value']*config['co2_emissions']))})

    h2_hub.add(steel_mill, electricity_slack, co2_emissions)

    return h2_hub


def optimizer(energy_system, config):
    model = Model(energy_system)
    model.solve(solver=config['solver']) # "solve_kwargs={'tee': True}" to display solver's output
    energy_system.results['main'] = processing.results(model) # data components and flows
    energy_system.results['meta'] = processing.meta_results(model) #data solvers
    # Dump the energy system including the results (saving) for later analyzing of the results without running the whole code
    energy_system.dump('C:\\Users\\ann82611\\ownCloud\\U-Platte\\04_Code\\hydrogen_hub\\h2_hub_minimalschnitt\\h2_hub_dumps', 'h2_hub_dump_1.oemof')
    return energy_system


def main():
    config = load_config('config.yaml') #enter relative file path config file
    h2_hub = create_energy_system(config)   
    h2_hub = optimizer(h2_hub, config) #Ergebnisse sind unter .results gespeichert
    # plot_energy_system(h2_hub)
    plot_result(h2_hub)

if __name__ == "__main__":
    main() 
