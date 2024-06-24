import re
import csv
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression
import numpy as np

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
            school_name = row[0]
            collaborative_teachers = row[1]
            effective_leadership = row[2]
            rigor = row[3]
            support = row[4]
            family_community=row[5]
            trust = row[6]
            student_achievement = row[7]
            hs_metrics[school_name]=[student_achievement, rigor, collaborative_teachers, support, effective_leadership, family_community, trust]
            
        return hs_metrics


def extract_x_y(hs_subway_pairs, subway_ctr_pairs, hs_metrics):
    #pair 1 is hs sub (HS, SUB)
    #pair 2 is sub centrality (SUB, CENTRALITY)
    #pair 3 is hs and metrics (HS, METRICS)
    
    pairs = []
    for pair in hs_subway_pairs:
        hs = pair[0]
        sub = pair[1]
        
        if(sub in subway_ctr_pairs.keys() and hs in hs_metrics.keys()):
            centrality = subway_ctr_pairs[sub]
            metrics = hs_metrics[hs]
            pairs.append((float(centrality), metrics))
    
    return pairs

def get_coords(c,i):
    x_coord = []
    y_coord = []
    for pair in c:
        x = pair[0]
        y = float(pair[1][i])
        x_coord.append(x)
        y_coord.append(y)
        
    return x_coord, y_coord

def get_metric_name(i):
    if i==0:
        return 'Student Achievement'
    elif i==1:
        return 'Rigorous Instruction'
    elif i==2:
        return 'Collaborative Teachers'
    elif i==3:
        return 'Supportive Environment'
    elif i==4:
        return 'Effective School Leadership'
    elif i==5:
        return 'Strong Family-Community Ties'
    elif i==6:
        return 'Trust'
    else:
        return 'Invalid Performance Metric Index'

def multiple_lin_reg(c1,c2,c3,c4,perf_metric):
    i = perf_metric
    x1,y1 = get_coords(c1,i)
    x2,y2 = get_coords(c2,i)
    x3,y3 = get_coords(c3,i)
    x4,y4 = get_coords(c4,i)
    
    x = np.array((x1,x2,x3,x4))
    y = np.array((y1,y2,y3,y4))
    x = x.reshape(360,1)
    y = y.reshape(360,1)
    reg = LinearRegression()
    reg.fit(x, y)
    x = x.flatten()
    y=y.flatten()
    
    print()
    
    slope, intercept, r, p, std_err = stats.linregress(x, y)
    
    def myfunc(x):
        return slope * x + intercept

    mymodel = list(map(myfunc, x))

    #plt.scatter(x, y)
    
    plt.scatter(x1, y1, color='red', label='Node Degree')
    plt.scatter(x2, y2, color='blue', label='Closeness Centrality')
    plt.scatter(x3, y3, color='green', label='Betweenness Centrality')
    plt.scatter(x4, y4, color='orange', label='Eigenvector Centrality')
    
    plt.xlabel('Centrality Values')
    
    metric_name = get_metric_name(i)
    plt.ylabel(metric_name)
    plt.title('Multiple Linear Regression')
    
    plt.legend()
    plt.plot(x, mymodel)
    plt.show()
    
def main():
    hs_sub = f"C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/highschool_station_distances.txt"
    with open(hs_sub, 'r', encoding="utf-8") as f: 
        lines = f.readlines()
    
    hs_subway_pairs = extract_hs_subway_pairs(lines)
    
    closeness_csvf = f"C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/closeness_centrality_output.csv"
    closeness_subway_ctr_pairs = extract_subway_ctr_pairs(closeness_csvf)
    
    eigenvector_csvf = f"C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/eigenvector_centrality_output.csv"
    eigenvector_subway_ctr_pairs = extract_subway_ctr_pairs(eigenvector_csvf)
    
    betweenness_csvf = f"C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/betweenness_centrality_output.csv"
    betweenness_subway_ctr_pairs = extract_subway_ctr_pairs(betweenness_csvf)
    
    degree_csvf = f"C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/node_degree_output.csv"
    degree_subway_ctr_pairs = extract_subway_ctr_pairs(degree_csvf)
    
    csvmetric = f"C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/manhattan-quality-metrics.csv"
    hs_metrics = extract_hs_metrics(csvmetric)
    
    degree = extract_x_y(hs_subway_pairs, degree_subway_ctr_pairs, hs_metrics)
    closeness = extract_x_y(hs_subway_pairs, closeness_subway_ctr_pairs, hs_metrics)
    betweenness = extract_x_y(hs_subway_pairs, betweenness_subway_ctr_pairs, hs_metrics)
    eigenvector = extract_x_y(hs_subway_pairs, eigenvector_subway_ctr_pairs, hs_metrics)
    
    #from 1 to 6
    performance_metric = 0
    multiple_lin_reg(degree, closeness, betweenness, eigenvector,performance_metric)
        
if __name__ == "__main__":
    main()