import numpy as np
import pandas as pd

def calc_matrix_A (X_io, X_total):
    #print("inside calc_matrix_A")

    mat_A=np.divide(X_io,X_total)
    
    #print(mat_A.shape, X_total.shape)
    #print(mat_A[:5,:5])
    #print(X_total)

    return mat_A

def get_mat_finEnerCons(mat_A, X_FEC_yr):
    #FEC: final energy consumption

    #https://stackoverflow.com/questions/71443487/how-to-extract-non-consecutive-rows-and-columns-of-a-matrix

    rows=np.array([36, 37, 38, 144])
    #print("rows", rows)
    X1=mat_A[rows,:]

    total_1_axis = np.sum(X1, axis=1)
    #print(f'Sum of elements at 1-axis is {total_1_axis}')

    #https://stackoverflow.com/questions/35661919/numpy-array-divide-column-by-vector
    divider=total_1_axis.reshape(-1,1) 
    X1_div=np.divide(X1, divider)

    mult=X_FEC_yr.reshape(-1,1)
    X1_mult=np.multiply(X1_div,mult)
    #print("mult", mult)

    #print ("X1", X1[:,:5])
    #print ("X1_div", X1_div[:,:5])
    #print ("X1_mult", X1_mult[:,:5])
    return X1_mult

def get_mat_finCons(finEnerCons, convFactor):
    div1=convFactor.reshape(-1,1)
    X1_div=np.divide(finEnerCons,div1)
    X1_div=np.multiply(X1_div,1000)
    #print("div1", div1)

    #print ("X1", X1[:,:5])
    #print ("X1_div", X1_div[:,:5])
    #print ("X1_mult", X1_mult[:,:5])
    return X1_div

def get_mat_finConsCO2(finCons, CO2_EF):

    #print("CO2_EF", CO2_EF, CO2_EF.shape)

    #coal
    #=(B7*1000)*'Direct CO2 emission factor'!$B$9*'Direct CO2 emission factor'!$C$9
    row1=np.multiply(finCons[0,:],1000)
    row1=np.multiply(row1,CO2_EF[0,0])
    row1=np.multiply(row1,CO2_EF[0,1])

    #fuel
    #=B8*'Direct CO2 emission factor'!$B$16*'Direct CO2 emission factor'!$C$16
    row2=np.multiply(finCons[1,:],CO2_EF[1,0])
    row2=np.multiply(row2,CO2_EF[1,1])

    #nat gas
    #=B9*26.8*('Direct CO2 emission factor'!$B$14/1000)*'Direct CO2 emission factor'!$C$14
    row3=np.multiply(finCons[2,:],26.8)
    row3=np.multiply(row3,CO2_EF[2,0])
    row3=np.divide(row3,1000)
    row3=np.multiply(row3,CO2_EF[2,1])

    #electricity
    #=(B10*'Direct CO2 emission factor'!$B$24)*1000000
    row4=np.multiply(finCons[3,:],CO2_EF[3,0])
    row4=np.multiply(row4,1000000)

    mat_co2=np.vstack((row1,row2,row3,row4))

    #print("shape", mat_co2.shape)

    #print ("mat_co2", mat_co2[:,:5])

    return mat_co2

def get_io_aggregate(df_io, df_agg_label, totEm, scope1, scope2, scope3):
    #https://www.geeksforgeeks.org/pandas-groupby-and-sum/
    #https://stackoverflow.com/questions/37697195/how-to-merge-two-data-frames-based-on-particular-column-in-pandas-python
    #https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/

    cnf_sector=df_agg_label.shape[0]
    #print("cnf_sector", cnf_sector)

    #df_agg_io=df_io[["Sector_Code",	"Sector_Name", "Sector_CodeName"]]
    df_agg_io=df_io[["Sector_CodeName"]]
    df_agg_io=df_agg_io.head(cnf_sector) #get the first 185 sectors

    df_agg_io["total_Emission"] = totEm
    df_agg_io["scope1_Emission"] = scope1
    df_agg_io["scope2_Emission"] = scope2
    df_agg_io["scope3_Emission"] = scope3

    df_agg_io=pd.merge(df_agg_io, df_agg_label, on='Sector_CodeName')
    #print(df_agg_io.head(5))

    df_agg_io=df_agg_io.drop(columns=['Sector_CodeName', 'Sector_Number'])
    #print(df_agg_io.head(5))

    #df1 = df_agg_io.groupby("Aggregated sectors")["total_Emission", "scope1_Emission", "scope2_Emission", "scope3_Emission"].sum()
    df_agg_sectors= df_agg_io.groupby("Aggregated sectors").sum()
    #print(df_agg_sectors.head(5))
    
    return df_agg_sectors

def plot_agg_sectors(df):
    #https://dataviz.unhcr.org/tools/python/python_stacked_bar_chart.html
    # import libraries
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    from textwrap import wrap

    #plt.style.use(['unhcrpyplotstyle','bar'])
    print (df.head(5))
    #sort by total descending order
    #df['Total'] = df[["scope1_Emission", "scope2_Emission", "scope3_Emission"]].sum(numeric_only=True, axis=1)
    df = df.sort_values("total_Emission", ascending=True)
    #print(df)
    
    #prepare data array for plotting
    x = df.index.values
    #print("x", x)
    
    y1 = df[['scope1_Emission']].values.ravel()
    y2 = df[['scope2_Emission']].values.ravel()
    y3 = df[['scope3_Emission']].values.ravel()
    #print("y1", y1)
    #b_y3 = np.add(y1, y2)

    #wrap long labels
    x = [ '\n'.join(wrap(l, 25)) for l in x ]
    
    #plot the chart
    fig, ax = plt.subplots()
    rect1=ax.barh(x, y1, label='Scope 1 Emission')
    rect2=ax.barh(x, y2, left=y1, label='Scope 2 Emission')
    rect3=ax.barh(x, y3, left=y1+y2, label='Scope 3 Emission')

    #set chart title
    ax.set_title('Scope 1, 2 and 3 emission 2016 (t CO2)')

    #set chart legend
    #ax.legend(loc=(0,1.02), ncol=3)
    ax.legend(loc="lower right", prop={'size': 10})

    #set y-axis title
    ax.set_xlabel('in t CO2', fontsize=12)
    ax.set_ylabel('Aggregated I/O sectors', fontsize=12)
    ax.tick_params(labelsize=9)
    
    #set y-axis label 
    ax.tick_params(labelbottom=True)

    #show grid below the bars
    ax.grid(axis='x')

    #format x-axis tick labels
    def number_formatter(x, pos):
        if x >= 1e6:
            s = '{:1.0f}M'.format(x*1e-6)
        elif x < 1e6 and x >= 1e3:
            s = '{:1.0f}K'.format(x*1e-3)
        else: 
            s = '{:1.0f}'.format(x)
        return s
    ax.xaxis.set_major_formatter(number_formatter)

    #set chart source and copyright
    #plt.annotate('Source: UNHCR Refugee Data Finder', (0,0), (0, -40), xycoords='axes fraction', textcoords='offset points', va='top', color = '#666666', fontsize=9)
    #plt.annotate('©UNHCR, The UN Refugee Agency', (0,0), (0, -50), xycoords='axes fraction', textcoords='offset points', va='top', color = '#666666', fontsize=9)

    #adjust chart margin and layout
    fig.tight_layout()

    #show chart
    plt.show()
    
    
