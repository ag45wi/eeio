# Indonesian EEIO Model
# Sept 2024
# Ref: Putra, A. S., & Anita, Y. (2024). How does the establishment of an Indonesian Environmentally Extended Input Output (EEIO) model pave the way for Indonesia’s carbon future? Energy, Ecology and Environment. https://doi.org/10.1007/s40974-024-00328-6
# Python version: 3.10.11


import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from myutil import calc_matrix_A, get_mat_finEnerCons, get_mat_finCons, get_mat_finConsCO2, get_io_aggregate, plot_agg_sectors


## MAIN ##------------------------------------------------------------------------------------    

IS_CALC_MATRIX = 0   #0 read matrix; 1 calculate matrix

if (IS_CALC_MATRIX):

    #Original IO table
    #-----------------------------------------------------------------------------------------
    file_path = 'data/io_ind_2016.xlsx'

    #pip install pandas openpyxl
    df_io = pd.read_excel(file_path)
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
    file_path_FEC = 'data/final_energy_consumption_bytype.xlsx'
    df_fec= pd.read_excel(file_path_FEC)
    #print(df_fec.columns.values)
    X_fec = df_fec[["Coal", "Fuel", "Natural gas", "Electricity"]].values
    ROW_Year=6 #row index for year 2016 inside the file
    X_fec_yr = X_fec[ROW_Year,:]
    mat_finEnerCons=get_mat_finEnerCons(mat_A, X_fec_yr)
    #pd.DataFrame(mat_finEnerCons).to_excel("buf/mat_finEnerCons.xlsx")

    file_path_conv = 'data/conversion_factor.xlsx'
    df_conv= pd.read_excel(file_path_conv)
    #print(df_conv.columns.values)
    X_conv = df_conv[["Multiplier Factor to BOE"]].values
    #print(X_conv, X_conv.shape)
    COL=[3, 31, 17, 38] #col index for Coal, Fuel, Nat Gas, Electricity
    X_conv_subset = X_conv[COL]
    mat_finCons=get_mat_finCons(mat_finEnerCons, X_conv_subset)
    #pd.DataFrame(mat_finCons).to_excel("buf/mat_finCons.xlsx")

    file_path_co2 = 'data/direct_CO2_EF.xlsx'
    df_co2= pd.read_excel(file_path_co2)
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


    file_path_AGG = 'data/aggregated_sectors.xlsx'
    df_agg_label= pd.read_excel(file_path_AGG)
    #print(df_fec.columns.values)

    df_agg_sectors=get_io_aggregate(df_io, df_agg_label, totalEmission, scope1_emission_inT, scope2_emission_inT, scope3_emission_inT)
    #print(df_agg_sectors.head(5))

    if (1):
        print ("Writing dataframe to excels...")

        pd.DataFrame(mat_A).to_excel("buf/mat_A.xlsx")
        pd.DataFrame(mat_B).to_excel("buf/mat_B.xlsx")
        pd.DataFrame(mat_B_El).to_excel("buf/mat_B_El.xlsx")
        pd.DataFrame(mat_I).to_excel("buf/mat_I.xlsx")
        pd.DataFrame(mat_F).to_excel("buf/mat_F.xlsx")
        pd.DataFrame(mat_BF).to_excel("buf/mat_BF.xlsx")
        pd.DataFrame(mat_IminusA).to_excel("buf/mat_IminusA.xlsx")
        pd.DataFrame(mat_Inv).to_excel("buf/mat_Inv.xlsx")
        pd.DataFrame(mat_InvF).to_excel("buf/mat_InvF.xlsx")
        pd.DataFrame(mat_BInvF).to_excel("buf/mat_BInvF.xlsx")
        pd.DataFrame(mat_AF).to_excel("buf/mat_AF.xlsx")
        pd.DataFrame(mat_BAF).to_excel("buf/mat_BAF.xlsx")

        df_emissionIntensity.to_excel("buf/result_emissionIntensity.xlsx")
        df_emission.to_excel("buf/result_emission.xlsx")
        df_agg_sectors.to_excel("buf/result_agg_sectors.xlsx")
else:
    print ("Reading saved file to dataframe...")

    saved_file_path = "buf/result_agg_sectors.xlsx"
    df_agg_sectors = pd.read_excel(saved_file_path)
    df_agg_sectors.set_index('Aggregated sectors', inplace=True)
#endif

plot_agg_sectors(df_agg_sectors)


