from itertools import islice
import pandas as pd
import csv
import networkx as nx
import matplotlib.pyplot as plt

#-----------(xls-csv) conversion-----------#

#------ Load the XLS file into a pandas dataframe-------#
df = pd.read_excel('retweets.xlsx')

# Save the dataframe to a CSV file
df.to_csv('retweets_columnForm.csv', index=False)

#--------interchange of colums and rows-----------------#

# Load the CSV file into a pandas dataframe
df = pd.read_csv('retweets_columnForm.csv')

# Transpose the dataframe (i.e., swap rows and columns)
df = df.transpose()

# Save the transposed dataframe to a new CSV file
df.to_csv('retweets_rowForm.csv', header=False)


#------------counting number of headers-----------#
headings=[]
with open('retweets_rowForm.csv', 'r') as file:

    # Create a reader object
    reader = csv.reader(file)

    # Count the number of header rows
    num_headers = 0
    for row in reader:
        if any(row):
            headings.append(row)
            num_headers += 1
        else:
            break
#-------------------------------#
# Print the number of headers
# print(headings)


# Print the column data
column_data=[]
row_data=[]

#----storing each row of data--------#
with open('retweets_columnForm.csv', 'r') as file:
    reader= csv.reader(file)
    data = list(reader)

    row_data=data[0]


    # for name in data:
    #     print(name)
    file.close()
        # row_data=[]


G = nx.DiGraph()
pos = nx.spring_layout(G)  # positions for all nodes

# ---------Add nodes to the graph for each header------
node_labels = []
for name in row_data:
    if G.has_node(name):
        continue
    else:
        G.add_node(name,name=name)
    # node_labels.append(name)

# nx.draw_networkx_nodes(G, pos, node_labels,node_color="red")
# Print the nodes in the graph

#--------------------------#
# print(G.nodes())
# print(node_labels)

#------iterating over the number of original users---#
j=0
for name in row_data:
    #---getting the name of the user---#
    originalUser_name= name

    #getting the retweet data of the particular user#
    with open('retweets_rowForm.csv', 'r') as file:
        reader = csv.reader(file)
        column_datas = list(reader)
        # print(column_datas[j])

        #--iterating through each retweet of a specific user---#
        for retweet_name in column_datas[j]:
            # print(retweet_name)
            if retweet_name == originalUser_name:
                continue
            #if the name is null then we come out of the loop
            elif not retweet_name:
                break
            else:
                #-----checking if the graph has the particular node
                if G.has_node(retweet_name):
                    #if the graph has the node then we add an edge between them
                    G.add_edge(originalUser_name, retweet_name)
                else:
                    #if the present graph doesnot has the node then we create the node
                    G.add_node(retweet_name, name=retweet_name, color="red")
                    #adding edge between the nodes
                    G.add_edge(originalUser_name, retweet_name)

    j+=1

#     label = G.nodes[node]['name']
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, font_size=5)
plt.tight_layout()
plt.show()
# print(nx.is_connected(G))


#-------Getting all the nodes in the graph--#
node_list=[]
for node in G.nodes():
    node_list.append(node)


#--------centrality-----------#

degree_centrality = nx.degree_centrality(G)
in_degree=nx.in_degree_centrality(G)
out_degree = nx.out_degree_centrality(G)
between_centrality=nx.betweenness_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
katz=nx.katz_centrality(G)
eigen_centrality = nx.eigenvector_centrality_numpy(G)
page_rank = nx.pagerank(G)


#-------calculating average of centralities-------#
average={}
for key, deg, betw, katzv in zip(degree_centrality, degree_centrality.values(), between_centrality.values(), katz.values()):
    avg = (deg+betw+katzv)/3
    average[key]=avg


##-----------calculating spread of the graph----------#

# Calculate the spread of the graph
spread = {}
for node in G.nodes():
    spread[node] = nx.single_source_shortest_path_length(G, node)
# print(spread)

# Aggregate the results
total_spread = {}
for node in G.nodes():
    for target, distance in spread[node].items():
        if target not in total_spread:
            total_spread[target] = distance
        else:
            total_spread[target] += distance

# print(total_spread)
# Calculate the average spread
num_pairs = len(total_spread)
total_distance = sum(total_spread.values())
average_spread = total_distance / num_pairs
# print(average_spread)


# Compute ratio of out-degree centrality to average shortest path length
average_spread_outdeg={}
for node in G.nodes():
    if out_degree[node] == 0:
        average_spread_outdeg[node]=0
    else:
        average_spread_outdeg[node] =  total_spread[node] / out_degree[node]

#
# ##-------sorting centralities to find influential people-------#
#
# # Sort the degree centrality data temporarily in descending order
# sorted_deg_cent = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
# sorted_btw_cent = sorted(between_centrality.items(), key=lambda x: x[1], reverse=True)
# sorted_cls_cent = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)
# sorted_eig_cent = sorted(eigen_centrality.items(), key=lambda x: x[1], reverse=True)


#----creating a file to store the centrality data----#
data = [(k, degree_centrality[k], in_degree[k],out_degree[k],between_centrality[k], katz[k], eigen_centrality[k], average[k], total_spread[k]) for k in degree_centrality]
with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Nodes','Degree_centrality', 'In_Degree', 'Out_Degree','Betweenness','KaztCentrality','Eigen_Centrality', 'Average_Centrality', 'Spread'])
    writer.writerows(data)

# plt.show()

##-------sorting centralities to find influential people-------#

# Sort the degree centrality data temporarily in descending order
sorted_deg_cent = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
sorted_btw_cent = sorted(between_centrality.items(), key=lambda x: x[1], reverse=True)
sorted_cls_cent = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)
sorted_eig_cent = sorted(eigen_centrality.items(), key=lambda x: x[1], reverse=True)
sorted_page_rank = sorted(page_rank.items(), key=lambda x: x[1], reverse=True)
sorted_avg_cent = sorted(average.items(), key=lambda x: x[1], reverse=True)
sorted_spread = sorted(average_spread_outdeg.items(), key=lambda x: x[1], reverse=True)
sorted_katz = sorted(katz.items(), key=lambda x: x[1], reverse=True)
sorted_out_degree = sorted(out_degree.items(), key=lambda x: x[1], reverse=True)


#------top 5 influencers in various category-----#

deg_influencers={}
out_deg_influencers={}
betw_influencers={}
close_influencers={}
katz_influencers={}
page_rank_influencers={}
average_influencers={}
average_spread_influencers={}

deg_influencers.update(dict(islice(sorted_deg_cent, 5)))
out_deg_influencers.update(dict(islice(sorted_out_degree, 5)))
betw_influencers.update(dict(islice(sorted_btw_cent, 5)))
close_influencers.update(dict(islice(sorted_cls_cent, 5)))
katz_influencers.update(dict(islice(sorted_katz, 5)))
page_rank_influencers.update(dict(islice(sorted_page_rank, 5)))
average_influencers.update(dict(islice(sorted_avg_cent, 5)))
average_spread_influencers.update(dict(islice(sorted_spread, 5)))


# print(deg_influencers)
# print(betw_inflencers)
# print(close_inflencers)
# print(eigen_inflencers)


##--------creating figures----------#

font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 3,
        }

# plot the network graph
plt.subplot(3, 3, 1)
# pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, font_size=0.2)

# plot the first bar graph
plt.subplot(3, 3, 2)
plt.bar(deg_influencers.keys(), deg_influencers.values())
plt.title('Degree Centrality')
# plt.xlabel("People")
plt.xticks(fontsize=6)
plt.xticks(rotation=45)
# plt.xticks(list(range(len(deg_influencers.values()))), [label.replace(' ', '\n') for label in deg_influencers.values()])


# plot the second bar graph
plt.subplot(3, 3, 3)
plt.bar(betw_influencers.keys(), betw_influencers.values())
plt.title('Betweenness Centrality')
plt.xticks(fontsize=6)
plt.xticks(rotation=45)

# plot the third bar graph
plt.subplot(3, 3, 4)
plt.bar(close_influencers.keys(), close_influencers.values())
plt.title('Closeness Centrality')
plt.xticks(fontsize=6)
plt.xticks(rotation=45)

# plot the fourth bar graph
plt.subplot(3, 3, 5)
plt.bar(page_rank_influencers.keys(), page_rank_influencers.values())
plt.title('PageRank Centrality')
plt.xticks(fontsize=6)
plt.xticks(rotation=45)

# plot the fifth bar graph
plt.subplot(3, 3, 6)
plt.bar(average_influencers.keys(), average_influencers.values())
plt.title('All rounder on avg centrality')
plt.xticks(fontsize=6)
plt.xticks(rotation=45)

# plot the sixth bar graph
plt.subplot(3, 3, 7)
plt.bar(katz_influencers.keys(), katz_influencers.values())
plt.title('Katz Centrality')
plt.xticks(fontsize=6)
plt.xticks(rotation=45)

# plot the seventh bar graph
plt.subplot(3, 3, 8)
plt.bar(out_deg_influencers.keys(), out_deg_influencers.values())
plt.title('Out degree')
plt.xticks(fontsize=6)
plt.xticks(rotation=45)

# plot the eighth bar graph
plt.subplot(3, 3, 9)
plt.bar(average_spread_influencers.keys(), average_spread_influencers.values())
plt.title('Average spread')
plt.xticks(fontsize=6)
plt.xticks(rotation=45)

# adjust the layout and display the plot
plt.tight_layout()


# Display the figure
plt.show()