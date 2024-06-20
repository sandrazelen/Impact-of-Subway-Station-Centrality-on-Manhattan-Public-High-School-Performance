import re

def clean_data(line):
    cleaned_line = re.sub(r'[\x00\r\n]', '', line)
    cleaned_line = cleaned_line.replace('\n', '').replace('\r', '')
    return cleaned_line

def match_string(str, line):
    match = re.search(str, line)  
    if match:
        value = match.group(1)
        return value
    
def find_edges(lines):
    edges = []
    for line in lines:
        #print(line)
        if(line.strip()):
            line = clean_data(line)
            #print(line)
            
            origin = r'"origin"\s*:\s*"([^"]*)"'
            destination = r'"destination"\s*:\s*"([^"]*)"'
            duration = r'"duration"\s*:\s*"([^"]*)"'
            
            station1 = match_string(origin, line)
            station2 = match_string(destination, line)
            duration = match_string(duration, line)
            
            if duration: 
                first_digit = int(duration[0])
                second_digit = duration[1]
                digits = ['0','1','2','3','4','5','6','7','8','9']
                if second_digit in digits:
                    second_digit = int(second_digit) 
                    final_digit = first_digit + second_digit
                else:
                    final_digit = first_digit
                    
            if station1 and station2 and duration:
                edge = (station1,station2,final_digit)
                edges.append(edge)       
    return edges
    
def main():
    filename = "C:/Users/misss/OneDrive/Desktop/csuremm/CSUREMM/one_line_formatted.txt"
    with open(filename, 'r', encoding='ISO-8859-1') as f:
        lines = f.readlines()
        
    edges = find_edges(lines)         
    #print(edges)
    
if __name__ == "__main__":
    main()
