import requests
import pandas as pd
import time

#Replace with your API Key
API_key = "YOUR API KEY"

origins = [
   {"name": "Orchard Collegiate Academy - [HS] 01M292", "lat": 40.713446, "lng": -73.986033, "station":{"name": "East Broadway", "lat": 40.713715, "lng": -73.990173, "routes": ["F"], "borough": "M"}},
{"name": "University Neighborhood High School - [HS] 01M448", "lat": 40.7121857, "lng": -73.9842031, "station":{"name": "East Broadway", "lat": 40.713715, "lng": -73.990173, "routes": ["F"], "borough": "M"}},
{"name": "East Side Community School - [HS] 01M450", "lat": 40.7291086, "lng": -73.9825277, "station":{"name": "1 Av", "lat": 40.730953, "lng": -73.981628, "routes": ["L"], "borough": "M"}},
{"name": "New Explorations into Science, Technology and Math High School - [HS] 01M539", "lat": 40.719783, "lng": -73.979245, "station":{"name": "Delancey St-Essex St", "lat": 40.718611, "lng": -73.988114, "routes": ["F"], "borough": "M"}},
{"name": "Bard High School Early College - [HS] 01M696", "lat": 40.7184646, "lng": -73.9758571, "station":{"name": "Delancey St-Essex St", "lat": 40.718611, "lng": -73.988114, "routes": ["F"], "borough": "M"}},
{"name": "47 The American Sign Language and English Secondary School - [HS] 02M047", "lat": 40.7387769, "lng": -73.9814014, "station":{"name": "23 St and Park Av S", "lat": 40.739864, "lng": -73.986599, "routes": ["6"], "borough": "M"}},
{"name": "The Urban Assembly School for Emergency Management - [HS] 02M135", "lat": 40.7112411, "lng": -74.0014423, "station":{"name": "Brooklyn Bridge-City Hall", "lat": 40.713065, "lng": -74.004131, "routes": ["4", "5", "6"], "borough": "M"}},
{"name": "Stephen T. Mather Building Arts & Craftsmanship High School - [HS] 02M139", "lat": 40.763999, "lng": -73.990835, "station":{'name': '50 St and 8th Av', 'lat': 40.762456, 'lng': -73.985984, 'routes': ['C', 'E'], 'borough': 'M'}},
{"name": "The Clinton School - [HS] 02M260", "lat": 40.7362915, "lng": -73.9924468, "station":{"name": "14 St-Union Sq", "lat": 40.735736, "lng": -73.990568, "routes": ["N", "Q", "R", "W"], "borough": "M"}},
{"name": "Manhattan Early College School for Advertising - [HS] 02M280", "lat": 40.7112756, "lng": -74.0012679, "station":{"name": "Brooklyn Bridge-City Hall", "lat": 40.713065, "lng": -74.004131, "routes": ["4", "5", "6"], "borough": "M"}},
{"name": "Urban Assembly Maker Academy - [HS] 02M282", "lat": 40.71134, "lng": -74.00165, "station":{"name": "Brooklyn Bridge-City Hall", "lat": 40.713065, "lng": -74.004131, "routes": ["4", "5", "6"], "borough": "M"}},
{"name": "Food and Finance High School - [HS] 02M288", "lat": 40.7653073, "lng": -73.9922821, "station":{"name": "50 St and 8th Av", "lat": 40.762456, "lng": -73.985984, "routes": ["C", "E"], "borough": "M"}},
{"name": "Essex Street Academy - [HS] 02M294", "lat": 40.7174561, "lng": -73.9895561, "station":{"name": "Delancey St-Essex St", "lat": 40.718611, "lng": -73.988114, "routes": ["F"], "borough": "M"}},
{"name": "High School of Hospitality Management - [HS] 02M296", "lat": 40.7655356, "lng": -73.9931625, "station":{"name": "50 St and 8th Av", "lat": 40.762456, "lng": -73.985984, "routes": ["C", "E"], "borough": "M"}},
{"name": "Pace High School - [HS] 02M298", "lat": 40.716194, "lng": -73.993385, "station":{"name": "Grand St", "lat": 40.718267, "lng": -73.993753, "routes": ["B", "D"], "borough": "M"}},
{"name": "Urban Assembly School of Design and Construction, The - [HS] 02M300", "lat": 40.765536, "lng": -73.993163, "station":{"name": "50 St and 8th Av", "lat": 40.762456, "lng": -73.985984, "routes": ["C", "E"], "borough": "M"}},
{"name": "Facing History School, The - [HS] 02M303", "lat": 40.7654304, "lng": -73.9926528, "station":{"name": "50 St and 8th Av", "lat": 40.762456, "lng": -73.985984, "routes": ["C", "E"], "borough": "M"}},
{"name": "Urban Assembly Academy of Government and Law, The - [HS] 02M305", "lat": 40.717192, "lng": -73.989467, "station":{"name": "Delancey St-Essex St", "lat": 40.718611, "lng": -73.988114, "routes": ["F"], "borough": "M"}},
{"name": "Lower Manhattan Arts Academy - [HS] 02M308", "lat": 40.7208595, "lng": -74.0006686, "station":{"name": "Spring St and Lafayette", "lat": 40.722301, "lng": -73.997141, "routes": ["6"], "borough": "M"}},
{"name": "Urban Assembly School of Business for Young Women, the - [HS] 02M316", "lat": 40.706554, "lng": -74.011877, "station":{"name": "Broad St", "lat": 40.706476, "lng": -74.011056, "routes": ["J", "Z"], "borough": "M"}},
{"name": "Gramercy Arts High School - [HS] 02M374", "lat": 40.7354278, "lng": -73.9872741, "station":{"name": "14 St-Union Sq", "lat": 40.735736, "lng": -73.990568, "routes": ["N", "Q", "R", "W"], "borough": "M"}},
{"name": "NYC iSchool - [HS] 02M376", "lat": 40.7246823, "lng": -74.0050859, "station":{"name": "Spring St and 6th Av", "lat": 40.726227, "lng": -74.003739, "routes": ["C", "E"], "borough": "M"}},
{"name": "Manhattan Business Academy - [HS] 02M392", "lat": 40.743136, "lng": -74.002519, "station":{"name": "14 St and 8 Av", "lat": 40.740893, "lng": -74.00169, "routes": ["A", "C", "E"], "borough": "M"}},
{"name": "Business Of Sports School - [HS] 02M393", "lat": 40.7638592, "lng": -73.9903543, "station":{"name": "50 St and 8th Av", "lat": 40.762456, "lng": -73.985984, "routes": ["C", "E"], "borough": "M"}},
{"name": "The High School For Language And Diplomacy - [HS] 02M399", "lat": 40.7353237, "lng": -73.9870812, "station":{"name": "14 St-Union Sq", "lat": 40.735736, "lng": -73.990568, "routes": ["N", "Q", "R", "W"], "borough": "M"}},
{"name": "High School for Environmental Studies - [HS] 02M400", "lat": 40.7679759, "lng": -73.9881796, "station":{"name": "59 St-Columbus Circle", "lat": 40.768272, "lng": -73.981833}},
{"name": "Institute for Collaborative Education - [HS] 02M407", "lat": 40.7326687, "lng": -73.9825816, "station":{"name": "1 Av", "lat": 40.730953, "lng": -73.981628, "routes": ["L"], "borough": "M"}},
{"name": "Professional Performing Arts High School - [HS] 02M408", "lat": 40.761226, "lng": -73.9886092, "station":{"name": "50 St and 8th Av", "lat": 40.762456, "lng": -73.985984, "routes": ["C", "E"], "borough": "M"}},
{"name": "Baruch College Campus High School - [HS] 02M411", "lat": 40.7418485, "lng": -73.985909, "station":{"name": "23 St and Park Av S", "lat": 40.739864, "lng": -73.986599, "routes": ["6"], "borough": "M"}},
{"name": "N.Y.C. Lab School for Collaborative Studies - [HS] 02M412", "lat": 40.7424259, "lng": -74.0026278, "station":{"name": "14 St and 8 Av", "lat": 40.740893, "lng": -74.00169, "routes": ["A", "C", "E"], "borough": "M"}},
{"name": "School of the Future High School - [HS] 02M413", "lat": 40.7390867, "lng": -73.9853658, "station":{"name": "23 St and Park Av S", "lat": 40.739864, "lng": -73.986599, "routes": ["6"], "borough": "M"}},
{"name": "N.Y.C. Museum School - [HS] 02M414", "lat": 40.7424393, "lng": -74.0026597, "station":{"name": "14 St and 8 Av", "lat": 40.740893, "lng": -74.00169, "routes": ["A", "C", "E"], "borough": "M"}},
{"name": "Eleanor Roosevelt High School - [HS] 02M416", "lat": 40.770284, "lng": -73.953281, "station":{"name": "72 St and 2nd Av", "lat": 40.768799, "lng": -73.958424, "routes": ["Q"], "borough": "M"}},
{"name": "Millennium High School - [HS] 02M418", "lat": 40.70473, "lng": -74.011452, "station":{"name": "Broad St", "lat": 40.706476, "lng": -74.011056, "routes": ["J", "Z"], "borough": "M"}},
{"name": "Landmark High School - [HS] 02M419", "lat": 40.743136, "lng": -74.002519, "station":{"name": "14 St and 8 Av", "lat": 40.740893, "lng": -74.00169, "routes": ["A", "C", "E"], "borough": "M"}},
{"name": "High School for Health Professions and Human Services - [HS] 02M420", "lat": 40.7325522, "lng": -73.9826723, "station":{"name": "1 Av", "lat": 40.730953, "lng": -73.981628, "routes": ["L"], "borough": "M"}},
{"name": "Quest to Learn - [HS] 02M422", "lat": 40.7431305, "lng": -74.0025192, "station":{"name": "14 St and 8 Av", "lat": 40.740893, "lng": -74.00169, "routes": ["A", "C", "E"], "borough": "M"}},
{"name": "Leadership and Public Service High School - [HS] 02M425", "lat": 40.7090242, "lng": -74.0123569, "station":{"name": "Rector St", "lat": 40.70722, "lng": -74.013342, "routes": ["R", "W"], "borough": "M"}},
{"name": "Manhattan Academy For Arts & Language - [HS] 02M427", "lat": 40.746306, "lng": -73.98114, "station":{"name": "33 St", "lat": 40.746081, "lng": -73.982076, "routes": ["6"], "borough": "M"}},
{"name": "Murray Hill Academy - [HS] 02M432", "lat": 40.746306, "lng": -73.98114, "station":{"name": "33 St", "lat": 40.746081, "lng": -73.982076, "routes": ["6"], "borough": "M"}},
{"name": "International High School at Union Square - [HS] 02M438", "lat": 40.7354677, "lng": -73.987393, "station":{"name": "14 St-Union Sq", "lat": 40.735736, "lng": -73.990568, "routes": ["N", "Q", "R", "W"], "borough": "M"}},
{"name": "Manhattan Village Academy - [HS] 02M439", "lat": 40.7419187, "lng": -73.9922938, "station":{"name": "23 St and 6th Av", "lat": 40.742878, "lng": -73.992821, "routes": ["F", "M"], "borough": "M"}},
{"name": "Vanguard High School - [HS] 02M449", "lat": 40.76536, "lng": -73.959737, "station":{"name": "72 St and 2nd Av", "lat": 40.768799, "lng": -73.958424, "routes": ["Q"], "borough": "M"}},
{"name": "Manhattan International High School - [HS] 02M459", "lat": 40.7653683, "lng": -73.9596962, "station":{"name": "68 St-Hunter College", "lat": 40.768141, "lng": -73.96387, "routes": ["6"], "borough": "M"}},
{"name": "Stuyvesant High School - [HS] 02M475", "lat": 40.7178149, "lng": -74.0138422, "station":{"name": "Chambers St and West Broadway", "lat": 40.715478, "lng": -74.009266, "routes": ["1", "2", "3"], "borough": "M"}},
{"name": "High School of Economics and Finance - [HS] 02M489", "lat": 40.7092571, "lng": -74.0123392, "station":{"name": "Rector St", "lat": 40.70722, "lng": -74.013342, "routes": ["R", "W"], "borough": "M"}},
{"name": "Unity Center for Urban Technologies - [HS] 02M500", "lat": 40.7464213, "lng": -73.9811631, "station":{"name": "33 St", "lat": 40.746081, "lng": -73.982076, "routes": ["6"], "borough": "M"}},
{"name": "Talent Unlimited High School - [HS] 02M519", "lat": 40.76564, "lng": -73.959777, "station":{"name": "72 St and 2nd Av", "lat": 40.768799, "lng": -73.958424, "routes": ["Q"], "borough": "M"}},
{"name": "Jacqueline Kennedy Onassis High School - [HS] 02M529", "lat": 40.7577928, "lng": -73.9834084, "station":{"name": "47-50 Sts-Rockefeller Ctr", "lat": 40.758663, "lng": -73.981329, "routes": ["B", "D", "F", "M"], "borough": "M"}},
{"name": "Repertory Company High School for Theatre Arts - [HS] 02M531", "lat": 40.7561203, "lng": -73.9844558, "station":{"name": "Times Sq-42 St", "lat": 40.755356, "lng": -73.987042}},
{"name": "Union Square Academy for Health Sciences - [HS] 02M533", "lat": 40.7354911, "lng": -73.9874171, "station":{"name": "14 St-Union Sq", "lat": 40.735736, "lng": -73.990568, "routes": ["N", "Q", "R", "W"], "borough": "M"}},
{"name": "Harvest Collegiate High School - [HS] 02M534", "lat": 40.7366027, "lng": -73.9954298, "station":{"name": "6 Av", "lat": 40.737335, "lng": -73.996786, "routes": ["L"], "borough": "M"}},
{"name": "Manhattan Bridges High School - [HS] 02M542", "lat": 40.7652446, "lng": -73.9927375, "station":{"name": "50 St and 8th Av", "lat": 40.762456, "lng": -73.985984, "routes": ["C", "E"], "borough": "M"}},
{"name": "New Design High School - [HS] 02M543", "lat": 40.7173452, "lng": -73.9892929, "station":{"name": "Delancey St-Essex St", "lat": 40.718611, "lng": -73.988114, "routes": ["F"], "borough": "M"}},
{"name": "Academy for Software Engineering - [HS] 02M546", "lat": 40.735543, "lng": -73.987478, "station":{"name": "14 St-Union Sq", "lat": 40.735736, "lng": -73.990568, "routes": ["N", "Q", "R", "W"], "borough": "M"}},
{"name": "Richard R. Green High School of Teaching - [HS] 02M580", "lat": 40.7050989, "lng": -74.0128466, "station":{"name": "Bowling Green", "lat": 40.704817, "lng": -74.014065, "routes": ["4", "5"], "borough": "M"}},
{"name": "The High School of Fashion Industries - [HS] 02M600", "lat": 40.7454593, "lng": -73.9965165, "station":{"name": "23 St and 8th Av", "lat": 40.745906, "lng": -73.998041, "routes": ["C", "E"], "borough": "M"}},
{"name": "Humanities Preparatory Academy - [HS] 02M605", "lat": 40.743136, "lng": -74.002519, "station":{"name": "18 St", "lat": 40.74104, "lng": -73.997871, "routes": ["1"], "borough": "M"}},
{"name": "Chelsea Career and Technical Education High School - [HS] 02M615", "lat": 40.7246823, "lng": -74.0050859, "station":{"name": "Spring St and 6th Av", "lat": 40.726227, "lng": -74.003739, "routes": ["C", "E"], "borough": "M"}},
{"name": "Art and Design High School - [HS] 02M630", "lat": 40.759047, "lng": -73.9664806, "station":{"name": "Lexington Av/53 St", "lat": 40.757552, "lng": -73.969055, "routes": ["E", "M"], "borough": "M"}},
{"name": "The High School for Climate Justice - [HS] 02M655", "lat": 40.783409, "lng": -73.945859, "station":{"name": "96 St and 2nd Av", "lat": 40.784318, "lng": -73.947152, "routes": ["Q"], "borough": "M"}},
{"name": "West End Secondary School - [HS] 03M291", "lat": 40.7726113, "lng": -73.988348, "station":{"name": "66 St-Lincoln Center", "lat": 40.77344, "lng": -73.982209, "routes": ["1"], "borough": "M"}},
{"name": "The Maxine Greene HS for Imaginative Inquiry - [HS] 03M299", "lat": 40.7748463, "lng": -73.9856659, "station":{"name": "66 St-Lincoln Center", "lat": 40.77344, "lng": -73.982209, "routes": ["1"], "borough": "M"}},
{"name": "Urban Assembly School for Media Studies, The - [HS] 03M307", "lat": 40.7639993, "lng": -73.9908346, "station":{"name": "50 St and 8th Av", "lat": 40.762456, "lng": -73.985984, "routes": ["C", "E"], "borough": "M"}},
{"name": "The Urban Assembly School for Green Careers - [HS] 03M402", "lat": 40.785994, "lng": -73.97417, "station":{"name": "86 St and Broadway", "lat": 40.788644, "lng": -73.976218, "routes": ["1"], "borough": "M"}},
{"name": "The Global Learning Collaborative - [HS] 03M403", "lat": 40.785992, "lng": -73.9743724, "station":{"name": "86 St and Broadway", "lat": 40.788644, "lng": -73.976218, "routes": ["1"], "borough": "M"}},
{"name": "Wadleigh Secondary School for the Performing & Visual Arts - [HS] 03M415", "lat": 40.8025923, "lng": -73.9544319, "station":{"name": "116 St and Frederick Douglass Blvd", "lat": 40.805085, "lng": -73.954882, "routes": ["B", "C"], "borough": "M"}},
{"name": "Frank McCourt High School - [HS] 03M417", "lat": 40.785861, "lng": -73.9745414, "station":{"name": "86 St and Broadway", "lat": 40.788644, "lng": -73.976218, "routes": ["1"], "borough": "M"}},
{"name": "Beacon High School - [HS] 03M479", "lat": 40.7613016, "lng": -73.9960457, "station":{"name": "42 St-Port Authority Bus Terminal", "lat": 40.757308, "lng": -73.989735, "routes": ["A", "C", "E"], "borough": "M"}},
{"name": "High School for Law, Advocacy and Community Justice - [HS] 03M492", "lat": 40.774779, "lng": -73.98472, "station":{"name": "66 St-Lincoln Center", "lat": 40.77344, "lng": -73.982209, "routes": ["1"], "borough": "M"}},
{"name": "High School of Arts and Technology - [HS] 03M494", "lat": 40.7753818, "lng": -73.9860622, "station":{"name": "66 St-Lincoln Center", "lat": 40.77344, "lng": -73.982209, "routes": ["1"], "borough": "M"}},
{"name": "Manhattan / Hunter Science High School - [HS] 03M541", "lat": 40.7745619, "lng": -73.985282, "station":{"name": "66 St-Lincoln Center", "lat": 40.77344, "lng": -73.982209, "routes": ["1"], "borough": "M"}},
{"name": "Young Women's Leadership School - [HS] 03M610", "lat": 40.7971349, "lng": -73.9668867, "station":{"name": "103 St and Broadway", "lat": 40.799446, "lng": -73.968379, "routes": ["1"], "borough": "M"}},
{"name": "Special Music School - [HS] 03M859", "lat": 40.7752064, "lng": -73.9831573, "station":{"name": "66 St-Lincoln Center", "lat": 40.77344, "lng": -73.982209, "routes": ["1"], "borough": "M"}},
{"name": "Frederick Douglass Academy II Secondary School - [HS] 03M860", "lat": 40.8025691, "lng": -73.9541214, "station":{"name": "116 St and Frederick Douglass Blvd", "lat": 40.805085, "lng": -73.954882, "routes": ["B", "C"], "borough": "M"}},
{"name": "Esperanza Preparatory Academy - [HS] 04M372", "lat": 40.793049, "lng": -73.942651, "station":{"name": "110 St", "lat": 40.79502, "lng": -73.94425, "routes": ["6"], "borough": "M"}},
{"name": "Manhattan Center for Science and Mathematics - [HS] 04M435", "lat": 40.7943018, "lng": -73.9334062, "station":{"name": "116 St and Lexington Av", "lat": 40.798629, "lng": -73.941617, "routes": ["6"], "borough": "M"}},
{"name": "Park East High School - [HS] 04M495", "lat": 40.7902049, "lng": -73.9441678, "station":{"name": "103 St and Lexington", "lat": 40.7906, "lng": -73.947478, "routes": ["6"], "borough": "M"}},
{"name": "Central Park East High School - [HS] 04M555", "lat": 40.7936899, "lng": -73.9491583, "station":{"name": "103 St and Lexington", "lat": 40.7906, "lng": -73.947478, "routes": ["6"], "borough": "M"}},
{"name": "Heritage School, The - [HS] 04M680", "lat": 40.791964, "lng": -73.946878, "station":{"name": "103 St and Lexington", "lat": 40.7906, "lng": -73.947478, "routes": ["6"], "borough": "M"}},
{"name": "Eagle Academy for Young Men of Harlem - [HS] 05M148", "lat": 40.8115504, "lng": -73.9464769, "station":{"name": "135 St and St. Nicholas Av", "lat": 40.817894, "lng": -73.947649, "routes": ["B", "C"], "borough": "M"}},
{"name": "The Urban Assembly School for Global Commerce - [HS] 05M157", "lat": 40.806632, "lng": -73.938438, "station":{"name": "125 St and Lexington Av", "lat": 40.804138, "lng": -73.937594, "routes": ["4", "5", "6"], "borough": "M"}},
{"name": "Mott Hall High School - [HS] 05M304", "lat": 40.817349, "lng": -73.94745, "station":{"name": "135 St and St. Nicholas Av", "lat": 40.817894, "lng": -73.947649, "routes": ["B", "C"], "borough": "M"}},
{"name": "Columbia Secondary School - [HS] 05M362", "lat": 40.8106437, "lng": -73.9560287, "station":{"name": "125 St and St Nicholas Av", "lat": 40.811109, "lng": -73.952343, "routes": ["A", "B", "C", "D"], "borough": "M"}},
{"name": "Urban Assembly School for the Performing Arts - [HS] 05M369", "lat": 40.815709, "lng": -73.9556642, "station":{"name": "125 St and Broadway", "lat": 40.815581, "lng": -73.958372, "routes": ["1"], "borough": "M"}},
{"name": "Frederick Douglass Academy - [HS] 05M499", "lat": 40.824267, "lng": -73.936642, "station":{"name": "Harlem-148 St", "lat": 40.82388, "lng": -73.93647, "routes": ["3"], "borough": "M"}},
{"name": "Thurgood Marshall Academy for Learning and Social Change - [HS] 05M670", "lat": 40.8152484, "lng": -73.9443203, "station":{"name": "135 St and Lenox Av", "lat": 40.814229, "lng": -73.94077, "routes": ["2", "3"], "borough": "M"}},
{"name": "High School for Mathematics, Science and Engineering at City College - [HS] 05M692", "lat": 40.8214739, "lng": -73.9490389, "station":{"name": "137 St-City College", "lat": 40.822008, "lng": -73.953676, "routes": ["1"], "borough": "M"}},
{"name": "Inwood Early College for Health and Information Technologies - [HS] 06M211", "lat": 40.8659143, "lng": -73.925157, "station":{"name": "Dyckman St and Broadway", "lat": 40.865491, "lng": -73.927271, "routes": ["A"], "borough": "M"}},
{"name": "City College Academy of the Arts - [HS] 06M293", "lat": 40.8608456, "lng": -73.9301494, "station":{"name": "Dyckman St and Nagle Av", "lat": 40.860531, "lng": -73.925536, "routes": ["1"], "borough": "M"}},
{"name": "Community Health Academy of the Heights - [HS] 06M346", "lat": 40.833612, "lng": -73.942198, "station":{"name": "157 St", "lat": 40.834041, "lng": -73.94489, "routes": ["1"], "borough": "M"}},
{"name": "Washington Heights Expeditionary Learning School - [HS] 06M348", "lat": 40.8491088, "lng": -73.9310992, "station":{"name": "181 St and St Nicholas Av", "lat": 40.849505, "lng": -73.933596, "routes": ["1"], "borough": "M"}},
{"name": "The College Academy - [HS] 06M462", "lat": 40.856121, "lng": -73.926333, "station":{"name": "191 St", "lat": 40.855225, "lng": -73.929412, "routes": ["1"], "borough": "M"}},
{"name": "High School for Media and Communications - [HS] 06M463", "lat": 40.8561208, "lng": -73.9263326, "station":{"name": "191 St", "lat": 40.855225, "lng": -73.929412, "routes": ["1"], "borough": "M"}},
{"name": "High School for Law and Public Service - [HS] 06M467", "lat": 40.855894, "lng": -73.926033, "station":{"name": "191 St", "lat": 40.855225, "lng": -73.929412, "routes": ["1"], "borough": "M"}},
{"name": "High School for Health Careers and Sciences - [HS] 06M468", "lat": 40.8558937, "lng": -73.9260333, "station":{"name": "191 St", "lat": 40.855225, "lng": -73.929412, "routes": ["1"], "borough": "M"}},
{"name": "A. Philip Randolph Campus High School - [HS] 06M540", "lat": 40.8183585, "lng": -73.9499696, "station":{"name": "135 St and St. Nicholas Av", "lat": 40.817894, "lng": -73.947649, "routes": ["B", "C"], "borough": "M"}},
{"name": "Gregorio Luperon High School for Science and Mathematics - [HS] 06M552", "lat": 40.8382264, "lng": -73.9385356, "station":{"name": "168 St", "lat": 40.840719, "lng": -73.939561, "routes": ["A", "C"], "borough": "M"}},
{"name": "Democracy Preparatory Endurance Charter School - [HS] 84M065", "lat": 40.801463, "lng": -73.93507, "station":{"name": "125 St and Lexington Av", "lat": 40.804138, "lng": -73.937594, "routes": ["4", "5", "6"], "borough": "M"}},
{"name": "Democracy Preparatory Harlem Charter School - [HS] 84M481", "lat": 40.8115504, "lng": -73.9464769, "station":{"name": "135 St and Lenox Av", "lat": 40.814229, "lng": -73.94077, "routes": ["2", "3"], "borough": "M"}},
{"name": "Harlem Prep Charter School - [HS] 84M708", "lat": 40.7886777, "lng": -73.9448453, "station":{"name": "103 St and Lexington", "lat": 40.7906, "lng": -73.947478, "routes": ["6"], "borough": "M"}},
]

def get_distances(origins):
    
    for count, origin in enumerate(origins):
        if(count!=len(origins)-1):  
            origin_str =f"{origin['lat']},{origin['lng']}"       
            dest = origin['station']
            destination_str = f"{dest['lat']},{dest['lng']}"
            
            hs = f"{origin['name']}"
            sub = f"{dest['name']}"
           
            
            url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin_str}&destinations={destination_str}&mode=subway&key={API_key}"

            
            response = requests.get(url)
            data = response.json()
            #print(data,",")
            
            origin_addresses = hs
            destination_addresses = sub
            rows = data['rows']
            for i, row in enumerate(rows):
                elements = row['elements']
                for j, element in enumerate(elements):
                    distancekm = element['distance']['text']
                    distancem = element['distance']['value']
                    durationmin = element['duration']['text']
                    durationsec = element['duration']['value']
                    #origin = origin_addresses[0]  #
                    #destination = destination_addresses[j]
                        
                    new_dict = {
                        'origin': origin_addresses,
                        'destination': destination_addresses,
                        'distancekm': distancekm,
                        'distancem': distancem,
                        'durationmin': durationmin,
                        'durationsec': durationsec
                    }
                print(new_dict,",")
                
            
get_distances(origins)
