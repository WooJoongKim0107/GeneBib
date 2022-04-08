These files are the raw data used for the second half of this project.

All files given here are identical to the data used for our work, except
	1. three files <paper_hitgene_list.txt>, <patent_hitgene_list.txt> and <paper_hitgene_list_gon.txt> are just subset of the original data: they are demo-version of real data. 
	
	If you need the full data rather than demo, then carefully follow the first half of this project or email to "wcjung@unist.ac.kr" or "henrik@unist.ac.kr"
	
	2. <yearly_new_genes.csv> corresponds to 
		Debuts('any', n=1, load=False).transposed.items()
	if the three files mentioned above are replaced by the original data.
	See <TimeSeries/debut.py> for details of the above statement.
	
	3. <demo_initial_paras.pkl> corresponds to
		random_initial_paras(100, BOUNDARIES)
	See <fitting.py> for details of the above statement.