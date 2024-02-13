import wikipedia
import networkx as nx
import matplotlib.pyplot as plt


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
    article_titles = ['october 7 2023']  # Add more article titles as needed
    for title in article_titles:
        search_results = wikipedia.search(title)

        for article in search_results:
            try:
                summary = wikipedia.summary(article, sentences=1)
                G.add_node(article, summary=summary)
                print(f'Added {article} to the graph')
            except wikipedia.exceptions.PageError:
                print(f'Article "{article}" does not exist.')

    add_edges(G, article_titles)

    print("Number of nodes:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges())

    # Compute the largest connected component
    largest_cc = max(nx.connected_components(G), key=len)
    G_lcc = G.subgraph(largest_cc)

    # Calculate network metrics for the largest connected component
    if len(G_lcc) > 0:
        diameter = nx.diameter(G_lcc)
        clustering_coefficient = nx.average_clustering(G_lcc)
        print("Diameter of the largest connected component:", diameter)
        print("Average clustering coefficient of the largest connected component:", clustering_coefficient)
    else:
        print("The graph does not contain any connected components.")

    # Plot the graph
    plt.figure(figsize=(10, 6))
    nx.draw(G_lcc, with_labels=True, font_weight='bold')
    plt.show()


if __name__ == '__main__':
    main()
