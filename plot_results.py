from oemof.solph import views, processing
# import pprint as pp
import matplotlib.pyplot as plt
import oemof


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
    #plt.show()


def plot_result(energy_system):
    main_results = energy_system.results['main']
    #pp.pprint(main_results)

    h2_storage = views.node(main_results, 'h2_storage')
    electricity_bus = views.node(main_results, 'electricity')
    steel = views.node(main_results, 'steel')
    steel_mill = views.node(main_results, 'steel_mill')
    electrolyzer = views.node(main_results, 'electrolyzer')
    co2_emissions = views.node(main_results, 'co2_emissions_bus')

    plot_figures_for(electricity_bus, 'Electricity Bus')
    # plot_figures_for(h2_storage, 'H2 Storage')
    # #plot_figures_for(steel, 'Steel Production')
    # plot_figures_for(steel_mill, 'Steel Mill')
    
    # plot_figures_for(electrolyzer, 'Electrolyzer')
    # plot_figures_for(co2_emissions, "CO2 Emissions")
    # print(energy_system)
    #print(main_results)
    plt.show()

def main():
    energy_system = oemof.solph.EnergySystem()
    energy_system.restore('C:\\Users\\ann82611\\ownCloud\\U-Platte\\04_Code\\hydrogen_hub\\h2_hub_minimalschnitt\\h2_hub_dumps', 'h2_hub_dump.oemof')
    
    plot_result(energy_system)


if __name__ == "__main__":
    main() 