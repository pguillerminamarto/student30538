from shiny import App, render, ui
import matplotlib.pyplot as plt
import numpy as np

app_ui = ui.page_fluid(
    ui.panel_title("Histogram of 200 Draws from Normal with mean mu"),
    ui.input_slider("mu", "mean mu", 0, 100, 20), 
    ui.output_plot("my_hist"),
    ui.output_text_verbatim("my_sumstats"),
    ui.input_radio_buttons(
        "data_type",  # id for the radio buttons
        "Choose Data to Display",  # label for the radio buttons
        choices={"cases": "Cases", "deaths": "Deaths"},  # options for the user
        selected="cases"  # default selection
    )
)

def server(input, output, session):
    @render.plot
    def my_hist():
        sample = np.random.normal(input.n(), 20, 200)
        fig, ax = plt.subplots()
        ax.hist(sample, bins=30, color='blue', alpha=0.7)
        return fig
    
def my_sumstats():
    sample = np.random.normal(input.n(), 20, 100)
    min = np.min(sample)
    max = np.max(sample)
    median = np.median(sample)
    return "Min:" + str(min) + ", Median: " + str(median), ", Max: " + str(max)

@render.plot
def ts():
    df = subsetted_data()
    if input.outcome() == "Cases": #begin new code
        series = df['cases']       #
    if input.outcome() == "Deaths":#
        series = df['deaths']      # end new code
    fig, ax = plt.subplots(figsize=(3,6))
    ax.plot(df['date'], series)
    ax.tick_params(axis = 'x', rotation = 45)
    ax.set_xlabel('Date')
    ax.set_ylabel(input.outcome())
    ax.set_title(f'COVID-19 {input.outcome()} in {input.state()}')
    ax.set_yticklabels(['{:,}'.format(int(x)) for x in ax.get_yticks()])
    return fig

app = App(app_ui, server)
