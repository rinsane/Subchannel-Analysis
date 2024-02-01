import csv

l = ["data1", "data2", "data3"]
data1 = ['1', '2', '3', '4' ]
data2 = ["rishabh", "hitesh", "roopesh", "kannan"]
data3 = [";[';]", "checker", "&^&%&", "()*(@)"]

datas = zip(data1, data2, data3)
print(datas)

with open("results.csv", "w", newline='') as datasheet:
    writer = csv.writer(datasheet)
    
    writer.writerow(l)
    # Use writerows to write multiple rows
    writer.writerows(datas)

