import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description='Calculate core, dispensable, and private genome segments.')
    parser.add_argument('-m', '--matrix', help='Path to the node matrix file', required=True)
    parser.add_argument('-l', '--graph_w_length', help='Path to the graph length file', required=True)
    parser.add_argument('-p', '--prefix', help='Prefix for the output file', required=True)
    return parser.parse_args()

def calculate_core(matrix, graph_w_length, prefix):
    mat = pd.read_csv(matrix, sep="\t", header=0)
    # add the number of accessions in each node
    #mat['accession'] = mat.iloc[:, 2:].sum(axis=1)
    accession_columns = mat.columns[1:]  # Adjust based on actual column names, excluding 'segid'
    mat['accession'] = mat[accession_columns].sum(axis=1)
    # total number of assembly in the graph
    total = mat.shape[1] - 2
    # add the nodelen
    data_len = pd.read_csv(graph_w_length, sep="\t", header=None)
    data_len.columns = ['nodeid', 'seglen', 'chromo', 'pos', 'rrank']
    # join to get the node len in the matrix
    mat = mat.merge(data_len, on='nodeid', how='left')
    # calculate core genome length
    core = mat.loc[mat['accession'] == total, 'seglen'].sum()
    dispensable= mat.loc[(mat['accession'] < total) & (mat['accession'] > 1), 'seglen'].sum()
    private = mat.loc[mat['accession'] == 1, 'seglen'].sum()
    # add core and flexible node count
    node_core = len(mat.loc[mat['accession'] == total, 'seglen'])
    node_dispensable = len(mat.loc[(mat['accession'] < total) & (mat['accession'] > 1), 'seglen'])
    node_private = len(mat.loc[mat['accession'] == 1, 'seglen'])
    outfile = f"{prefix}_categorize.tsv"
    with open(outfile, 'w') as f:
        f.write("core\tdispensable\tprivate\n")
        f.write(f"{core}\t{dispensable}\t{private}\n")
        f.write(f"{node_core}\t{node_dispensable}\t{node_private}\n")

def main():
    args = parse_args()
    calculate_core(args.matrix, args.graph_w_length, args.prefix)

if __name__ == '__main__':
    main()


