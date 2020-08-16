import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt

data = pd.read_json('AY_30_proc.json')

cloud_list = data['Breakdown-advice']

comment_words = '' 
stopwords = set(STOPWORDS) 
  
# iterate through the csv file 
columns = ['greetings', 'story', 'advice', 'others']
for column in columns:
	print(column)
	for val in data['Breakdown-' + column]: 
		  
		# typecaste each val to string 
		val = str(val) 
	  
		# split the value 
		tokens = val.split() 
		  
		# Converts each token into lowercase 
		for i in range(len(tokens)): 
		    tokens[i] = tokens[i].lower() 
		  
		comment_words += " ".join(tokens)+" "

	wordcloud = WordCloud(width = 600, height = 600, 
		            background_color ='white',
		            include_numbers=True,
		            collocations=True,
		            stopwords = stopwords).generate(comment_words)  
#		            min_font_size = 20,
#		            max_font_size = 200
		            
	plt.figure(figsize = (6, 6), facecolor = None) 
	plt.imshow(wordcloud) 
	plt.axis("off") 
	plt.tight_layout() 
	plt.savefig('cloud_' + column + '.jpg')
	plt.close()
