import datetime
import pandas as pd
import data_importer
import location_importer
import threshold_importer
import location_data
import validator
import corrector
import data_processor

def main():
    raw_data_df = data_importer.importResponder()
    location_dict = location_importer.importLocations()
    detector_validation_dict = validator.importValidations()
    validator.printValidationDict(detector_validation_dict)
    correction_dict = corrector.importCorrections()
    threshold_dict = threshold_importer.importThresholds()
    location_importer.printLocationDict(location_dict)
    if not location_importer.checkLocationDict(location_dict):
        location_df_list = location_data.getLocationDFList(location_dict, raw_data_df)
        validator.applyValidations(location_df_list, detector_validation_dict)
        corrector.applyCorrections(location_df_list, correction_dict)
        df = data_processor.getProcessedDF(location_df_list, ['A', 'B'], ['CO(ppm)', 'LEL(%LEL)'], 
                                            datetime.datetime(2023, 3, 7, 9, 18), datetime.datetime(2023, 3, 7, 9, 34), 2)    
        print(df)

if __name__ == "__main__":
    main()