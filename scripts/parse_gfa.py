import argparse
import os

def parse_gfa(graph, prefix):
    # Extract node information
    with open(graph, 'r') as graph_file:
        with open(f"{prefix}_len.tsv", 'w') as len_file:
            for line in graph_file:
                if line.startswith('S'):
                    components = line.split('\t')
                    chr_info = components[4].split(':')
                    pos_info = components[5].split(':')
                    arr_info = components[6].split(':')
                    len_file.write(f"{components[1]}\t{len(components[2])}\t{chr_info[2]}\t{pos_info[2]}\t{arr_info[2]}")
    
    # Extract edge information
    with open(graph, 'r') as graph_file:
        with open(f"{prefix}_link.tsv", 'w') as link_file:
            for line in graph_file:
                if line.startswith('L'):
                    link_file.write(line)

def main():
    parser = argparse.ArgumentParser(description="Parse node and edge information from a GFA file.")
    parser.add_argument("graph", help="Path to the GFA file")
    parser.add_argument("prefix", help="Prefix for output files")
    args = parser.parse_args()

    if not os.path.isfile(args.graph):
        print("Error: The specified graph file does not exist.")
        return
    parse_gfa(args.graph, args.prefix)

if __name__ == "__main__":
    main()