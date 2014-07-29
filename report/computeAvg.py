
with open('evaluation.txt') as f :
	table = [map(int,line.strip().split()[1:]) for line in f if len(line)>1 and line[1]==')']

	shifts = ['Cern1','Cern2','FortHood','Hangover','Jackson1','Jackson2','SwineFlu']
	rowAvgs = map(lambda r: float(sum(r))/len(r),table)
	
	texTable = []
	for i in range(7) :
		texTable.append(rowAvgs[i*4:(i*4)+4])

	texOutput = '\\begin{table*}[htbp]\n'
	texOutput += '\\centering\n'
	texOutput += '\\begin{tabular}{lccccc}\n\n'

	texOutput += '\\textbf{Contr. point:} & \\textbf{SS:} & \\textbf{TF-IDF:} & \\textbf{LSI:} & \\textbf{NGG:} & \\textbf{Avg:} \\\\\n'
	texOutput += '\\hline\n'
	


	columnSum = [0,0,0,0,0]
	for i in range(len(texTable)) :
		texTable[i].append(sum(texTable[i])/len(texTable[i]))
		for j in range(len(texTable[i])) :
			columnSum[j] += texTable[i][j]
		texOutput += shifts[i] + ''.join(map(lambda x : ' & %.2f' % x,texTable[i])) + ' \\\\\n'
	
	texOutput += '\\hline\n'
	texOutput += '\\textbf{Avg:}' + ''.join(map(lambda x : ' & %.2f' % (x/7),columnSum)) + ' \\\\\n'

	texOutput += '\\hline\n'
	texOutput += '\\end{tabular}\n'
	texOutput += '\\caption{User evaluation}\n'
	texOutput += '\\label{tab:UserEvaluation}\n'
	texOutput += '\\end{table*}\n'


with open('chapters/results/UserEvaluation.tex','w') as f :
	f.write(texOutput)
