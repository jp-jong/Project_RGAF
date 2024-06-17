import argparse
import pandas as pd
import os
from typing import Tuple, List

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse coverage of each assemblies to graph and combine. GAF files are expected to contain the dc tag from --cov of minigraph.")
    parser.add_argument("-g", "--graph", help="Graph prefix")
    parser.add_argument("-a", "--assembly", help="Assembly prefixes", nargs="+")
    return parser.parse_args()

def parse_node_coverage(line: str) -> Tuple[str, int, str, str, str, str]:
    components = line.strip().split()
    nodeid = components[1]
    nodelen = len(components[2])
    start_chromo = components[4].split(":")[2]
    start_pos = components[5].split(":")[2]
    rrank = components[-2].split(":")[2]
    coverage = components[-1].split(":")[2]
    if not coverage:
        print("GAF format does not contain dc tag. Please use --cov when running minigraph. Exiting...")
        exit()
    return nodeid, nodelen, start_chromo, start_pos, rrank, coverage

def parse_edge_coverage(line: str) -> Tuple[str, str, int]:
    components = line.strip().split()
    parent, child = (components[3], components[1]) if components[2] == "-" or components[4] == "-" else (components[1], components[3])
    coverage = 1 if int(components[-1].split(":")[2]) > 0 else 0
    return parent, child, coverage

# Here it is assumed that the name of the gaf file follows this name for tracking which assembly was mapped to which graph. 
# assemb_graph.gaf example, if nh232 is assembly mapped to the pangenome graph asm5, then, nh232_asm5.gaf
# it also assumes that the files being processed are within the same directory from which these files are being read
def process_node_coverage(graph: str, assembly: List[str]) -> pd.DataFrame:
    combined_coverage = None

    for idx, asm in enumerate(assembly):
        with open(f"{asm}_{graph}.gaf") as infile:
            if idx == 0:
                combined_coverage = pd.DataFrame(
                    [parse_node_coverage(line) for line in infile if line.startswith("S")],
                    columns=["nodeid", "nodelen", "start_chromo", "start_pos", "rrank", asm]
                )
            else:
                additional_coverage = pd.DataFrame(
                    [[parse_node_coverage(line)[0], parse_node_coverage(line)[-1]] for line in infile if line.startswith("S")],
                    columns=["nodeid", asm]
                )
                combined_coverage = pd.merge(combined_coverage, additional_coverage, on=["nodeid"], how="outer")

    return combined_coverage

def process_edge_coverage(graph: str, assembly: List[str]) -> pd.DataFrame:
    combined_edge = None

    for idx, asm in enumerate(assembly):
        with open(f"{asm}_{graph}.gaf") as infile:
            if idx == 0:
                combined_edge = pd.DataFrame(
                    [parse_edge_coverage(line) for line in infile if line.startswith("L")],
                    columns=["parent_node", "child_node", asm]
                )
            else:
                additional_edge = pd.DataFrame(
                    [parse_edge_coverage(line) for line in infile if line.startswith("L")],
                    columns=["parent_node", "child_node", asm]
                )
                combined_edge = pd.merge(combined_edge, additional_edge, on=["parent_node", "child_node"], how="outer")

    return combined_edge

def main():
    args = parse_args()
    graph = args.graph
    assembly = args.assembly

    # Create directory if it doesn't exist
    directory = "coverage_use"
    if not os.path.exists(directory):
        os.makedirs(directory)

    node_coverage = process_node_coverage(graph, assembly)
    node_coverage.fillna(0, inplace=True)
    node_coverage.to_csv(f"{directory}/{graph}_coverage.tsv", sep=" ", index=False)

    edge_coverage = process_edge_coverage(graph, assembly)
    edge_coverage.to_csv(f"{directory}/{graph}_edge_use.tsv", sep=" ", index=False)

if __name__ == "__main__":
    main()
