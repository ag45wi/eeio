import pandas as pd
from textwrap import wrap
import plotly

def get_aggregate_each ():
    df_emission = pd.read_excel("buf/result_emission.xlsx")
    df_io = pd.read_excel("data/io_ind_2016.xlsx")

    cnf_sector=df_emission.shape[0]
    df_sector=df_io[["Sector_CodeName"]]
    df_sector=df_sector.head(cnf_sector)

    df_emission["Sector_CodeName"]=df_sector.values.ravel()

    file_path_AGG = 'data/aggregated_sectors.xlsx'
    df_agg_label= pd.read_excel(file_path_AGG)

    df_emission=pd.merge(df_emission, df_agg_label, on='Sector_CodeName')

    return df_emission

def customwrap(s,in_width=40):
    return "<br>".join(wrap(s,width=in_width))

def plot_agg_each(df, agg_label):
    import streamlit as st
    import plotly.graph_objects as go

    # Sample data for the stacked bar chart
    categories = df[['Sector_CodeName']].values.ravel()
    group_a = df[['emissionScope1']].values.ravel()
    group_b = df[['emissionScope2']].values.ravel()
    group_c = df[['emissionScope3']].values.ravel()

    # Create a horizontal stacked bar chart
    fig = go.Figure()

    categories = [ '<br>'.join(wrap(l, 50)) for l in categories ]
    #categories = list(map(customwrap,categories))
    #print("categories", categories)

    #colors = plotly.colors.qualitative.Prism

    # Add traces for each group
    fig.add_trace(go.Bar(y=categories, x=group_a, name='emission Scope 1', orientation='h'))
    fig.add_trace(go.Bar(y=categories, x=group_b, name='emission Scope 2', orientation='h'))
    fig.add_trace(go.Bar(y=categories, x=group_c, name='emission Scope 3', orientation='h'))

    # Update the layout for stacked bars
    fig.update_layout(
        barmode='stack',
        title='Emmision of Sectors in Category: '+agg_label ,
        xaxis_title='Emission in T CO2',
        yaxis_title='I/O Sector in '+agg_label + ' Category'
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)


def plot_agg(df):
    import streamlit as st
    import plotly.graph_objects as go

    df = df.sort_values("total_Emission", ascending=True)

    # Sample data for the stacked bar chart
    #categories = df[['Aggregated sectors']].values.ravel()
    categories = df.index.values
    group_a = df[['scope1_Emission']].values.ravel()
    group_b = df[['scope2_Emission']].values.ravel()
    group_c = df[['scope3_Emission']].values.ravel()

    categories = [ '\n'.join(wrap(l, 25)) for l in categories ]

    # Create a horizontal stacked bar chart
    fig = go.Figure()

    # Add traces for each group
    fig.add_trace(go.Bar(y=categories, x=group_a, name='emission Scope 1', orientation='h'))
    fig.add_trace(go.Bar(y=categories, x=group_b, name='emission Scope 2', orientation='h'))
    fig.add_trace(go.Bar(y=categories, x=group_c, name='emission Scope 3', orientation='h'))

    # Update the layout for stacked bars
    fig.update_layout(
        barmode='stack',
        title='Emmision by Aggregate of Sectors',
        xaxis_title='Emission in T CO2',
        yaxis_title='Aggregate of Sectors'
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)


#MAIN, executed if run independently------------------------------------------------------
if __name__ == "__main__":
    df_agg_sectors_each=get_aggregate_each()

    df_agg_sectors_each.to_excel("buf/result_agg_sectors_each.xlsx")
    print(df_agg_sectors_each.head(5))