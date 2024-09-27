import os
import pandas as pd
import numpy as np

def copy_file_todata(in_fname):
    import shutil
    cwd = os.getcwd()

    src_dir=f'{cwd}/static/uploads'
    dest_dir=f'{cwd}/static/data'

    files = os.listdir(src_dir)
    for file in files:
        file_path_src = os.path.join(src_dir, file)
        file_path_dest = os.path.join(dest_dir, file)

        #https://www.freecodecamp.org/news/python-copy-file-copying-files-to-another-directory/
        #If the destination file already exists, it gets replaced
        shutil.copyfile(file_path_src, file_path_dest)
        print(f"Copied: {file_path_src} -> {file_path_dest}")

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
    #print("X1_div,mult shape", X1_div.shape, mult.shape, X1_div[:, :5], mult)
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

def get_aggregate_each ():
    cwd=os.getcwd()
    df_emission = pd.read_csv(f"{cwd}/static/buf/result_emission.csv")
    df_io = pd.read_csv(f"{cwd}/static/data/io_ind_2016.csv")

    cnf_sector=df_emission.shape[0]
    df_sector=df_io[["Sector_CodeName"]]
    df_sector=df_sector.head(cnf_sector)

    df_emission["Sector_CodeName"]=df_sector.values.ravel()

    file_path_AGG = f'{os.getcwd()}/static/data/aggregated_sectors.csv'
    df_agg_label= pd.read_csv(file_path_AGG)

    df_emission=pd.merge(df_emission, df_agg_label, on='Sector_CodeName')

    return df_emission


def calc_mat(in_fname_io, in_fname_fec, in_fname_conv, in_fname_co2):
    print ("Inside util_app::calc_mat")
    print ("in_fname", in_fname_io, in_fname_fec, in_fname_conv, in_fname_co2)

    if (in_fname_io !=""): copy_file_todata(in_fname_io)
    else: in_fname_io="io_ind_2016.csv"
    if (in_fname_fec !=""): copy_file_todata(in_fname_fec)
    else: in_fname_fec="final_energy_consumption_bytype.csv"
    if (in_fname_conv !=""): copy_file_todata(in_fname_conv)
    else: in_fname_conv="conversion_factor.csv"
    if (in_fname_co2 !=""): copy_file_todata(in_fname_co2)
    else: in_fname_co2="direct_CO2_EF.csv"

    cwd = os.getcwd()
    folder_path = f'{cwd}/static/data'
    folder_path_buf = f'{cwd}/static/buf'
    #Original IO table
    #-----------------------------------------------------------------------------------------
    #file_path = 'data/io_ind_2016.xlsx'
    file_path=f"{folder_path}/{in_fname_io}"

    #pip install pandas openpyxl
    #df_io = pd.read_excel(file_path)
    df_io = pd.read_csv(file_path)
    #print(df_io.head(5))

    CNT_SECTOR=185
    sector_codeName=df_io.columns.values[3:CNT_SECTOR+3]
    #print(sector_codeName.shape, '\n',sector_codeName[:5])
    X = df_io[sector_codeName].values
    X_io=X[:CNT_SECTOR,:]
    X_total=X[-1,:]
    #print(X_io.shape, X_total.shape)
    #print(X_io[:5,:5]); print(X_total[:5])

    #Matrix A Coefficient
    #-----------------------------------------------------------------------------------------
    mat_A=calc_matrix_A(X_io, X_total)
    #print(mat_A[:5,:5])

    #Energy use per sector
    #-----------------------------------------------------------------------------------------
    #file_path_FEC = 'data/final_energy_consumption_bytype.xlsx'
    file_path_FEC = f"{folder_path}/{in_fname_fec}"
    df_fec= pd.read_csv(file_path_FEC)
    #print(df_fec.columns.values)
    X_fec = df_fec[["Coal", "Fuel", "Natural gas", "Electricity"]].values
    ROW_Year=6 #row index for year 2016 inside the file
    X_fec_yr = X_fec[ROW_Year,:]
    mat_finEnerCons=get_mat_finEnerCons(mat_A, X_fec_yr)
    #pd.DataFrame(mat_finEnerCons).to_excel("buf/mat_finEnerCons.xlsx")

    #file_path_conv = 'data/conversion_factor.xlsx'
    file_path_conv = f"{folder_path}/{in_fname_conv}"
    df_conv= pd.read_csv(file_path_conv)
    #print(df_conv.columns.values)
    X_conv = df_conv[["Multiplier Factor to BOE"]].values
    #print(X_conv, X_conv.shape)
    COL=[3, 31, 17, 38] #col index for Coal, Fuel, Nat Gas, Electricity
    X_conv_subset = X_conv[COL]
    mat_finCons=get_mat_finCons(mat_finEnerCons, X_conv_subset)
    #pd.DataFrame(mat_finCons).to_excel("buf/mat_finCons.xlsx")

    #file_path_co2 = 'data/direct_CO2_EF.xlsx'
    file_path_co2 = f"{folder_path}/{in_fname_co2}"
    df_co2= pd.read_csv(file_path_co2)
    #print(df_co2.columns.values)
    X_co2 = df_co2[["Heat content (HHV)", "Emission Factor"]].values
    #print(X_co2, X_co2.shape)
    ROW=[0, 2, 1, 3] #col index for Coal, Fuel, Nat Gas, Electricity
    X_co2_subset = X_co2[ROW,:]
    mat_finConsCO2=get_mat_finConsCO2(mat_finCons, X_co2_subset)
    #pd.DataFrame(mat_finConsCO2).to_excel("buf/mat_finConsCO2.xlsx")

    total_finConsCO2_inG=np.sum(mat_finConsCO2, axis=0)
    #print(total_finConsCO2_inG[:5])
    total_finConsCO2_inT=np.divide(total_finConsCO2_inG,1000000)
    #print(total_finConsCO2_inT[:5])
    total_finConsCO2_inT_perMillion=np.divide(total_finConsCO2_inT,X_total)
    #print(total_finConsCO2_inT_perMillion[:5])

    total_finConsCO2_El_inT=np.divide(mat_finConsCO2[3,:],1000000) #electricity at the 4th row
    total_finConsCO2_El_inT_perMillion=np.divide(total_finConsCO2_El_inT, X_total)

    #Matrix B
    #-----------------------------------------------------------------------------------------
    mat_B = total_finConsCO2_inT_perMillion
    mat_B_El = total_finConsCO2_El_inT_perMillion

    #Matrix F & I
    #-----------------------------------------------------------------------------------------
    mat_F = np.identity(CNT_SECTOR)
    mat_I = np.identity(CNT_SECTOR)
    #print("mat_F", mat_F[:5,:5])

    #Calculation Scope 1
    #-----------------------------------------------------------------------------------------
    mat_BF = np.matmul(mat_B, mat_F)
    #print("mat_BF shape", mat_BF.shape); print("mat_BF", mat_BF[:5])

    #Calculation Total
    #-----------------------------------------------------------------------------------------
    mat_IminusA = np.subtract(mat_I, mat_A)
    #print("mat_IminusA  shape", mat_IminusA.shape); print("mat_IminusA ", mat_IminusA [:5,:5])

    mat_Inv=np.linalg.inv(mat_IminusA)
    #print("mat_Inv shape", mat_Inv.shape); print("mat_Inv ", mat_Inv [:5,:5])

    mat_InvF=np.matmul(mat_Inv, mat_F)
    #print("mat_InvF shape", mat_InvF.shape); print("mat_InvF", mat_InvF[:5,:5])

    mat_BInvF=np.matmul(mat_B, mat_InvF)
    #print("mat_BInvF shape", mat_BInvF.shape); print("mat_BInvF", mat_BInvF[:5])


    #Calculation Scope 2
    #-----------------------------------------------------------------------------------------
    mat_AF = np.matmul(mat_A, mat_F)
    #print("mat_AF shape", mat_AF.shape); print("mat_AF", mat_AF[:5, :5])

    mat_BAF = np.matmul(mat_B_El, mat_AF)
    #print("mat_BAF shape", mat_BAF.shape); print("mat_BAF", mat_BAF[:5])

    #Results
    #-----------------------------------------------------------------------------------------
    totalEmissionIntensity = mat_BInvF
    emissionIntensityScope1 = mat_BF
    emissionIntensityScope2 = mat_BAF
    emissionIntensityScope3 = np.subtract(mat_BInvF, np.add(mat_BF,mat_BAF))
    #print("emissionIntensityScope3 shape", emissionIntensityScope3.shape); print(emissionIntensityScope3[:5])

    df_emissionIntensity = pd.DataFrame(data=[emissionIntensityScope1, emissionIntensityScope2, emissionIntensityScope3, totalEmissionIntensity]).T
    df_emissionIntensity.columns = ["emissionIntensityScope1", "emissionIntensityScope2", "emissionIntensityScope3", "totalEmissionIntensity"]

    X_domOut = df_io[["7000/Total Domestic Output at Basic Price"]].values
    X_domOut=X_domOut[:CNT_SECTOR].ravel()
    totalEmission = totalEmissionIntensity * X_domOut
    #print(totalEmissionIntensity.shape, X_domOut.shape)
    #print("totalEmission shape", totalEmission.shape); print(totalEmission[:5])

    scope1_emission_inT = emissionIntensityScope1 * X_domOut
    scope2_emission_inT = emissionIntensityScope2 * X_domOut
    scope3_emission_inT = totalEmission - (scope1_emission_inT + scope2_emission_inT)
    #print("scope3_emission_inT", totalEmission.shape); print(scope3_emission_inT[:5])

    df_emission = pd.DataFrame(data=[scope1_emission_inT, scope2_emission_inT, scope3_emission_inT, totalEmission]).T
    df_emission.columns = ["emissionScope1", "emissionScope2", "emissionScope3", "totalEmission"]


    file_path_AGG = f'{folder_path}/aggregated_sectors.csv'
    #file_path_AGG = in_path_agg
    df_agg_label= pd.read_csv(file_path_AGG)
    #print(df_fec.columns.values)

    df_agg_sectors=get_io_aggregate(df_io, df_agg_label, totalEmission, scope1_emission_inT, scope2_emission_inT, scope3_emission_inT)
    #print(df_agg_sectors.head(5))

    df_agg_sectors_each=get_aggregate_each()

    if (1):
        print ("Writing dataframe to csv...")

        pd.DataFrame(mat_A).to_csv(f"{folder_path_buf}/mat_A.csv", index=False)
        pd.DataFrame(mat_B).to_csv(f"{folder_path_buf}/mat_B.csv", index=False)
        pd.DataFrame(mat_B_El).to_csv(f"{folder_path_buf}/mat_B_El.csv", index=False)
        pd.DataFrame(mat_I).to_csv(f"{folder_path_buf}/mat_I.csv", index=False)
        pd.DataFrame(mat_F).to_csv(f"{folder_path_buf}/mat_F.csv", index=False)
        pd.DataFrame(mat_BF).to_csv(f"{folder_path_buf}/mat_BF.csv", index=False)
        pd.DataFrame(mat_IminusA).to_csv(f"{folder_path_buf}/mat_IminusA.csv", index=False)
        pd.DataFrame(mat_Inv).to_csv(f"{folder_path_buf}/mat_Inv.csv", index=False)
        pd.DataFrame(mat_InvF).to_csv(f"{folder_path_buf}/mat_InvF.csv", index=False)
        pd.DataFrame(mat_BInvF).to_csv(f"{folder_path_buf}/mat_BInvF.csv", index=False)
        pd.DataFrame(mat_AF).to_csv(f"{folder_path_buf}/mat_AF.csv", index=False)
        pd.DataFrame(mat_BAF).to_csv(f"{folder_path_buf}/mat_BAF.csv", index=False)

        df_emissionIntensity.to_csv(f"{folder_path_buf}/result_emissionIntensity.csv", index=False)
        df_emission.to_csv(f"{folder_path_buf}/result_emission.csv", index=False)
        df_agg_sectors.to_csv(f"{folder_path_buf}/result_agg_sectors.csv", index=True)

        df_agg_sectors_each.to_csv(f"{folder_path_buf}/result_agg_sectors_each.csv",index=False)

    return df_agg_sectors, df_agg_sectors_each

if __name__ == '__main__':
    if (1):
        fname_io="io_ind_2016.csv"; fname_fec=""; fname_conv=""; fname_co2=""
        calc_mat(fname_io, fname_fec, fname_conv, fname_co2)