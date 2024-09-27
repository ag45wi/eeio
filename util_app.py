import pandas as pd
import os

def get_lst_agg():
    cwd = os.getcwd()
    #cwd="/home/inovasi9/app_eeio"
    
    fpath = cwd+"/static/data/list_agg_sectors.csv"
    df_lagg = pd.read_csv(fpath)
    #print("df_lagg", df_lagg.head(5))
    lst = df_lagg['Aggregated sectors'].tolist()
    lst.insert(0, "--All_Sectors--")

    return lst

def generate_chart_agg(in_agg):
    import plotly.graph_objects as go
    from textwrap import wrap
    from urllib.parse import unquote

    #print("inside generate_chart_agg::in_agg", in_agg)

    in_agg = unquote(in_agg)
    
    cwd = os.getcwd()
    #cwd="/home/inovasi9/app_eeio"

    #if (in_agg == "--All%20Sectors--"): in_agg = "--All Sectors--"
    
    if ((in_agg == "--All_Sectors--") or (in_agg == "")):
        saved_file_path = cwd+"/static/buf/result_agg_sectors.csv"
        df = pd.read_csv(saved_file_path)
        #df.set_index('Aggregated sectors', inplace=True)
        categories = df[['Aggregated sectors']].values.ravel()
        group_a = df[['scope1_Emission']].values.ravel()
        group_b = df[['scope2_Emission']].values.ravel()
        group_c = df[['scope3_Emission']].values.ravel()

        title_VAL='Emmision by Aggregate of Sectors'
        yaxis_title_VAL="Aggregate of Sectors"
    else:
        saved_file_path = cwd+"/static/buf/result_agg_sectors_each.csv"
        df1 = pd.read_csv(saved_file_path)
        df=df1[df1["Aggregated sectors"] == in_agg]
        categories = df[['Sector_CodeName']].values.ravel()
        group_a = df[['emissionScope1']].values.ravel()
        group_b = df[['emissionScope2']].values.ravel()
        group_c = df[['emissionScope3']].values.ravel()

        title_VAL='Emmision of Sectors in Category: '+in_agg
        yaxis_title_VAL='I/O Sector in category: '+in_agg 

    #categories = [ '\n'.join(wrap(l, 25)) for l in categories ]
    categories = [ '<br>'.join(wrap(l, 50)) for l in categories ]

    fig = go.Figure()

    # Add traces for each group
    fig.add_trace(go.Bar(y=categories, x=group_a, name='emission Scope 1', orientation='h'))
    fig.add_trace(go.Bar(y=categories, x=group_b, name='emission Scope 2', orientation='h'))
    fig.add_trace(go.Bar(y=categories, x=group_c, name='emission Scope 3', orientation='h'))

    # Update the layout for stacked bars
    fig.update_layout(
        barmode='stack',
        title=title_VAL,
        xaxis_title='Emission in T CO2',
        yaxis_title=yaxis_title_VAL
    )

    return fig

#https://www.tutorialspoint.com/how-to-delete-all-files-in-a-directory-with-python
def delete_files_in_directory(directory_path):
    print("inside delete_files_in_directory")
    files = os.listdir(directory_path)
    for file in files:
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def get_df_input():
    cwd = os.getcwd()
    folder_path = f'{cwd}/static/data'

    fname_io="io_ind_2016.csv"
    fname_fec="final_energy_consumption_bytype.csv"
    fname_conv="conversion_factor.csv"
    fname_co2="direct_CO2_EF.csv"

    file_path=f"{folder_path}/{fname_io}"
    df_io = pd.read_csv(file_path, index_col=False)
    df_io.columns = df_io.columns.str[:10]

    file_path=f"{folder_path}/{fname_fec}"
    df_fec = pd.read_csv(file_path, index_col=False)

    file_path=f"{folder_path}/{fname_conv}"
    df_conv = pd.read_csv(file_path, index_col=False)

    file_path=f"{folder_path}/{fname_co2}"
    df_co2 = pd.read_csv(file_path, index_col=False)

    return df_io, df_fec, df_conv, df_co2
    

if __name__ == '__main__':

    if (0):
        lst=get_lst_agg()
        print("lst", lst)

        #--------------------------
        fig=generate_chart_agg()
        #fig.show()
        img = io.BytesIO()
        fig.savefig(img, format='png')

