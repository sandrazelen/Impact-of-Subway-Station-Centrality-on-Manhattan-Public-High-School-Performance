import json

def main():
    #filename = f"C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/output-onlinetexttools_.txt"
    #filename =f"C:/Users/misss/Downloads/output-onlinetexttools_walking.txt"
    #filename = f"C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/hs_subway_walkingdist_finalversion_quotes.json"
    filename = f"C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/oneline_final.txt"
    with open(filename, 'r', encoding='utf-8-sig') as f:
        file_content = f.readlines()  
    
    l=[]
    for line in file_content:
        l.append(line)
    #print(len(l))
    i=0
    for line in l:
        #put if each line ends in , otherwise comment out
        line =line[:-2]
        #print(line)
        data = json.loads(line)
        
        origin_addresses = data['origin_addresses']
        destination_addresses = data['destination_addresses']
        rows = data['rows']
        
        for i, row in enumerate(rows):
            elements = row['elements']
            for j, element in enumerate(elements):
                distancekm = element['distance']['text']
                distancem = element['distance']['value']
                duration = element['duration']['text']
                
                # Print or process the information as needed
                origin = origin_addresses[0]  # Since origin_addresses is a list with one item
                destination = destination_addresses[j]
                
                new_dict = {
                    'origin': origin,
                    'destination': destination,
                    'distancekm': distancekm,
                    'distancem': distancem,
                    'duration': duration
                }
                print(new_dict,",")

if __name__ == "__main__":
    main()
    
    

