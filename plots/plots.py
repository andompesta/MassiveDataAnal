import matplotlib
import matplotlib.pyplot as plt

def plotData(datapoints,outputFile,xLabel="",yLabel="",xBounds = None,yBounds = None,color = 'k',alpha = 1.0) :

	fig = plt.figure(figsize=(12, 10)) # creates the figure
	ax = fig.add_subplot(111) # creates the subplot (as big as the figure)

	lineStyles = ['-','--',':','-.','.',',','o','v','^','<','>']

	if xBounds != None : ax.set_xlim([xBounds[0],xBounds[1]])
	if yBounds != None : ax.set_ylim([yBounds[0],yBounds[1]])

	i = 0
	for x,y,lab in datapoints :
		ax.plot(x,y,lineStyles[i%len(lineStyles)],color=color,alpha=alpha,label=lab)
		i += 1

	ax.set_xlabel(xLabel,fontsize=20)
	ax.set_ylabel(yLabel,fontsize=20)


	ax.set_xticks(range(min(x), max(x)+1))
	#ax.set_yticks(range(0, max(x)+1))

	plt.setp(ax.get_xticklabels(), fontsize=15)
	plt.setp(ax.get_yticklabels(), fontsize=15)

	# legend
	leg = plt.legend(loc='lower left',prop={'size':12})
	leg.get_frame().set_alpha(0.9)

	fig.savefig(outputFile)

def plotTheWorld(inputPath,outputFolder) :
	with open(inputPath) as f :
		data = [map(int,line.strip().split('\t')) for line in f if line.strip() != '']

		# fixed window

		for i,window in enumerate(list(set(map(lambda x:x[2],data)))) :
			# fixed rank
			datapoints = []
			for rank in set(map(lambda x:x[0],data)) :
				xyValues = [(x[1],x[-1]) for x in data if x[0]==rank and x[2]==window]
				x = map(lambda x:x[0],xyValues)
				y = map(lambda x:x[1],xyValues)
				lab = "Rank " + str(rank)
				datapoints.append((x,y,lab))
			plotData(datapoints,outputFolder+'win_'+str(i)+'_ranks.pdf',xLabel="Neighborhood distance",yLabel="Execution time (ms)",xBounds=(min(x)-1,max(x)+1))

		for i,window in enumerate(list(set(map(lambda x:x[2],data)))) :
			# fixed neighborhood distance
			datapoints = []
			for ndist in set(map(lambda x:x[1],data)) :
				xyValues = [(x[0],x[-1]) for x in data if x[1]==ndist and x[2]==window]
				x = map(lambda x:x[0],xyValues)
				y = map(lambda x:x[1],xyValues)
				lab = "Neigh. dist. " + str(ndist)
				datapoints.append((x,y,lab))
			plotData(datapoints,outputFolder+'win_'+str(i)+'_ndists.pdf',xLabel="Rank",yLabel="Execution time (ms)",xBounds=(min(x)-1,max(x)+1))

from sys import argv
plotTheWorld(argv[1],argv[2])
