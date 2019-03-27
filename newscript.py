import os
import numpy as np
version = 1
test = 1
statement = 1

f = open("./runall.sh")
oldscript = f.readlines()

for version in range(1,42):import os
import numpy as np
import time
time_start=time.time()
version = 1
test = 1
statement = 1

os.system("gcc -O2 ../source.alt/source.orig/tcas.c -o ../source/tcas.exe -w")
os.system("./runall.sh  > /dev/null")
f = open("runall.sh")
oldscript = f.readlines()

for version in range(1,42):
	LF = 0
	print('>>>>>>>>running version '+str(version))
	matrix = np.zeros((1609,100))
	os.system("gcc -fprofile-arcs -ftest-coverage -o ../versions.alt/versions.orig/v"+str(version)+"/tcas.exe ../versions.alt/versions.orig/v"+str(version)+"/tcas.c -w")
	os.system("cp ../versions.alt/versions.orig/v"+str(version)+"/tcas.exe ../source")
	os.system("mv ../scripts/tcas.gcno ../versions.alt/versions.orig/v"+str(version))
	os.system("mkdir ../newoutputs/v"+str(version)+" -p")
	oldscript = [line for line in oldscript if(not line.startswith("echo"))]
	for line in oldscript:#test
		os.system(line.replace('../outputs', '../newoutputs/v'+str(version)))
		os.system("mv ../scripts/tcas.gcda ../versions.alt/versions.orig/v"+str(version))
		os.system("gcov -b ../versions.alt/versions.orig/v"+str(version)+"/tcas.c > /dev/null")
		g = open("tcas.c.gcov")
		for line in g.readlines():#statement
			if(line.strip()[0] in ('1','2','3','4','5','6','7','8')):
				matrix[test-1][statement-1] = int(line.strip()[0])
				matrix[-1][statement-1] += 1
				statement += 1
			elif(line.strip()[0] == '#'):
				matrix[test-1][statement-1] = 0
				statement += 1
		LF = statement - 1
		statement = 1
		test += 1
		g.close()
	test = 1
	np.savetxt("../versions.alt/versions.orig/v"+str(version)+"/matrix",matrix[:,0:LF],fmt='%d')
	false_num = 0
	true_num = 0
	LH = 0
	max_num = 0
	min_num = 1608
	sum_num = 0
	mean_num = 0
	for i in range(1, 1609):
		tmp = os.system("diff ../outputs/t"+str(i)+" ../newoutputs/v"+str(version)+"/t" + str(i) + ">/dev/null")
		if tmp != 0:
			false_num += 1
		else:
			true_num += 1
	for i in range(0,LF):
		if(matrix[-1][i] != 0):
			LH += 1	
		if(matrix[-1][i] > max_num):
			max_num = matrix[-1][i]
		if(matrix[-1][i] < min_num):
			min_num = matrix[-1][i]
		sum_num += matrix[-1][i]
	linecov = round(LH/LF,4)
	mean_num = round(sum_num/LF,2)
	r = open("../versions.alt/versions.orig/v"+str(version)+"/result","w+")
	r.write("输出正确的用例个数: "+str(true_num)+"\n输出错误的用例个数: "+str(false_num))
	r.write("\n可执行语句个数: "+str(LF)+"\n被执行语句个数: "+str(LH))
	r.write("\n语句覆盖率: "+("%.2f%%" % (linecov * 100)))
	r.write("\n被执行最多次数的语句执行次数: "+str(max_num))
	r.write("\n被执行最少次数的语句执行次数: "+str(min_num))
	r.write("\n每个语句平均被执行次数: "+str(mean_num))
	r.close()
f.close()
time_end=time.time()
print('time cost',time_end-time_start,'s')
	#version
	#this module is used for running test language----shell
	matrix = np.zeros((1609,65))
	os.system("gcc -fprofile-arcs -ftest-coverage -o ../versions.alt/versions.orig/v"+str(version)+"/tcas.exe ../versions.alt/versions.orig/v"+str(version)+"/tcas.c\n")
	os.system("cp ../versions.alt/versions.orig/v"+str(version)+"/tcas.exe ../source\n")
	os.system("mv ../scripts/tcas.gcno ../versions.alt/versions.orig/v"+str(version)+"\n")
	os.system("mkdir ../outputs/v"+str(version)+"\n")
	oldscript = [line for line in oldscript if(not line.startswith("echo"))]
	for line in oldscript:
		#test case
		os.system(line.replace('../outputs', '../outputs/v'+str(version)))
		os.system("mv ../scripts/tcas.gcda ../versions.alt/versions.orig/v"+str(version)+"\n")
		os.system("gcov -b ../versions.alt/versions.orig/v"+str(version)+"/tcas.c > /dev/null")
		g = open("tcas.c.gcov")
		#this module is used for generate test case matrix
		for line in g.readlines():
			#statement
			if(line.strip()[0] in ('1','2','3','4','5','6','7','8')):
				matrix[test-1][statement-1] = int(line.strip()[0])
				matrix[-1][statement-1] += 1
				statement += 1
			elif(line.strip()[0] == '#'):
				matrix[test-1][statement-1] = 0
				statement += 1
		statement = 1
		test += 1
		g.close()
	test = 1
	np.savetxt("../versions.alt/versions.orig/v"+str(version)+"/matrix",matrix,fmt='%d')
	#this module is used for print out results
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
f.close()
