from oemof.solph import views, processing
from co2_emissions import get_co2_emissions
import matplotlib.pyplot as plt
import oemof
import yaml


def plot_figures_for(element, title):
    figure, axes = plt.subplots(figsize=(10, 5))
    element["sequences"].plot(ax=axes, kind="line", drawstyle="steps-post")
    plt.title(title)
    plt.legend(
        loc="upper center",
        prop={"size": 8},
        bbox_to_anchor=(0.5, 1.25),
        ncol=2,
    )
    figure.subplots_adjust(top=0.8)


def plot_co2(co2_emissions, title):
    plt.clf()
    plt.plot(co2_emissions)
    plt.title(title)


def plot_result(energy_system, co2_emissions):
    main_results = energy_system.results['main']

    h2_storage = views.node(main_results, 'h2_storage')
    electricity_bus = views.node(main_results, 'electricity')
    steel = views.node(main_results, 'steel')
    steel_mill = views.node(main_results, 'steel_mill')
    electrolyzer = views.node(main_results, 'electrolyzer')
    # CO2 Emissions were calculated seperately, therefore already pd and forwarded to plot_co2

    plot_figures_for(electricity_bus, 'Electricity Bus')
    plot_figures_for(h2_storage, 'H2 Storage')
    plot_figures_for(steel, 'Steel Production')
    plot_figures_for(steel_mill, 'Steel Mill')
    plot_figures_for(electrolyzer, 'Electrolyzer')
    plot_co2(co2_emissions, "CO2 Emissions")
    plt.show()

def main():
    energy_system = oemof.solph.EnergySystem()
    energy_system.restore('C:\\Users\\ann82611\\ownCloud\\U-Platte\\04_Code\\hydrogen_hub\\h2_hub_minimalschnitt\\h2_hub_dumps', 'h2_hub_dump.oemof')
    
    # load config
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    

    co2_emissions = get_co2_emissions(energy_system, config)
    plot_result(energy_system, co2_emissions)


if __name__ == "__main__":
    main() 