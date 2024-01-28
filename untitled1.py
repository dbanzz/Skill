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



import matplotlib.pyplot as plt
from datetime import datetime

# Group the data by year and count the number of articles per year
articles_per_year = articles.groupby('Year').size()

articles_per_year.index = articles_per_year.index.year
# Remove the data for the year 2024
articles_per_year_without_2024 = articles_per_year[articles_per_year.index != 2024]


#Plotting the line graph using the data without 2024
plt.figure(figsize=(10, 6))
plt.plot(articles_per_year_without_2024.index, articles_per_year_without_2024.values, marker='o')
plt.title('Number of Articles per Year (Excluding 2024)')
plt.xlabel('Year')
plt.ylabel('Number of Articles')
plt.grid(True)
plt.xticks(articles_per_year_without_2024.index, rotation=45)
plt.show()



import networkx as nx
# Reread the CSV file to prevent the DataFrame from being incorrectly modified in previous operations
articles_df = pd.read_csv('D:/Skill Assessment2/articles.BACE1.csv')
authors_df = pd.read_csv('D:/Skill Assessment2/authors.BACE1.csv')
paper_counts_df = pd.read_csv('D:/Skill Assessment2/paper_counts.csv')

# Generate full author name
authors_df['AuthorFullname'] = authors_df['AuthorForename'] + ' ' + authors_df['AuthorLastname']

# Convert the Year column to a datetime object and calculate the time span
articles['Year'] = pd.to_datetime(articles['Year'], format='%Y')
author_y = authors_df.merge(articles[['PMID', 'Year']], on='PMID')
time_span = author_y.groupby('AuthorFullname')['Year'].agg([min, max])
time_span['TimeSpan'] = (time_span['max'] - time_span['min']).dt.days / 365

# Find the top 10 active authors based on the number of papers and active time
active_author = pd.DataFrame(authors_df['AuthorFullname'].value_counts()).merge(
    time_span, left_index=True, right_index=True, how='left')
active_author.rename(columns={'AuthorFullname': 'PaperCount'}, inplace=True)
top_authors = active_author.sort_values(by=['PaperCount', 'TimeSpan'], ascending=False).head(10)

# Get a list of author IDs for all articles
all_authors_per_paper = authors_df.groupby('PMID')['AuthorFullname'].apply(list).reset_index()

# Only papers with the top 10 active authors will be considered
top_author_papers = authors_df[authors_df['AuthorFullname'].isin(top_authors.index)]

# Find the names of all authors for each paper
collaborations = top_author_papers.merge(all_authors_per_paper, on='PMID')

# Create network diagram
G = nx.Graph()

# Add nodes and edges
for paper_id, group in collaborations.groupby('PMID'):
    authors = group['AuthorFullname_y'].iloc[0]  # Get a list of co-authors
    for i in range(len(authors)):
        if authors[i] in top_authors.index:  # Only the top 10 active authors will be considered
            for j in range(i + 1, len(authors)):
                # If the author is among the top 10 active authors, add to the graph
                if authors[j] in top_authors.index:
                    G.add_edge(authors[i], authors[j])

# Draw a collaboration network diagram
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, seed=42)

# Draw graphics
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=12, edge_color='gray')
plt.title('Co-authorship Network Graph', fontsize=15)
plt.show()

