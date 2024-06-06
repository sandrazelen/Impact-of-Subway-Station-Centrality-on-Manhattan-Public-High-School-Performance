#Selecting relevant columns from MTA Subway Stations dataset
#CSUREMM 2024

import csv


def read_data(filename):
    subway_data = []
    with open(filename, mode = 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        for row in csv_reader:
            coordinate = (float(row["GTFS Longitude"]),float(row["GTFS Latitude"]))
            subway_data.append((row["Line"], row["Stop Name"], row["Daytime Routes"], float(row["GTFS Latitude"]), float(row["GTFS Longitude"]),  coordinate))
    print(subway_data)
    return subway_data

def write_data(filename, filtered_data):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Line", "Stop Name", "Daytime Routes", "GTFS Latitude", "GTFS Longitude", "Georeference"])
        writer.writerows(filtered_data)
        
def main():
    input_mta = "C:/Users/misss/OneDrive/Desktop/csuremm/MTA_Subway_Stations.csv"
    output_mta = "C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/filtered_mta.csv"
    mta_data = read_data(input_mta)
    write_data(output_mta,mta_data)

if __name__ == "__main__":
    main()

