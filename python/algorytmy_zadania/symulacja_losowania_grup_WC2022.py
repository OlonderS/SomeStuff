"""Symulacja losowania grup Mistrzostw Świata 2022 dla kraju w zmiennej 'name'"""
list_conf = ["AFC", "CAF", "CONCACAF", "CONMEBOL", "OFC", "UEFA"]
 
pot = [ #1
        [{"name" : "Katar", 
         "conf": ["AFC"]}, 
         {"name" : "Brazylia", 
         "conf": ["CONMEBOL"]},
         {"name" : "Belgia", 
         "conf": ["UEFA"]},
         {"name" : "Francja", 
         "conf": ["UEFA"]},
         {"name" : "Argentyna", 
         "conf": ["CONMEBOL"]},
         {"name" : "Anglia", 
         "conf": ["UEFA"]},
         {"name" : "Hiszpania", 
         "conf": ["UEFA"]},
         {"name" : "Portugalia", 
         "conf": ["UEFA"]}],
        #2
        [{"name" : "Meksyk", 
         "conf": ["CONCACAF"]}, 
         {"name" : "Holandia", 
         "conf": ["UEFA"]},
         {"name" : "Dania", 
         "conf": ["UEFA"]},
         {"name" : "Niemcy", 
         "conf": ["UEFA"]},
         {"name" : "Urugwaj", 
         "conf": ["CONMEBOL"]},
         {"name" : "Szwajcaria", 
         "conf": ["UEFA"]},
         {"name" : "USA", 
         "conf": ["CONCACAF"]},
         {"name" : "Chorwacja", 
         "conf": ["UEFA"]}],
        #3
        [{"name" : "Senegal", 
         "conf": ["CAF"]}, 
         {"name" : "Iran", 
         "conf": ["AFC"]},
         {"name" : "Japonia", 
         "conf": ["AFC"]},
         {"name" : "Maroko", 
         "conf": ["CAF"]},
         {"name" : "Serbia", 
         "conf": ["UEFA"]},
         {"name" : "Polska", 
         "conf": ["UEFA"]},
         {"name" : "Korea Południowa", 
         "conf": ["AFC"]},
         {"name" : "Tunezja", 
         "conf": ["CAF"]}],
        #4
        [{"name" : "Kamerun", 
         "conf": ["CAF"]}, 
         {"name" : "Kanada", 
         "conf": ["CONCACAF"]},
         {"name" : "Ekwador", 
         "conf": ["CONMEBOL"]},
         {"name" : "Arabia Saudyjska", 
         "conf": ["AFC"]},
         {"name" : "Ghana", 
         "conf": ["CAF"]},
         {"name" : "Baraz UEFA", 
         "conf": ["UEFA"]},
         {"name" : "Baraz AFC/CONMEBOL", 
         "conf": ["AFC", "CONMEBOL"]},
         {"name" : "Baraz CONCACAF/OFC", 
         "conf": ["CONCACAF", "OFC"]}]]

name = "Polska" #!!!
 
result_tmp = []
index=0
pots = [1,2,3,4]
 
for t1 in pot[0]:
    for t2 in pot[1]:
        for t3 in pot[2]:
            for t4 in pot[3]:
                tmp = [t1]
                tmp.append(t2)
                tmp.append(t3)
                tmp.append(t4)
                flag = True
                conf_tmp = []
                for i in pots:
                    for c in tmp[i-1]["conf"]:
                        conf_tmp.append(c)
                for i in list_conf:
                    count_tmp = conf_tmp.count(i)
                    if i == "UEFA":
                        if count_tmp > 2 or count_tmp == 0:
                            flag = False
                    else:
                        if count_tmp > 1:
                            flag = False
                if flag == True:
                    result_tmp.append(tmp)
 
pot_index = 0
for i in pots:
    for j in range(len(pot[i-1])):
        if pot[i-1][j]["name"] == name:
            pot_index = i
            break
 
result = []
for i in result_tmp:
    if i[pot_index - 1]["name"] == name:
        result.append(i)
denominator = len(result)
 
result2 = []
for i in result:
    tmp_result = []
    for j in pots:
        result2.append(i[j-1]["name"])
        
count_list = dict()
for i in pot:
    for j in range(len(i)):
        count_list[i[j]["name"]] = 0
 

for i in result2:
    count_list[i] = count_list[i] + 1
          
pots.remove(pot_index)
print(name, end=" ")
print( "z koszyka", end=" ")
print(pot_index)
for i in pots:
    print("Koszyk ",end="")
    print(i)
    for tmp in pot[i-1]:
        counter = count_list[tmp["name"]]
        print(str(round(100*counter/denominator,2)),end="% ")
        print(tmp["name"])
