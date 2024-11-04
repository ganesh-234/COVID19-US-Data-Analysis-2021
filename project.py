import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load data
df = pd.read_csv(r"C:\Users\hp\Desktop\Projects\Project\COVID19-all-states.csv")


# Convert date column to datetime format for accurate filtering and plotting
df["date"] = pd.to_datetime(df["date"])


# Function to visualize case trend for each state.
def state_trend(df):
    state_cases = df.groupby(["state", "date"])["hospitalized"].sum().reset_index()
    plt.figure(figsize=(20, 10))
    sns.lineplot(x="date", y="hospitalized", hue="state", data=state_cases)
    plt.title("COVID-19 Hospitalizations by State")
    plt.show()


# Function to plot death rate by state.
def state_death_rate(df):
    state_death = df.groupby("state")["deathConfirmed"].mean().reset_index()
    plt.figure(figsize=(20, 10))
    sns.barplot(x="state", y="deathConfirmed", data=state_death)
    plt.title("COVID-19 Death Rate by State")
    plt.show()


# Plotly Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div(
    [
        dcc.Dropdown(
            id="state-dropdown",
            options=[
                {"label": state, "value": state} for state in df["state"].unique()
            ],
            value="NY",
        ),
        dcc.Graph(id="state-cases"),
        dcc.Graph(id="state-death-rate"),
    ]
)


# Callback to update case trend graph based on selected state
@app.callback(Output("state-cases", "figure"), Input("state-dropdown", "value"))
def update_cases(state):
    state_cases = (
        df[df["state"] == state].groupby("date")["hospitalized"].sum().reset_index()
    )
    fig = px.line(state_cases, x="date", y="hospitalized")
    fig.update_layout(title=f"COVID-19 Hospitalizations in {state}")
    return fig


# Callback to update death rate graph based on selected state
@app.callback(Output("state-death-rate", "figure"), Input("state-dropdown", "value"))
def update_death_rate(state):
    # Filter data for the selected state
    state_death = (
        df[df["state"] == state].groupby("state")["deathConfirmed"].mean().reset_index()
    )
    fig = px.bar(state_death, x="state", y="deathConfirmed")
    fig.update_layout(title=f"COVID-19 Death Rate in {state}")
    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
