import os
import glob
import io
import requests
import logging
import warnings
import statistics
import math
from pathlib import Path
from importlib import resources

import numpy as np
import pandas as pnd

from Bio.phenotype.phen_micro import WellRecord

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator




def collect_raw_data(logger, input_folder, pms, replicates, discarding):
    logger.info(f"Collecting raw data...")
    
    
    # check file presence
    files = glob.glob(f'{input_folder}/*.xlsx')
    if len(files) == 0:
        logger.error(f"No .xlsx file found in the provided directory ('--input {input_folder}').")
        return 1
    
    
    # format discarding: 
    formatted_discarding = []
    for d in discarding.split(','):
        try: 
            strain, pm, replicate = d.split('-')
            formatted_discarding.append(f"{strain} {pm} 590 {replicate}")
            formatted_discarding.append(f"{strain} {pm} 750 {replicate}")
        except:
            logger.error(f"Invalid syntax found ('--discarding {discarding}').")
            return 1
    discarding = formatted_discarding
            
    
    # each strain has its own xlsx file: 
    strain_to_df = {}
    for file in files:
        strain = Path(file).stem

        res_df = []
        excel_file = pnd.ExcelFile(file)
        for time in range(len(excel_file.sheet_names)):
            df = excel_file.parse(f'T{time}')
            for pm in pms.split(','):
                for od in ['590', '750']:
                    for replicate in replicates.split(','):
                        readout = f'{pm} {od} {replicate}'
                        if strain + ' ' + readout in discarding:   # discard these samples
                            logger.debug(f"Discarding readout as requested: '{strain}', PM '{pm}', OD '{od}', replicate '{replicate}', time 'T{time}'.")
                            continue 

                            
                        # find boolean mask where value matches
                        mask = df == readout
                        # get the integer positions (row and column indices)
                        indices = list(zip(*mask.to_numpy().nonzero()))
                        # get the only result
                        try: result = indices[0]
                        except: 
                            logger.debug(f"Expected readout not found: strain '{strain}', PM '{pm}', OD '{od}', replicate '{replicate}', time 'T{time}'.")
                            continue


                        # adjust indices
                        row_i = result[0] + 2
                        col_i = result[1] + 1
                        for pm_row_i, pm_row in enumerate([r for r in 'ABCDEFGH']):
                            for pm_col_i, pm_col in enumerate([c +1 for c in range(12)]):
                                # get proper well name
                                pm_col = str(pm_col)
                                if len(pm_col) == 1: pm_col = '0' + pm_col
                                well = f'{pm_row}{pm_col}'
                                # get proper plate name
                                plate = pm
                                if plate == 'PM1': pass
                                if plate == 'PM2': plate = 'PM2A'
                                if plate == 'PM3': plate = 'PM3B'
                                if plate == 'PM4': plate = 'PM4A'
                                # read value
                                value = df.iloc[row_i + pm_row_i, col_i + pm_col_i]
                                res_df.append({
                                    'index_col': f"{plate}_{time}_{od}_{replicate}_{well}",
                                    'pm': plate, 'time': time, 'od': od, 'replicate': replicate, 'well': well, 'value': value})                     
        res_df = pnd.DataFrame.from_records(res_df)
        res_df = res_df.set_index('index_col', drop=True, verify_integrity=True)

        # populate dictionary
        strain_to_df[strain] = res_df
        
        
        # verbose logging
        logger.debug(f"Strain '{strain}' has {len(res_df['pm'].unique())} plates, {len(res_df['replicate'].unique())} replicates, and {len(res_df['time'].unique())} time points.")
        
        
    logger.info(f"Found {len(strain_to_df)} strains in input.")
    return strain_to_df



def data_preprocessing(logger, strain_to_df):
    
    
    
    # step 1: OD590 - OD750:
    logger.info(f"Substracting wavelengths...")
    for i, strain in enumerate(strain_to_df.keys()):
        df = strain_to_df[strain]
        logger.debug(f"Processing strain '{strain}'...")
        
        df['value_norm'] = None   
        for index, row in df.iterrows(): 
            if row['od'] == '590':
                index_750 = f"{row['pm']}_{row['time']}_750_{row['replicate']}_{row['well']}"
                df.loc[index, 'value_norm'] = df.loc[index, 'value'] - df.loc[index_750, 'value']
        df = df[df['value_norm'].isna()==False]
        df = df.drop(columns=['od', 'value'])
        df.index = [f"{row['pm']}_{row['time']}_{row['replicate']}_{row['well']}" for index, row in df.iterrows()]
        
        strain_to_df[strain] = df

        
        
    # step 2: subtraction of the blank
    logger.info(f"Substracting negative controls...")
    for i, strain in enumerate(strain_to_df.keys()):
        df = strain_to_df[strain]
        logger.debug(f"Processing strain '{strain}'...")
        
        for index, row in df.iterrows():
            # get the well of the blank
            if row['pm'] in ['PM1', 'PM2A', 'PM3B']:
                well_black = 'A01'
            else:  # PM4A is both for P and S
                if row['well'][0] in ['A','B','C','D','E']:
                    well_black = 'A01'  # P
                else: well_black = 'F01'  # S
            # get the index of the blank
            index_blank = f"{row['pm']}_{row['time']}_{row['replicate']}_{well_black}"
            df.loc[index, 'value_norm'] = df.loc[index, 'value_norm'] - df.loc[index_blank, 'value_norm']
            if df.loc[index_blank, 'value_norm'] < 0: 
                df.loc[index_blank, 'value_norm'] = 0
                
        strain_to_df[strain] = df


        
    # step 3: substraction of T0
    logger.info(f"Substracting T0...")
    for i, strain in enumerate(strain_to_df.keys()):
        df = strain_to_df[strain]
        logger.debug(f"Processing strain '{strain}'...")
        
        for index, row in df.iterrows():
            index_T0 = f"{row['pm']}_0_{row['replicate']}_{row['well']}"
            df.loc[index, 'value_norm'] = df.loc[index, 'value_norm'] - df.loc[index_T0, 'value_norm']
            if df.loc[index_blank, 'value_norm'] < 0: 
                df.loc[index_blank, 'value_norm'] = 0
                
    strain_to_df[strain] = df


    
    # step 4: get mean +- sem given replicates
    logger.info(f"Computing mean and SEM...")
    for i, strain in enumerate(strain_to_df.keys()):
        df = strain_to_df[strain]
        logger.debug(f"Processing strain '{strain}'...")
        
        found_reps = list(df['replicate'].unique())
        df['value_mean'] = None   # dedicated column
        df['value_sem'] = None   # dedicated column
        for index, row in df.iterrows():
            values = []
            for rep in found_reps:
                index_rep = f"{row['pm']}_{row['time']}_{rep}_{row['well']}"
                try: value = df.loc[index_rep, 'value_norm']
                except: continue  # replicate missing for some reason
                values.append(value)
            if len(values) > 1:
                # get the # standard error of the mean (standard deviation)
                std_dev = statistics.stdev(values)
                sem = std_dev / math.sqrt(len(values))
                df.loc[index, 'value_mean'] = statistics.mean(values)
                df.loc[index, 'value_sem'] = sem
            else:  # no replicates
                df.loc[index, 'value_mean'] = df.loc[index, 'value_norm']
                df.loc[index, 'value_sem'] = 0
        df = df.drop(columns=['replicate', 'value_norm'])
        df = df.drop_duplicates()
        df.index = [f"{row['pm']}_{row['time']}_{row['well']}" for index, row in df.iterrows()]

        strain_to_df[strain] = df
        
        
    return strain_to_df



def curve_fitting(logger, output_folder, strain_to_df, threshold_auc):
    chosen_model = 'gompertz'
    logger.info(f"Fitting wells using '{chosen_model}'...")
    
    
    # load official mappings
    official_pm_tables = {}
    for pm in ['PM1', 'PM2A', 'PM3B', 'PM4A']:
        with resources.path("phenodig.assets", f"{pm}.csv") as asset_path: 
            official_pm_tables[pm] = pnd.read_csv(asset_path, index_col=1, names=['plate','substrate','source','u1','u2','u3','u4','kc','cas'])
    
    
    
    strain_to_fitdf = {}
    
    # iterate strains:
    for strain, df in strain_to_df.items():
        logger.debug(f"Processing strain '{strain}'...")
        os.makedirs(f'{output_folder}/tables/', exist_ok=True)
        strain_to_fitdf[strain] = None


        fitdf = []
        for pm in df['pm'].unique():
            df_pm = df[df['pm']==pm]


            for i, row in enumerate('ABCDEFGH'):
                for j, col in enumerate([i+1 for i in range(12)]):
                    col = str(col)
                    if len(col)==1: col = f'0{col}'
                    well = f'{row}{col}'


                    # main plots: 
                    x_vector = df_pm[df_pm['well']==well]['time'].to_list()
                    y_vector = df_pm[df_pm['well']==well]['value_mean'].to_list()


                    # fit
                    wellrecord = WellRecord('custom', plate=None, signals={time: signal for time, signal in zip(x_vector, y_vector)})
                    
                    try: 
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")

                            wellrecord.fit([chosen_model])

                    except: pass  # "Could not fit any sigmoid function"
                
                
                    # get the area under the curve: 
                    auc = round(np.trapz(y_vector, x_vector),2)
                    lag = round(wellrecord.lag, 2) if wellrecord.lag != None else None
                    slope = round(wellrecord.slope, 2) if wellrecord.slope != None else None
                    plateau = round(wellrecord.plateau, 2) if wellrecord.plateau != None else None
                    y0 = round(wellrecord.y0, 2) if wellrecord.y0 != None else None
                    
                                
                    # growth calling
                    call = auc >= threshold_auc
                    
                    
                    substrate = official_pm_tables[pm].loc[well, 'substrate']
                    fitdf.append({
                        'index_col': f'{strain}_{pm}_{well}',
                        'strain': strain, 'pm': pm, 'well': well,
                        'substrate': substrate,
                        'auc': auc,
                        'model': wellrecord.model, 
                        'lag': lag, 
                        'slope': slope,
                        'plateau': plateau,
                        'y0': y0,
                        'call': call
                    })
        
        # populate dict:
        fitdf = pnd.DataFrame.from_records(fitdf)
        fitdf = fitdf.set_index('index_col', drop=True, verify_integrity=True)
        strain_to_fitdf[strain] = fitdf
        
        # save table:
        fitdf_xlsx = fitdf.fillna('na')
        fitdf_xlsx = fitdf_xlsx.reset_index(drop=True)
        fitdf_xlsx.index = fitdf_xlsx.index +1
        fitdf_xlsx.to_excel(f'{output_folder}/tables/fitting_{strain}.xlsx')
        logger.info(f"'{output_folder}/tables/fitting_{strain}.xlsx' created!")


    return strain_to_fitdf



def plot_plates(logger, output_folder, strain_to_df, strain_to_fitdf, noynorm, threshold_auc):
        
    zoom = 1.2
    logger.info(f"Plotting PM plates...")


    # load official mappings
    official_pm_tables = {}
    for pm in ['PM1', 'PM2A', 'PM3B', 'PM4A']:
        with resources.path("phenodig.assets", f"{pm}.csv") as asset_path: 
            official_pm_tables[pm] = pnd.read_csv(asset_path, index_col=1, names=['plate','substrate','source','u1','u2','u3','u4','kc','cas'])
    

    # get global y min/max
    if noynorm == False:
        mins, maxs = [], []
        for strain, df in strain_to_df.items():
            mins.append(min(df['value_mean'] - df['value_sem']))
            maxs.append(max(df['value_mean'] + df['value_sem']))
        y_min, y_max = min(mins), max(maxs)


    # iterate strains:
    for strain, df in strain_to_df.items():
        os.makedirs(f'{output_folder}/figures/{strain}', exist_ok=True)
        for pm in df['pm'].unique():
            df_pm = df[df['pm']==pm]


            # prepare subplots:
            fig, axs = plt.subplots(
                nrows=8, ncols=12,
                figsize=(12*zoom, 8*zoom), 
                gridspec_kw={'width_ratios': [1 for i in range(12)]}
            ) 
            plt.subplots_adjust(wspace=0, hspace=0)


            # get min and max: 
            if noynorm:
                y_min = min(df_pm['value_mean'] - df_pm['value_sem'])  
                y_max = max(df_pm['value_mean'] + df_pm['value_sem'])


            for i, row in enumerate('ABCDEFGH'):
                for j, col in enumerate([i+1 for i in range(12)]):
                    col = str(col)
                    if len(col)==1: col = f'0{col}'
                    well = f'{row}{col}'


                    # main plots: 
                    x_vector = df_pm[df_pm['well']==well]['time'].to_list()
                    y_vector = df_pm[df_pm['well']==well]['value_mean'].to_list()
                    sem_vector = df_pm[df_pm['well']==well]['value_sem'].to_list()
                    y_vector_eneg = [y-e if (y-e)>=0 else 0 for y,e in zip(y_vector, sem_vector) ]
                    y_vector_epos = [y+e if (y+e)>=0 else 0 for y,e in zip(y_vector, sem_vector) ]


                    axs[i, j].scatter(x_vector, y_vector, s=10, color='C0')
                    axs[i, j].plot(x_vector, y_vector, linestyle='-', color='C0')
                    axs[i, j].fill_between(x_vector, y_vector, color='C0', edgecolor=None, alpha=0.4)
                    axs[i, j].fill_between(x_vector, y_vector_eneg, y_vector_epos, color='grey', edgecolor=None, alpha=0.5)


                    # normalize axis limit: 
                    axs[i, j].set_ylim(y_min, y_max)
                    axs[i, j].set_xlim(left=0)  

                    
                    with warnings.catch_warnings():
                        # avoid "UserWarning: set_ticklabels() should only be used with a fixed number of ticks, i.e. after set_ticks() or using a FixedLocator."
                        warnings.simplefilter("ignore")
                        
                        # set ticks:
                        axs[i, j].xaxis.set_major_locator(MaxNLocator(nbins=5, integer=True))  
                        axs[i, j].yaxis.set_major_locator(MaxNLocator(nbins=5)) 
                        
                        # set tick labels (exclude 0)
                        axs[i, j].set_xticklabels([str(int(i)) if i!=0 else '' for i in axs[i, j].get_xticks()])
                        axs[i, j].set_yticklabels([str(i) if i!=0 else '' for i in axs[i, j].get_yticks()])

                        # remove ticks for central plots
                        if j!=0: axs[i, j].set_yticks([])
                        if i!=7: axs[i, j].set_xticks([])
                        


                    # set background color
                    call = strain_to_fitdf[strain].loc[f'{strain}_{pm}_{well}', 'call']
                    bg_color = 'white'
                    if call: 
                        bg_color = '#f0ffdb'  # paler green
                    else: 
                        bg_color = 'mistyrose'
                    axs[i, j].set_facecolor(bg_color)


                    
                    # draw growth model parameters
                    auc = strain_to_fitdf[strain].loc[f'{strain}_{pm}_{well}', 'auc']
                    model = strain_to_fitdf[strain].loc[f'{strain}_{pm}_{well}', 'model']
                    lag = strain_to_fitdf[strain].loc[f'{strain}_{pm}_{well}', 'lag']
                    slope = strain_to_fitdf[strain].loc[f'{strain}_{pm}_{well}', 'slope']
                    plateau = strain_to_fitdf[strain].loc[f'{strain}_{pm}_{well}', 'plateau']
                    y0 = strain_to_fitdf[strain].loc[f'{strain}_{pm}_{well}', 'y0']
                    if lag != None: 
                        axs[i, j].scatter(lag, 0, marker='^', color='red', alpha=0.5, zorder=100)  # 'zorder' sets the plotting level  
                        if slope != None: 
                            x_line = [t + lag for t in x_vector]
                            y_line = [y0 + slope *t for t in x_vector]
                            axs[i, j].plot(x_line, y_line, color='red', linestyle=':', linewidth=1, alpha=0.5)



                    # annotations:
                    color = 'grey'
                    padx, pady = max(x_vector)/40, y_max/10
                    
                    # title
                    axs[i, j].text(padx, y_max - pady*0 -pady/2, well, fontsize=7, fontweight='bold', ha='left', va='top', color=color)
                    
                    # substrate name
                    annot_substrate = official_pm_tables[pm].loc[well, 'substrate']
                    if len(annot_substrate) > 15: annot_substrate = annot_substrate[0:15] + '...'
                    annot_substrate = f'{annot_substrate}'
                    axs[i, j].text(padx, y_max - pady*1 -pady/2, annot_substrate, fontsize=7, ha='left', va='top', color=color)
                    
                    # substrate kc
                    annot_kc = official_pm_tables[pm].loc[well, 'kc']
                    if type(annot_kc)==float : annot_kc = 'na'
                    annot_kc = f'kc: {annot_kc}'
                    axs[i, j].text(padx, y_max - pady*2 -pady/2, annot_kc, fontsize=6, ha='left', va='top', color=color)

                    # fitting parameters
                    annot_auc = f'AUC: {auc}'
                    annot_model = f'f: {model}' if model != None else 'f: na'
                    annot_lag = f'λ: {lag}' if lag != None else 'λ: na'
                    annot_slope = f'μ: {slope}' if slope != None else 'μ: na'
                    annot_plateau = f'p: {plateau}' if plateau != None else 'p: na'
                    axs[i, j].text(padx, y_max - pady*3 -pady/2, annot_model, fontsize=6, ha='left', va='top', color=color)
                    axs[i, j].text(padx, y_max - pady*4 -pady/2, annot_auc, fontsize=6, ha='left', va='top', color=color)
                    axs[i, j].text(padx, y_max - pady*5 -pady/2, annot_lag, fontsize=6, ha='left', va='top', color=color)
                    axs[i, j].text(padx, y_max - pady*6 -pady/2, annot_slope, fontsize=6, ha='left', va='top', color=color)


            # set main title:
            fig.suptitle(f'{strain} - Biolog® {pm}  (thr={threshold_auc})', y=0.9)
            plt.savefig(f'{output_folder}/figures/{strain}/{pm}_{strain}.png', dpi=200, bbox_inches='tight') 
            plt.close(fig)  
        logger.info(f"'{output_folder}/figures/{strain}/*.png' created!")

        
        
def phenodig(args, logger): 
    
    
    # adjust out folder path
    while args.output.endswith('/'):
        args.output = args.output[:-1]
    
        
    strain_to_df = collect_raw_data(logger, args.input, args.plates, args.replicates, args.discarding)
    if type(strain_to_df) == int: return 1


    strain_to_df = data_preprocessing(logger, strain_to_df)
    if type(strain_to_df) == int: return 1


    strain_to_fitdf = curve_fitting(logger, args.output, strain_to_df, args.auc)
    if type(strain_to_fitdf) == int: return 1


    response = plot_plates(logger, args.output, strain_to_df, strain_to_fitdf, args.noynorm, args.auc)
    if response==1: return 1
    
        
    return 0