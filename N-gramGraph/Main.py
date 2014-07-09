# -*- coding: utf-8 -*-
from networkx.classes.graph import Graph

__author__ = 'andocavallari'
import networkx as nx
import Ngram as gr
import matplotlib.pyplot as plt


#text
n = "A survivor. That’s how some Republicans think of Senator Mary Landrieu, a Louisiana Democrat who seemed to defy political gravity by winning two tough re-election campaigns,"+\
    " even while Louisiana, like the rest of the Deep South, became unshakably Republican.To win re-election, Ms. Landrieu will need to defy this anti-Democratic trend once again. Many believe she can. Despite fierce regional headwinds, her support seems remarkably resilient. Even as her party’s presidential nominee lost ground between each election, her share of the vote increased each time.But an analysis of election results, turnout data and exit polls shows that Ms. Landrieu is not immune to the anti-Democratic trend. She lost ground among Louisiana’s white voters between 2002 and 2008; the decline was obscured by high turnout among blacks in 2008’s strong Democratic showing, with blacks offering her overwhelming support. Ms. Landrieu’s route to victory looks exceptionally narrow this year, if it exists at all.Louisiana, the state where blacks represent the nation’s second-largest share of the population, saw a surge in turnout among blacks between Ms. Landrieu’s last two elections, rising from 27.1 percent of the vote in the 2002 Senate runoff to 29.5 percent in 2008. Yet Ms. Landrieu’s share of the total vote increased only slightly, moving from 51.7 to 52.1 percent.The implication — even under the assumption that she performed as well among black voters in 2002 as exit polls show she did in 2008 — is that her support among white voters dropped by at least 2 points, to an estimated 33 percent in 2008. And the decline may have been even greater, since Ms. Landrieu probably did worse among black voters in 2002, a good year for Republicans and without President Obama’s candidacy. If she won fewer black voters in 2002, then she must have won more white voters — and the decline between 2002 and 2008 was therefore greater.The decline of Ms. Landrieu’s support in such a Democratic year reflects the strength of an inexorable anti-Democratic tide among the state’s white voters. Unlike those in most states, Louisiana’s"+\
    " most Democratic white voters are its oldest ones (over 65), who formed many of their views when Democrats reigned in the South. Older whites offered more support to Ms. Landrieu and Charlie Melancon, the Democratic Senate candidate in 2010, than any other age group of whites. But the most Democratic seniors, who came of age during the Roosevelt years, are a shrinking segment of the electorate. Between 2002 and 2008, that generation fell to 2 percent from 8 percent of eligible voters. And as has happened elsewhere in the South, the Democrats’ views on cultural issues have alienated conservative white voters.The deterioration of Democratic strength among Louisiana’s white voters is also evident in voter registration figures and presidential election results. Between 2002 and 2008, the Democratic advantage in Louisiana white voter registration slipped to 4 percentage points from 17. On Election Day in 2008, registered white Democrats outnumbered white Republicans by a mere 1 percentage point, down from 16 points in 2002. The shift is just as striking in the presidential election results. In 1996, President Clinton received about 37 percent of Louisiana’s white vote. But that number has steadily declined: Al Gore received 27 percent, John Kerry received 24 percent, and President Obama won less than 14 percent in 2012.Compared with these figures, Ms. Landrieu’s slight decline still suggests an impressive base of support. But Ms. Landrieu suffered huge losses in some rural counties, performing more than 10 points worse among white voters. Statewide, these losses were largely canceled by an increase in Ms. Landrieu’s support in the New Orleans area, where there are more moderate voters.The anti-Democratic trend is, if anything, gaining speed. Soon after the 2010 midterms, Republicans seized a voter registration advantage among whites, and it has steadily grown to a 7-point edge today. In 2010, Republicans reduced the Democratic congressional delegation to a single seat, the majority-minority district representing New Orleans.Despiteconfessing to participatingin a prostitution ring, Senator David Vitter,"+\
    " a Republican, won re-election with 58 percent of the vote. In 2011, Republicans seized every statewide office for the first time in the state’s history. And on Election Day 2012, registered white Republicans outnumbered white Democrats by a 10-point margin.To win in 2014, with lower black turnout likely, Ms. Landrieu cannot afford any additional decline in her support among white voters. But 2014 promises far more challenging conditions, and her losses among white voters could easily surpass those from 2008, especially if one assumes that she was near her ceiling in the New Orleans area. Holding onto her territory will be hard enough. For instance, Ms. Landrieu easily won Jefferson Parish, encompassing most of New Orleans’s suburbs, which never voted for Mr. Clinton or President Carter, and which never previously came close to supporting Ms. Landrieu.All considered, it is unclear whether there is still a path for her to reach 50 percent — and while a third-party candidate might allow her to squeak by in another state, Louisiana’s runoff system requires her to clear 50 percent to win re-election.The limited polling data confirms that 2014 is not 2008. The only live interview surveys contacting voters with cellphones are from Southern Media and Opinion Research, which found Ms. Landrieu with just 41 percent of the vote in November, and from The New York Times/Kaiser Family Foundation, which found Ms. Landrieu at 42 percent. If there’s still a way for Ms. Landrieu to win, she has a long way to go.• • •How this was calculated:Ms. Landrieu’s share of the white vote was estimated using Louisiana’sturnout data by race, the exit polls and the actual results. We assume that Ms. Landrieu won 96 percent of black voters statewide, the same as the results reflected by the exit polls in 2008, and 56 percent of votes of other nonwhite voters, the share won by southern Democratic House candidates in the 2008 exit polls. Then, we can deduce her share of the white vote. There were no exit polls in 2002, so we assume that Ms. Landrieu did as well among nonwhite voters in 2002 as she did in 2008."
grams = gr.getGram(n)
Graph = gr.graph_node_computation(grams)



#Drawing graph
pos = nx.spring_layout(Graph)
nx.draw_circular(Graph)
#Drawing graph weight, specifiy edge labels explicitly

# edge_labels = dict([((u,v,),d['weight'])
#                   for u,v,d in Graph.edges(data=True)])
# nx.draw_networkx_edge_labels(Graph,pos,edge_labels=edge_labels)

plt.show()

#print(Graph.nodes())
#print(Graph.edges())

#for i,j in Graph.edges():
#    print(i + ' - '+ j +' , ' + str(Graph[i][j]['weight']))



