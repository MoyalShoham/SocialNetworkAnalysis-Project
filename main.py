import wikipedia
import networkx as nx
import matplotlib.pyplot as plt
import mplcursors

def fetch_links(article_title):
    try:
        links = wikipedia.page(article_title).links
        return links
    except wikipedia.exceptions.PageError:
        print(f'Article "{article_title}" does not exist.')
        return []

def add_edges(G, article_titles):
    for title in article_titles:
        links = fetch_links(title)
        for link in links:
            if link in G.nodes:
                G.add_edge(title, link)

def main():
    G = nx.Graph()
    article_titles = [
        'october 7 Israel',
        'Gaza before and after October 7',
        'Israel War Against Hamas',
        'Hamas Against Jew',
        'Hamas genocide October 7',
        'Iron Swords War 2023',
        'Cries of El-aqsa in October 7',
        "'Simhat Torah' in Israel, October 7",
        'Hamas before and after October 7',
        'Israel defense forces in October 7',
        'United Nations in October 7',
        'Nova Festival in Israel, October 7',
        'Hostage in October 7',
        'Hostages is gaza', 
        'Civilian of gaza in October 7',
        
    ]  
    for title in article_titles:
        search_results = wikipedia.search(title)

        for article in search_results:
            try:
                summary = wikipedia.summary(article, sentences=1)
                G.add_node(article, summary=summary)
                print(f'Added {article} to the graph')
            except wikipedia.exceptions.PageError:
                print(f'Article "{article}" does not exist.')

    
    print
    
    add_edges(G, article_titles)

    print('Graph created successfully.')
    print("Number of nodes:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges())

    largest_cc = max(nx.connected_components(G), key=len)
    print("Number of connected components:", nx.number_connected_components(G))
    G_lcc = G.subgraph(largest_cc)

    if len(G_lcc) > 0:
        diameter = nx.diameter(G_lcc)
        clustering_coefficient = nx.average_clustering(G_lcc)
        print("Diameter of the largest connected component:", diameter)
        print("Average clustering coefficient of the largest connected component:", clustering_coefficient)
    else:
        print("The graph does not contain any connected components.")

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G_lcc)  # Layout for the graph
    nx.draw(G_lcc, pos, with_labels=True, font_weight='bold', node_size=500, node_color='lightblue', font_size=8, edge_color='gray', width=0.5, alpha=0.7)  # Draw the graph
    edge_labels = nx.get_edge_attributes(G_lcc, 'weight')  # Extract edge labels

    # Use mplcursors to display edge labels on hover
    mplcursors.cursor(multiple=True).connect(
        "add", lambda sel: sel.annotation.set_text(edge_labels.get((sel.artist.get_data()[0], sel.artist.get_data()[1]), '')))

    plt.show()

    # Visualize degree distribution
    plt.figure(figsize=(8, 6))
    plt.hist(degrees, bins=len(degree_counts), edgecolor='black')
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.title("Degree Distribution of the Graph")
    plt.show()

if __name__ == '__main__':
    main()
