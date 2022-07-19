import json

# Opening JSON file
f = open('data.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
  
# Iterating through the json
# list
for i in data:
    #print(i)
    print (data[i])
  
# Closing file
f.close()