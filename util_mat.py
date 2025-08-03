import os
import pandas as pd
import numpy as np
import sys
from dotenv import load_dotenv
from flask import Flask

from util_db import tbl_to_df, db_init, execute_query


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
    #print("inside get_mat_finCons")

    div1=convFactor.reshape(-1,1)
    #print("finEnerCons, convFactor, div1 shape", finEnerCons.shape, convFactor.shape, div1.shape)
    #print("div1", div1)

    X1_div=np.divide(finEnerCons,div1)
    X1_div=np.multiply(X1_div,1000)
    #print("div1", div1)

    #print ("X1", X1[:,:5])
    #print ("X1_div", X1_div[:,:5])
    #print ("X1_mult", X1_mult[:,:5])
    return X1_div

def get_mat_finConsCO2(finCons, CO2_EF):
    #matrix CO2_EF must be 4 rows, for coal, fuel, nat gas, electricity; in that order
    print("inside get_mat_finConsCO2")
    print("finCons, CO2_EF", finCons.shape, CO2_EF.shape)

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
    #print("CHK CO2_EF", CO2_EF[2,2])
    #sys.exit()
    row3=np.multiply(finCons[2,:],CO2_EF[2,2])
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
    print("cnf_sector", cnf_sector)

    #df_agg_io=df_io[["Sector_Code",	"Sector_Name", "Sector_CodeName"]]
    df_agg_io=df_io[["Sector_Code"]]
    #df_agg_io=df_io[["Sector_Code"]]
    df_agg_io=df_agg_io.head(cnf_sector) #get the first 185 sectors

    df_agg_io["total_Emission"] = totEm
    df_agg_io["scope1_Emission"] = scope1
    df_agg_io["scope2_Emission"] = scope2
    df_agg_io["scope3_Emission"] = scope3

    print("column df_agg_io, df_agg_label", df_agg_io.columns, df_agg_label.columns)
    df_agg_io=pd.merge(df_agg_io, df_agg_label, on='Sector_Code')
    print(df_agg_io.head(5))

    #df_agg_io=df_agg_io.drop(columns=['Sector_CodeName', 'Sector_Number'])
    df_agg_io=df_agg_io.drop(columns=['Sector_Code', 'Sector_Name'])
    print(df_agg_io.head(5))

    #df1 = df_agg_io.groupby("Aggregated sectors")["total_Emission", "scope1_Emission", "scope2_Emission", "scope3_Emission"].sum()
    df_agg_sectors= df_agg_io.groupby("Aggregated sectors").sum()
    print(df_agg_sectors.head(5))
    
    return df_agg_sectors

def get_aggregate_each (df_io, df_emission, df_agg_label):
    #cwd=os.getcwd()
    #df_emission = pd.read_csv(f"{cwd}/static/buf/result_emission.csv")
    #df_io = pd.read_csv(f"{cwd}/static/data/io_ind_2016.csv")

    cnf_sector=df_emission.shape[0]
    df_sector=df_io[["Sector_Code"]]
    df_sector=df_sector.head(cnf_sector)

    df_emission["Sector_Code"]=df_sector.values.ravel()

    #file_path_AGG = f'{os.getcwd()}/static/data/aggregated_sectors.csv'
    #file_path_AGG = f'{os.getcwd()}/static/data/agg_sectors_det.csv'
    #df_agg_label= pd.read_csv(file_path_AGG)

    #df_emission=pd.merge(df_emission, df_agg_label, on='Sector_CodeName')
    df_emission=pd.merge(df_emission, df_agg_label, on='Sector_Code')

    return df_emission

def write_to_db(db, year, df_emissionIntensity, df_emission, df_agg_sectors, df_agg_sectors_each):
    q_str = "SELECT sector_agg, sector_code, sector_name FROM sector_lst WHERE sector_label='DET'"
    df_sector = tbl_to_df(db, q_str)
    print("df columns", df_sector.columns)
    print("df_sector", df_sector.head(5))
    cnt_sector=df_sector.shape[0]
    sector_agg=df_sector["sector_agg"].values.tolist()
    sector_code=df_sector["sector_code"].values.tolist()
    sector_name=df_sector["sector_name"].values.tolist()
    year_lst=[year]*cnt_sector

    #emissionIntensity==========================================================================
    #df_emissionIntensity.to_sql('emissionIntensity', con=db, if_exists='replace', index=False)

    #https://gemini.google.com/app/30bfc0bb5e9c2500
    #on float data types

    print(f"df_emissionIntensity.shape {df_emissionIntensity.shape}, cnt_sector {cnt_sector}")
    if (df_emissionIntensity.shape[0] != cnt_sector):
        print("Inequal length of df_emissionIntensity and sector_lst")
        sys.exit()
    
    df_emissionIntensity["year"]=year_lst
    df_emissionIntensity["sector_agg"]=sector_agg
    df_emissionIntensity["sector_code"]=sector_code
    df_emissionIntensity["sector_name"]=sector_name

    df_emissionIntensity.to_csv(f"{os.getcwd()}/static/buf/{year}/tmp/df_emissionIntensity_{year}.csv", index=False)

    data_to_upsert = list(df_emissionIntensity[['year', 'sector_agg', 'sector_code', 'sector_name', 'emissionIntensityScope1', 'emissionIntensityScope2', 'emissionIntensityScope3', 'totalEmissionIntensity']].itertuples(index=False, name=None))

    sql_str = """
        INSERT INTO result_emission_intensity (year, sector_agg, sector_code, sector_name, emissionIntensityScope1, emissionIntensityScope2, emissionIntensityScope3, totalEmissionIntensity)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            emissionIntensityScope1 = VALUES(emissionIntensityScope1),
            emissionIntensityScope2 = VALUES(emissionIntensityScope2),
            emissionIntensityScope3 = VALUES(emissionIntensityScope3),
            totalEmissionIntensity = VALUES(totalEmissionIntensity);
        """
    
    execute_query(db, sql_str, isBatch=True, data_to_insert=data_to_upsert)

    tbl_name="result_emission_intensity"
    df_cnt = tbl_to_df(db, f"select count(*) as cnt from {tbl_name} where year='{year}'")
    print(f"Count of {tbl_name} {year}: {df_cnt['cnt'].values[0]}")

    #emission==========================================================================
    print(f"df_emission.shape {df_emission.shape}, cnt_sector {cnt_sector}")
    if (df_emission.shape[0] != cnt_sector):
        print("Inequal length of df_emission and sector_lst")
        sys.exit()
    
    df_emission["year"]=year_lst
    df_emission["sector_agg"]=sector_agg
    df_emission["sector_code"]=sector_code
    df_emission["sector_name"]=sector_name

    data_to_upsert = list(df_emission[['year', 'sector_agg', 'sector_code', 'sector_name', 'emissionScope1', 'emissionScope2', 'emissionScope3', 'totalEmission']].itertuples(index=False, name=None))

    sql_str = """
        INSERT INTO result_emission (year, sector_agg, sector_code, sector_name, emissionScope1, emissionScope2, emissionScope3, totalEmission)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            emissionScope1 = VALUES(emissionScope1),
            emissionScope2 = VALUES(emissionScope2),
            emissionScope3 = VALUES(emissionScope3),
            totalEmission = VALUES(totalEmission);
        """
    
    execute_query(db, sql_str, isBatch=True, data_to_insert=data_to_upsert)

    tbl_name="result_emission"
    df_cnt = tbl_to_df(db, f"select count(*) as cnt from {tbl_name} where year='{year}'")
    print(f"Count of {tbl_name} {year}: {df_cnt['cnt'].values[0]}")

    if (0):
        #agg_sectors==========================================================================
        q_str = "SELECT * FROM sector_agg ORDER by id"
        df_sector_agg = tbl_to_df(db, q_str)
        cnt_sector_agg=df_sector_agg.shape[0]
        print(f"df_agg_sectors.shape {df_agg_sectors.shape}, cnt_sector_agg {cnt_sector_agg}")
        if (df_agg_sectors.shape[0] != cnt_sector_agg):
            print("Inequal length of df_agg_sectors and sector_agg")
            sys.exit()
        
        year_lst_agg=[year]*cnt_sector_agg
        df_agg_sectors["year"]=year_lst_agg

        df_agg_sectors = df_agg_sectors.reset_index()
        df_agg_sectors.rename(columns={'index': 'Aggregated sectors'}, inplace=True)
        print("df_agg_sectors.columns", df_agg_sectors.columns.values)

        data_to_upsert = list(df_agg_sectors[['year', 'Aggregated sectors', 'scope1_Emission', 'scope2_Emission', 'scope3_Emission', 'total_Emission']].itertuples(index=False, name=None))

        #print("data_to_upsert", data_to_upsert)

        sql_str = """
            INSERT INTO result_sector_agg (year, sector_agg, emissionScope1, emissionScope2, emissionScope3, totalEmission)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                emissionScope1 = VALUES(emissionScope1),
                emissionScope2 = VALUES(emissionScope2),
                emissionScope3 = VALUES(emissionScope3),
                totalEmission = VALUES(totalEmission);
            """
        
        execute_query(db, sql_str, isBatch=True, data_to_insert=data_to_upsert)

        tbl_name="result_sector_agg"
        df_cnt = tbl_to_df(db, f"select count(*) as cnt from {tbl_name} where year='{year}'")
        print(f"Count of {tbl_name} {year}: {df_cnt['cnt'].values[0]}")

        #agg_sectors_each==========================================================================

        print(f"df_agg_sectors_each.shape {df_agg_sectors_each.shape}, cnt_sector {cnt_sector}")
        if (df_agg_sectors_each.shape[0] != cnt_sector):
            print("Inequal length of df_agg_sectors_each and sector_lst")
            sys.exit()
        
        df_agg_sectors_each["year"]=year_lst

        data_to_upsert = list(df_agg_sectors_each[['year', 'Aggregated sectors', 'Sector_Code', 'Sector_Name', 'emissionScope1', 'emissionScope2', 'emissionScope3', 'totalEmission']].itertuples(index=False, name=None))

        sql_str = """
            INSERT INTO result_sector_each (year, sector_agg, sector_code, sector_name, emissionScope1, emissionScope2, emissionScope3, totalEmission)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                emissionScope1 = VALUES(emissionScope1),
                emissionScope2 = VALUES(emissionScope2),
                emissionScope3 = VALUES(emissionScope3),
                totalEmission = VALUES(totalEmission);
            """
        
        execute_query(db, sql_str, isBatch=True, data_to_insert=data_to_upsert)

        tbl_name="result_sector_each"
        df_cnt = tbl_to_df(db, f"select count(*) as cnt from {tbl_name} where year='{year}'")
        print(f"Count of {tbl_name} {year}: {df_cnt['cnt'].values[0]}")



def calc_mat(db, fname_io, year):
    print ("Inside util_app::calc_mat")

    cwd = os.getcwd()
    folder_path = f'{cwd}/static/data/{year}'
    folder_path_buf = f'{cwd}/static/buf/{year}'

    if not os.path.exists(folder_path_buf):
        os.makedirs(folder_path_buf)
    if not os.path.exists(f"{folder_path_buf}/tmp"):
        os.makedirs(f"{folder_path_buf}/tmp")

    #Original IO table
    #-----------------------------------------------------------------------------------------
    #file_path = 'data/io_ind_2016.xlsx'
    file_path=f"{folder_path}/{fname_io}"
    print("file_path", file_path)
    if not os.path.exists(file_path):
        return 0, f"Cannot find {file_path}", pd.DataFrame(), pd.DataFrame()

    df_io = pd.read_csv(file_path, thousands=",")
    #print(df_io.head(5))
    print("df_io shape", df_io.shape)

    q_str = "SELECT sector_agg, sector_code, sector_name FROM sector_lst WHERE sector_label='DET'"
    df_sector = tbl_to_df(db, q_str)
    cnt_sector=df_sector.shape[0]
    sector_code=df_sector["sector_code"].values.tolist()
    print("cnt_sector", cnt_sector)
    #print("sector_code", sector_code)
    CNT_SECTOR=cnt_sector

    X=df_io[sector_code].values
    #X_io = df_io[df_io['sector_code'].isin(sector_code)].values
    X_io=X[:cnt_sector,:]
    X_total=X[-1,:]
    print("X_io.shape, X_total.shape-2", X_io.shape, X_total.shape)
    print("X_io-2",X_io[:5,:5]); print("X_total-2",X_total[:5])
    print("df_io", df_io.head(5))
    

    #Matrix A Coefficient
    #-----------------------------------------------------------------------------------------
    mat_A=calc_matrix_A(X_io, X_total)
    #print(mat_A[:5,:5])

    #Energy use per sector
    fec_lst=["Coal", "Fuel", "Natural Gas", "Electricity"]
    q_str = f"""SELECT year, energy_type, fec_val, 
    energy_lst.energy_type_code, energy_lst.energy_type_name
    FROM fec_byyear
    LEFT JOIN energy_lst ON fec_byyear.energy_type = energy_lst.energy_type_code
    WHERE year='{year}'
    """

    df_fec = tbl_to_df(db, q_str)
    print("df_fec", df_fec.shape, df_fec.head(5))
    df_fec_reordered = df_fec.set_index('energy_type_name').reindex(fec_lst)
    X_fec_subset = df_fec_reordered['fec_val'].values
    print("X_fec_subset", X_fec_subset.shape, X_fec_subset[:5])
    #print(df_fec["energy_type_name"].values.tolist())
    mat_finEnerCons=get_mat_finEnerCons(mat_A, X_fec_subset)
    pd.DataFrame(mat_finEnerCons, index=fec_lst).to_csv(f"static/buf/{year}/tmp/df_finEnerCons.csv")
    
    #sys.exit()

    #Conversion factor==================================================================
    q_str = "SELECT energy_type, multiplier_factor FROM conversion_factor"
    df_conv = tbl_to_df(db, q_str)
    #print("df_conv", df_conv.shape, df_conv.head(5))
    #print("fec_lst", fec_lst)

    df_conv['energy_type_lower'] = df_conv['energy_type'].str.lower()
    fec_lst_lower = [item.lower() for item in fec_lst]

    df_reordered = df_conv.set_index('energy_type_lower').reindex(fec_lst_lower)
    X_conv_subset = df_reordered['multiplier_factor'].values
    #print("X_conv_subset", X_conv_subset.shape, X_conv_subset[:5])

    mat_finCons=get_mat_finCons(mat_finEnerCons, X_conv_subset)
    #print("mat_finCons", mat_finCons.shape)
    pd.DataFrame(mat_finCons).to_csv(f"static/buf/{year}/tmp/mat_finCons.csv")

    

    #CO2 emission factor=========================================================
    q_str = "SELECT energy_type, heat_content_hhv, emission_factor, multiplier FROM co2_factor"
    df_co2 = tbl_to_df(db, q_str)

    df_co2_reordered = df_co2.set_index('energy_type').reindex(fec_lst)
    X_co2_subset = df_co2_reordered[['heat_content_hhv','emission_factor', 'multiplier']].values
    print("X_co2_subset-df", X_co2_subset.shape, X_co2_subset[:5])

    mat_finConsCO2=get_mat_finConsCO2(mat_finCons, X_co2_subset)
    pd.DataFrame(mat_finConsCO2, index=fec_lst).to_csv(f"static/buf/{year}/tmp/df_finConsCO2.csv")

    

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

    col_domOut="7000"
    #X_domOut = df_io[["7000/Total Domestic Output at Basic Price"]].values
    X_domOut = df_io[[col_domOut]].values
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


    df_Sector=df_sector.copy()
    df_Sector = df_Sector.rename(columns={'sector_agg': 'Aggregated sectors', 'sector_code': 'Sector_Code', 'sector_name': 'Sector_Name'})

    print("df_io before merge", df_io.shape, df_io.head(5))
    print("df_Sector", df_Sector.shape, df_Sector.head(5))

    df_io = pd.merge(df_io, df_Sector[['Aggregated sectors', 'Sector_Code', 'Sector_Name']], on='Sector_Code')
    #df_io['Sector_CodeName'] = df_io['Sector_Code'].astype(str) + '/' + df_io['Sector_Name'].astype(str)
    print("df_io after merge", df_io.shape, df_io.head(5))
    #sys.exit()
    df_agg_sectors=get_io_aggregate(df_io, df_Sector, totalEmission, scope1_emission_inT, scope2_emission_inT, scope3_emission_inT)
    print("df_agg_sectors", df_agg_sectors.head(5))
    df_agg_sectors.to_csv(f"{folder_path_buf}/tmp/df_agg_sectors.csv", index=True)
    #sys.exit()

    df_agg_sectors_each=get_aggregate_each(df_io, df_emission, df_Sector)

    if (0):
        print ("Writing dataframe to csv...")

        pd.DataFrame(X_io).to_csv(f"{folder_path_buf}/X_io.csv", index=False)
        pd.DataFrame(X_total).to_csv(f"{folder_path_buf}/X_total.csv", index=False)
        pd.DataFrame(X_domOut).to_csv(f"{folder_path_buf}/X_domOut.csv", index=False)
        pd.DataFrame(totalEmission).to_csv(f"{folder_path_buf}/totalEmission.csv", index=False)
        pd.DataFrame(scope1_emission_inT).to_csv(f"{folder_path_buf}/scope1_emission_inT.csv", index=False)
        pd.DataFrame(scope2_emission_inT).to_csv(f"{folder_path_buf}/scope2_emission_inT.csv", index=False)
        pd.DataFrame(scope3_emission_inT).to_csv(f"{folder_path_buf}/scope3_emission_inT.csv", index=False)
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

    if (1):
        print ("Writing dataframe to database...")
        write_to_db(db, year, df_emissionIntensity, df_emission, df_agg_sectors, df_agg_sectors_each)
    
    return 1, "Matrices are successfully computed", df_agg_sectors, df_agg_sectors_each


if __name__ == '__main__':
    if (1):
        EEIO_FILES = ["IO", "FinalEnergyConsumption", "ConversionFactor", "DirectCO2EmmisionFactor"]
        YEAR=2020
        fname_io=f"io_ind_{YEAR}.csv"

        app = Flask(__name__)
        load_dotenv()
        db = db_init(app)
        with app.app_context():
            rv, msg1, df_agg_sectors, df_agg_sectors_each=calc_mat(db, fname_io, YEAR)