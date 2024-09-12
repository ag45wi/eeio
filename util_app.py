import pandas as pd
from textwrap import wrap
import plotly
import streamlit as st
import os

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


def save_toGit(in_df, in_fupload):

    def get_file_sha(file_name, GITHUB_REPO, GITHUB_TOKEN, GITHUB_BRANCH):
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_name}?ref={GITHUB_BRANCH}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            file_data = response.json()
            return file_data['sha']  # Return the file's SHA
        elif response.status_code == 404:
            return None  # File doesn't exist
        else:
            st.error(f"Error fetching file info: {response.json()}")
            return None


    #https://chatgpt.com/c/66e23381-e364-8005-ba67-3f936287559c
    import base64
    import requests

    print("Inside save_toGit")
    # GitHub repository details
    repo = 'ag45wi/eeio'
    branch = 'main'
    token = os.getenv('GITHUB_TOKEN') 

    path_name='data/'+in_fupload.name
    #path_name=in_fupload.name
    print("path_name",path_name)

    #this one is ok
    file_content=in_fupload.getvalue()
    encoded_content=base64.b64encode(file_content).decode()

    #in_df.to_excel(path_name, index=False)

    # Read the Excel file as binary and encode in base64
    #with open(path_name, 'rb') as file:
    #    encoded_content = base64.b64encode(file.read()).decode()

    # GitHub API URL to upload the file
    url = f'https://api.github.com/repos/{repo}/contents/{path_name}'
    #url = f'https://api.github.com/repos/{repo}/contents/test_io.xlsx'

    from datetime import datetime
    now = datetime.now()
    curr_date_time = now.strftime("%Y-%m-%d_%H.%M.%S")
    # Data to send to the API
    data = {
        'message': f'Update {curr_date_time}',
        'content': encoded_content,
        'branch': branch
    }

    # Headers including your GitHub token
    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    }

    file_sha = get_file_sha(path_name, repo, token, branch)
    if file_sha:
        print("sha: ", file_sha)
        data["sha"] = file_sha

    # Make the PUT request to upload the file
    response = requests.put(url, json=data, headers=headers)

    if response.status_code in [200, 201]:
        print('File successfully uploaded!')
    else:
        print(f'Failed to upload file: {response.json()}')


def save_toGit_xls(in_df, in_fname):

    def get_file_sha(file_name, GITHUB_REPO, GITHUB_TOKEN, GITHUB_BRANCH):
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_name}?ref={GITHUB_BRANCH}"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            file_data = response.json()
            return file_data['sha']  # Return the file's SHA
        elif response.status_code == 404:
            return None  # File doesn't exist
        else:
            st.error(f"Error fetching file info: {response.json()}")
            return None

    # Function to convert DataFrame to an in-memory Excel file
    def dataframe_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()  # Get the Excel data in bytes

    #https://chatgpt.com/c/66e23381-e364-8005-ba67-3f936287559c
    import base64
    import requests
    from io import BytesIO

    print("Inside save_toGit_xls")
    # GitHub repository details
    repo = 'ag45wi/eeio'
    branch = 'main'
    token = os.getenv('GITHUB_TOKEN') 
        #export GITHUB_TOKEN='your_personal_access_token' -> Unix
        #set GITHUB_TOKEN='your_personal_access_token' -> in windows, eg use control panel -> env vars
    
    path_name='data/'+in_fname
    #path_name=in_fupload.name
    print("path_name",path_name)
    print("token", token)

    #this one is ok
    #file_content=in_fupload.getvalue()
    #encoded_content=base64.b64encode(file_content).decode()

    file_content = dataframe_to_excel(in_df)
    encoded_content=base64.b64encode(file_content).decode()
    #in_df.to_excel(path_name, index=False)

    # Read the Excel file as binary and encode in base64
    #with open(path_name, 'rb') as file:
    #    encoded_content = base64.b64encode(file.read()).decode()

    # GitHub API URL to upload the file
    url = f'https://api.github.com/repos/{repo}/contents/{path_name}'
    #url = f'https://api.github.com/repos/{repo}/contents/test_io.xlsx'

    from datetime import datetime
    now = datetime.now()
    curr_date_time = now.strftime("%Y-%m-%d_%H.%M.%S")
    # Data to send to the API
    data = {
        'message': f'Update {curr_date_time}',
        'content': encoded_content,
        'branch': branch
    }

    # Headers including your GitHub token
    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    }

    file_sha = get_file_sha(path_name, repo, token, branch)
    if file_sha:
        print("sha: ", file_sha)
        data["sha"] = file_sha

    # Make the PUT request to upload the file
    response = requests.put(url, json=data, headers=headers)

    if response.status_code in [200, 201]:
        print('File successfully uploaded!')
    else:
        print(f'Failed to upload file: {response.json()}')



#MAIN, executed if run independently------------------------------------------------------
if __name__ == "__main__":
    df_agg_sectors_each=get_aggregate_each()

    df_agg_sectors_each.to_excel("buf/result_agg_sectors_each.xlsx")
    print(df_agg_sectors_each.head(5))
