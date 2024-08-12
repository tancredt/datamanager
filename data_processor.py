import numpy as np
import pandas as pd
import datetime

#location_choices should be a list of the location labels
#gas choices are a list of gases
#stop can be null but will be set to the future
#interval should be in minutes
def getProcessedDF(location_df_list, location_choices, gas_choices, start, stop, interval):
    #create a stop in future in case the stop time is None
    vstop = pd.to_datetime("2119-08-22")
    if stop:
        vstop = stop
    #create an index with constantly spaced intervals
    combined_df = pd.DataFrame(data={}, index=pd.date_range(start, vstop, freq=str(interval) + 'min'))
    
    for location_df in location_df_list:
        #resample the original dataframe
        if len(location_df) > 0:
            for gas in gas_choices:
                if gas in location_df.columns:
                    resampled_df = location_df.loc[location_df[gas + "_Validation"] == 1][gas].resample(str(interval) + 'min').mean()
                    #join the resampled dataframe with date range so that we have an evenly spaced timeseries (might be missing values in the resampled dataframe
                    combined_df = combined_df.join(resampled_df) 
                    combined_df.rename(columns={gas: location_df.label + "_" + gas}, inplace=True)
    print(combined_df)
    return combined_df