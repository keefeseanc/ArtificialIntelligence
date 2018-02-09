column = [[39, 105, 81, 15],[45, 96, 60, 9],[36, 69, 39, 6]]
row = [[39, 45, 36],[105, 96, 69],[81,60, 39],[15, 9, 6]]

totalAccidents = 600

print "\njoint probability"
for i in column:
	for j in i:
		print j/ float(totalAccidents) 

print "\nmarginal probability"
for i in column:
	total = 0
	for j in i:
		total += j
	print total / float(totalAccidents)

for i in row:
        total = 0
        for j in i:
                total += j
        print total / float(totalAccidents)

print "\nconditional probability"
for i in column:
	total = 0
	for j in i:
		total += j
	for j in i:
		print j / float(total)

for i in row:
        total = 0
        for j in i:
                total += j
        for j in i:
                print j / float(total)
      

print "\nrandom probability 1"
total = 45 + 36 + 96 + 69
print total / float(totalAccidents)

print "\nrandom probability 2"
total = 81 + 15
print total / float(39 + 105 + 81 + 15)

