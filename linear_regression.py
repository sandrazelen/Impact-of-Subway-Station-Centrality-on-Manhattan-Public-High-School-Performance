import re
import csv
import matplotlib.pyplot as plt
from scipy import stats

def extract_hs_subway_pairs(lines):
    stops = set()
    hs_subway_pairs = []
    for line in lines:
        line = line.strip()
        
        origin = r'"origin":\s*"([^"]+)"'
        dest = r'"destination":\s*"([^"]+)"'
        hs_match = re.search(origin, line)
        
        if hs_match:
            origin = hs_match.group(1)
            
        stop_match = re.search(dest, line)
        if stop_match:
            destination = stop_match.group(1)
            stops.add(destination)
            
        hs_subway_pairs.append((origin, destination))
    return hs_subway_pairs

def extract_subway_ctr_pairs(filename):
    subway_ctr_pairs = {}
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            
            subway_stop = row[0]
            centrality_score = row[1]
            if(subway_stop!='Node'):
                subway_ctr_pairs[subway_stop] =  float(centrality_score)
                
    return subway_ctr_pairs

def extract_hs_metrics(csvmetric):
    hs_metrics = {}
    with open(csvmetric, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        
        for row in reader:
            #print(row)
            school_name = row[0]
            collaborative_teachers = row[1]
            effective_leadership = row[2]
            rigor = row[3]
            support = row[4]
            family_community=row[5]
            trust = row[6]
            student_achievement = row[7]
            hs_metrics[school_name]=[collaborative_teachers, effective_leadership, rigor, support, family_community, trust, student_achievement]
            
        return hs_metrics


def extract_x_y(hs_subway_pairs, subway_ctr_pairs, hs_metrics):
    #pair 1 is hs sub (HS, SUB)
    #pair 2 is sub centrality (SUB, CENTRALITY)
    #pair 3 is hs and metrics (HS, METRICS)
    
    values = {}
    for pair in hs_subway_pairs:
        hs = pair[0]
        sub = pair[1]
        
        if(sub in subway_ctr_pairs.keys() and hs in hs_metrics.keys()):
            centrality = subway_ctr_pairs[sub]
            metrics = hs_metrics[hs]
            
            values[str(centrality)]=metrics
        
    return values

def linear_regr(d):
    x = []
    for key in d.keys():
        key = float(key)
        x.append(key)
        
    y =[]
    for value in d.values():
        y.append(float(value[2]))

    slope, intercept, r, p, std_err = stats.linregress(x, y)
    
    def myfunc(x):
        return slope * x + intercept

    mymodel = list(map(myfunc, x))

    plt.scatter(x, y)
    plt.plot(x, mymodel)
    plt.show()

def main():
    hs_sub = f"C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/highschool_station_distances.txt"
    with open(hs_sub, 'r', encoding="utf-8") as f: 
        lines = f.readlines()
    
    hs_subway_pairs = extract_hs_subway_pairs(lines)
    
    csvf = f"C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/closeness_centrality_output.csv"
    subway_ctr_pairs = extract_subway_ctr_pairs(csvf)
    
    csvmetric = f"C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/manhattan-quality-metrics.csv"
    hs_metrics = extract_hs_metrics(csvmetric)
    
    d = extract_x_y(hs_subway_pairs, subway_ctr_pairs, hs_metrics)
    linear_regr(d)
    
if __name__ == "__main__":
    main()