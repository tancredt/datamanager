import os
import numpy as np
import pandas as pd
import dirs


#both importers should return a dataframe with columns:
#{Serial, Model, Timestamp, Latitude, Longitude, Status, CO(ppm), H₂S(ppm), Isobutylene(ppm), LEL(%LEL), O₂(%)}
#Status contains the raw codes returned by polling application

def importResponder():
    raw_data_df = pd.DataFrame()
    for fname in os.listdir(dirs.RESPONDER_DIR):
        if len(fname) > 4 and fname[-4:] == ".csv": 
            raw_data_df = pd.read_csv(os.path.join(dirs.RESPONDER_DIR, fname))
            raw_data_df.rename(columns={"SERIAL NUMBER": "Serial", 
                               "MODEL NAME": "Model",
                              "LOG TIME": "Timestamp",
                              "LOCATION": "Location",
                              "STATUS": "Status",
                              "Isobutylene(ppm)": "VOC(ppm)"},
                              inplace=True)
            raw_data_df["Timestamp"] = pd.to_datetime(raw_data_df["Timestamp"])
            raw_data_df["CO(ppm)"] = raw_data_df["CO(ppm)"].astype(float)
            raw_data_df["H₂S(ppm)"] = raw_data_df["H₂S(ppm)"].astype(float)
            raw_data_df["VOC(ppm)"] = raw_data_df["VOC(ppm)"].astype(float)
            raw_data_df["LEL(%LEL)"] = raw_data_df["LEL(%LEL)"].astype(float)
            raw_data_df["O₂(%)"] = raw_data_df["O₂(%)"].astype(float)
            
            raw_data_df[["LongRAW", "LatRAW"]] = raw_data_df["Location"].str.split(" ", expand=True)
            raw_data_df["Longitude"] = raw_data_df["LongRAW"].str.lstrip("Lng:").astype(float)
            raw_data_df["Latitude"] = raw_data_df["LatRAW"].str.lstrip("Lat:").astype(float)
            raw_data_df = raw_data_df.drop(["Location", "LatRAW", "LongRAW"], axis=1) 
    return raw_data_df
            
def importRemote():
    for fname in os.listdir(RESPONDER_DIR):
        print(fname[:3])
        