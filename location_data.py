import os
import numpy as np
import pandas as pd

#returns the data for each location_dataframes
def getLocationDFList(location_dict, raw_data_df):
    location_df_list = []
    for location in location_dict["locations"]:
        #go through log an add the detectors data for each period
        temp_df_list = []
        for detector in location["detectors"]:
            start = pd.to_datetime(detector["start"])
            #date defaults to future but set to detector.stop if set
            stop = pd.to_datetime("2119-08-22")
            if detector["stop"]:
                stop = pd.to_datetime(detector["stop"])
            temp_df = raw_data_df.loc[(raw_data_df['Serial'] == detector["serial"]) & 
                                    (raw_data_df['Timestamp'] > start) & 
                                    (raw_data_df['Timestamp'] <= stop)]
            if len(temp_df) > 0:
                temp_df_list.append(temp_df)
        #create dataframe
        if len(temp_df_list) == 0:
            location_df = pd.DataFrame()
        else:
            #concatenate instrument sub dataframes
            location_df = pd.concat(temp_df_list)
            location_df = location_df.set_index("Timestamp").sort_index()
            #add validation columns
            location_df["CO(ppm)_Validation"] = [1] * len(location_df)
            location_df["VOC(ppm)_Validation"] = [1] * len(location_df)
            location_df["H₂S(ppm)_Validation"] = [1] * len(location_df)
            location_df["LEL(%LEL)_Validation"] = [1] * len(location_df)
            location_df["O₂(%)_Validation"] =  [1] * len(location_df)
                
        location_df.label = location["label"]
        location_df.latitude = location["latitude"]
        location_df.longitude = location["longitude"]
        location_df.description = location["description"]
        location_df_list.append(location_df)
        print(location_df.label)
        if len(location_df) == 0:
            print("\tNo Records found")
        else:
            print(f"\tNRecords: {len(location_df)} between {location_df.index[0]} and {location_df.index[-1]}")
    return location_df_list
    