import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

articles = pd.read_csv('D:/Skill Assessment2/articles.BACE1.csv')
authors = pd.read_csv('D:/Skill Assessment2/authors.BACE1.csv')
paper = pd.read_csv('D:/Skill Assessment2/paper_counts.csv')

articles['AuthorFullname'] = articles['FirstAuthorForename'] + ' ' + articles['FirstAuthorLastname']
authors['AuthorFullname'] = authors['AuthorForename'] + ' ' + authors['AuthorLastname']


#Filter out all articles about 'BACE1'
f_articles = articles[articles['Title'].str.contains('BACE1')]


#Merge articles that meet the conditions into the m_author variable through the PMID
m_authors = authors.merge(f_articles[['PMID']], on='PMID')

#Count the total number of papers for each author in the m_author variable
paper_counts = m_authors['AuthorFullname'].value_counts()

#Count author's Time_Span
f_articles['Year'] = pd.to_datetime(f_articles['Year'], format='%Y')
author_y = m_authors.merge(f_articles[['PMID', 'Year']], on='PMID')
time_span = author_y.groupby('AuthorFullname')['Year'].agg([min, max])
time_span['TimeSpan'] = (time_span['max'] - time_span['min']).dt.days / 365

#Merge data contains paper counts and timespan as active author
active_author = pd.DataFrame(paper_counts).merge(time_span, left_index=True, right_index=True, how='left')
active_author.rename(columns={'AuthorFullname': 'PaperCount'}, inplace=True)

#Sort the top ten authors who meet the conditions
t_authors = active_author.sort_values(by=['PaperCount', 'TimeSpan'], ascending=False).head(10)

#Create two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

#Draw the first subgraph, containing the number of papers
sns.barplot(x=t_authors['PaperCount'], y=t_authors.index, color='blue', ax=ax1)
ax1.set_ylabel('Authors')  
ax1.set_xlabel('Paper Count')
ax1.set_title('Paper Count by Author')

#Draw the Second subgraph, containing the number of papers
sns.barplot(x=t_authors['TimeSpan'], y=t_authors.index, color='darkred', ax=ax2)
ax2.set_ylabel('') 
ax2.set_xlabel('Time Span (years)')
ax2.set_title('Time Span by Author')

#Hide the y-axis label of the second subgraph to facilitate a clearer view of the visual chart
ax2.tick_params(labelleft=False)
plt.tight_layout()
plt.show()

