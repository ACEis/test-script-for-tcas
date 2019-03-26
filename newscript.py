import os
import numpy as np
version = 3         #每次测试时请按照需求改变脚本号
test = 1

#生成shell脚本
f = open("./runall.sh")
script = open("runv"+str(version),'w+')
oldscript = f.readlines()


script.write("gcc -fprofile-arcs -ftest-coverage -o ../versions.alt/versions.orig/v"+str(version)+"/tcas.exe ../versions.alt/versions.orig/v"+str(version)+"/tcas.c\n")
script.write("cp ../versions.alt/versions.orig/v"+str(version)+"/tcas.exe ../source\n")
script.write("mv ../scripts/tcas.gcno ../versions.alt/versions.orig/v"+str(version)+"\n")
script.write("mkdir ../outputs/v"+str(version)+"\n")
for line in oldscript:
	if(not line.startswith("echo")):
		script.write(line.replace('../outputs', '../outputs/v'+str(version)))
		script.write("mv ../scripts/tcas.gcda ../versions.alt/versions.orig/v"+str(version)+"\n")
		script.write("gcov -b ../versions.alt/versions.orig/v"+str(version)+"/tcas.c > ../versions.alt/versions.orig/v"+str(version)+"/t"+str(test)+"\n")
		script.write("lcov -d ../versions.alt/versions.orig/v"+str(version)+"/ -c -o ../versions.alt/versions.orig/v"+str(version)+"/r"+str(test)+".info >/dev/null\n")
		test += 1
f.close()
script.close()
os.system('chmod 777 runv'+str(version))
os.system('./runv'+str(version))


#生成测试矩阵
test_begin = 1
test_end   = 1608
statement_num = 65
cursor = 0
matrix = np.zeros((1609,65))
for i in range(test_begin, test_end + 1):
	read_file = open("../versions.alt/versions.orig/v"+str(version)+"/r"+str(i)+".info")
	info = read_file.readlines()
	for line in info:
		if(line.startswith("DA:")):
			matrix[i-1][cursor] = int(line.strip()[-1])
			cursor = cursor + 1
	cursor = 0
	read_file.close()

#for the statements are runed by how many tests in one version
for cursor in range(0,65):
	for test_num in range(0,1608):
		if(matrix[test_num][cursor] != 0):
			matrix[-1][cursor] = matrix[-1][cursor] + 1
save_file = open("../versions.alt/versions.orig/v"+str(version)+"/matrix","w+")
np.savetxt("../versions.alt/versions.orig/v"+str(version)+"/matrix",matrix,fmt='%d')
save_file.close()


#写入结果
false_num = 0
true_num = 0
LF = 65
LH = 0
max_num = 0
min_num = 1608
sum_num = 0
mean_num = 0
for i in range(1, 1609):
	tmp = os.system("diff ../outputs/v0/t"+str(i)+" ../outputs/v"+str(version)+"/t" + str(i) + ">/dev/null")
	if tmp != 0:
		false_num += 1
	else:
		true_num += 1

for i in range(0,LF):
	if(matrix[-1][i-1] != 0):
		LH += 1	
	if(matrix[-1][i-1] > max_num):
		max_num = matrix[-1][i-1]
	if(matrix[-1][i-1] < min_num):
		min_num = matrix[-1][i-1]
	sum_num += matrix[-1][i-1]
linecov = round(LH/LF,4)
mean_num = round(sum_num/LF,2)

r = open("../versions.alt/versions.orig/v"+str(version)+"/result","w+")
r.write("True test number: "+str(true_num)+"\nFalse test number: "+str(false_num))
r.write("\nThe total statements: "+str(LF)+"\nThe statements executed: "+str(LH))
r.write("\nThe line coverage: "+("%.2f%%" % (linecov * 100)))
r.write("\nMax number of executed times: "+str(max_num))
r.write("\nMin number of executed times: "+str(min_num))
r.write("\nMean number of execute times: "+str(mean_num))
r.close()





		
