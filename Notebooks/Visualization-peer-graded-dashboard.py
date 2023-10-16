#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard",style={'color':'#503D36', 'font-size':24, 'textAlign':'center'}),#May include style for title
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics ',
            placeholder='Select a report type ',
            style={'width':'80%','padding':'3px','font-size':'20px','textAlign':'center'}
        )
    ]),
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            style={'width':'80%','padding':'3px','font-size':'20px','textAlign':'center'}
        )
    ]),
    #Output Division
    html.Div([
    html.Div(id='output-container', className='chart-grid', style={'display':'flex','flex-wrap':'wrap'}),])
])

# CALLBACK 1
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))
def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

# CALLBACK 2
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), Input(component_id='dropdown-statistics', component_property='value')])
def update_output_container(input_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"))

#Plot 2 Calculate the average number of vehicles sold by vehicle type       
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                           
        R_chart2  = dcc.Graph(figure=px.bar(average_sales,x='Vehicle_Type',y='Automobile_Sales',title='Average number of vehicles sold by vehicle type Over Recession period'))
        
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        exp_rec= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()
        R_chart3 = dcc.Graph( figure = px.pie(
            exp_rec, values=exp_rec, names=exp_rec.index, title='Total expenditure share by vehicle type during recessions'
        ))

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        R_chart4 = dcc.Graph(figure=px.bar(
            recession_data, x='unemployment_rate',y='Automobile_Sales',color='Vehicle_Type',barmode='group',title='Effect of unemployment rate on vehicle type and sales'
        ))

        return [
            html.Div([html.Div(children=R_chart1),html.Div(children=R_chart2)],style={'display': 'flex'}),
            html.Div([html.Div(children=R_chart3),html.Div(R_chart4)],style={'display': 'flex'})
            ]

 # Yearly Statistic Report Plots                             
    elif (input_year and selected_statistics=='Yearly Statistics') :
        yearly_data = data[data['Year'] == input_year]
                                                            
#plot 1 Yearly Automobile sales using line chart for the whole period.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales',title='Yearly Automobile sales'))
            
# Plot 2 Total Monthly Automobile sales using line chart.
        Y_chart2 = dcc.Graph(figure=px.line(
            yearly_data, x='Month',y='Automobile_Sales', title='Total Monthly Automobile sales'
        ))

# Plot bar chart for average number of vehicles sold during the given year
        avr_vdata=yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean()
        Y_chart3 = dcc.Graph( figure = px.bar(avr_vdata,title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

# Total Advertisement Expenditure for each vehicle using pie chart
        exp_data=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()
        Y_chart4 = dcc.Graph(figure = px.pie(
            exp_data, values=exp_data, names=exp_data.index, title='Total Advertisement Expenditure for each vehicle type'
        ))

        return [
                html.Div([html.Div(Y_chart1),html.Div(Y_chart2)],style={'display': 'flex',}),
                html.Div([html.Div(Y_chart3),html.Div(Y_chart4)],style={'display': 'flex'})
                ]
        
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

