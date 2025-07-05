import plotly.express as px
from shiny import App, ui, render
from shinywidgets import output_widget, render_widget
import seaborn as sns
import matplotlib.pyplot as plt
from palmerpenguins import load_penguins

# Load data
penguins_df = load_penguins()

# UI
app_ui = ui.page_fluid(
    ui.h2("Penguin Data Explorer – Interactive Dashboard"),
    
    ui.layout_sidebar(
        ui.sidebar(
            ui.h2("Sidebar"),
            ui.input_selectize(
                "selected_attribute",
                "Choose a column:",
                ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
            ),
            ui.input_numeric(
                "plotly_bin_count",
                "Plotly Bin Count",
                10
            ),
            ui.input_slider(
                "seaborn_bin_count",
                "Seaborn Bin Count",
                1,
                100,
                5
            ),
            ui.input_checkbox_group(
                "selected_species_list",
                "Selected Species",
                ["Adelie", "Gentoo", "Chinstrap"],
                selected=["Adelie", "Gentoo", "Chinstrap"],
                inline=True
            ),
            ui.hr(),
            ui.a(
                "GitHub Repository",
                href="https://github.com/sabrouch36/cintel-02-data",
                target="_blank"
            )
        ),
        ui.layout_columns(
            ui.output_data_frame("penguin_data_table"),
            ui.output_data_frame("penguin_data_grid")
        ),
        ui.layout_columns(
            output_widget("plotly_piechart"),
            output_widget("plotly_scatterplot")
        ),
        ui.output_plot("seaborn_hist")
    )
)

# Server
def server(input, output, session):

    @output
    @render.data_frame
    def penguin_data_table():
        return render.DataTable(penguins_df, filters=True)

    @output
    @render.data_frame
    def penguin_data_grid():
        return render.DataGrid(penguins_df, filters=True)

    @output
    @render_widget
    def plotly_piechart():
        species_counts = penguins_df["species"].value_counts().reset_index()
        species_counts.columns = ["species", "count"]

        fig = px.pie(
            species_counts,
            names="species",
            values="count",
            title="Distribution of Penguin Species"
        )
        return fig

    @output
    @render_widget
    def plotly_scatterplot():
        df = penguins_df.dropna(subset=["flipper_length_mm", "body_mass_g", "species"])
        fig = px.scatter(
            df,
            x="flipper_length_mm",
            y="body_mass_g",
            color="species",
            title="Scatterplot: Flipper Length vs Body Mass"
        )
        return fig

    @output
    @render.plot
    def seaborn_hist():
        plt.figure(figsize=(8, 4))
        df = penguins_df.dropna(subset=["body_mass_g", "species"])
        sns.histplot(
            data=df,
            x="body_mass_g",
            hue="species",
            multiple="layer",
            bins=input.seaborn_bin_count()
        )
        plt.title("Seaborn Histogram of Body Mass by Species")
        plt.xlabel("Body Mass (g)")
        plt.ylabel("Count")
        return plt.gcf()

# Run the app
app = App(app_ui, server)
