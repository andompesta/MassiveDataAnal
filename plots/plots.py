import matplotlib
import matplotlib.pyplot as plt

def plotData(x,y,outputFile,xLabel="",yLabel="",xBounds = None,yBounds = None,color = 'k',alpha = 1.0) :

	fig = plt.figure(figsize=(10, 10)) # creates the figure
	ax = fig.add_subplot(111) # creates the subplot (as big as the figure)



	if xBounds != None : ax.set_xlim([xBounds[0],xBounds[1]])
	if yBounds != None : ax.set_ylim([yBounds[0],yBounds[1]])

	#ax.plot(x,y,'--', color=color,alpha=alpha)
	ax.plot(x,y, color=color,alpha=alpha)

	ax.set_xlabel(xLabel,fontsize=30)
	ax.set_ylabel(yLabel,fontsize=30)


	ax.set_xticks(range(min(x), max(x)+1))
	#ax.set_yticks(range(0, max(x)+1))

	plt.setp(ax.get_xticklabels(), fontsize=15)
	plt.setp(ax.get_yticklabels(), fontsize=15)

	fig.savefig(outputFile)

def plotTheWorld(inputPath,outputFolder) :
	with open(inputPath) as f :
		data = [map(int,line.strip().split('\t')) for line in f if line.strip() != '']

		# fixed window

		for i,window in enumerate(list(set(map(lambda x:x[2],data)))) :
			# fixed rank
			for rank in set(map(lambda x:x[0],data)) :
				xyValues = [(x[1],x[-1]) for x in data if x[0]==rank and x[2]==window]
				x = map(lambda x:x[0],xyValues)
				y = map(lambda x:x[1],xyValues)
				
				plotData(x,y,outputFolder+'win_'+str(i)+'_rank_'+str(rank)+'.pdf',xLabel="Neighborhood distance",yLabel="Execution time (ms)",xBounds=(min(x)-1,max(x)+1))

		for i,window in enumerate(list(set(map(lambda x:x[2],data)))) :
			# fixed neighborhood distance
			for ndist in set(map(lambda x:x[1],data)) :
				xyValues = [(x[0],x[-1]) for x in data if x[1]==ndist and x[2]==window]
				x = map(lambda x:x[0],xyValues)
				y = map(lambda x:x[1],xyValues)

				plotData(x,y,outputFolder+'win_'+str(i)+'_ndist_'+str(ndist)+'.pdf',xLabel="Rank",yLabel="Execution time (ms)",xBounds=(min(x)-1,max(x)+1))

from sys import argv
plotTheWorld(argv[1],argv[2])
