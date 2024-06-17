#!/usr/bin/env python

import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description="Process segment/node coverage and lengths, create matrix, and output matrix tsv files.")
    parser.add_argument("-c","--coverage", help="Coverage file in tsv")
    parser.add_argument("-n","--node_length", help="Parsed segment/node information in tsv")
    parser.add_argument("-a","--asms", nargs="+", help = "List of assemblies")
    parser.add_argument("-p","--prefix", help="Output Prefix for tsv files")
    return parser.parse_args()

def main():
    args = parse_args()
    coverage = args.coverage
    node_length= args.node_length
    assemblies = args.asms
    prefix = args.prefix

    # Read the coverage data
    data = pd.read_csv(coverage, sep=" ", header=0)
    data_cols = ["nodeid", "nodelen", "chromo", "pos", "rrank"] + list(assemblies)
    data.columns = data_cols


    # Create the data matrix. If cell has value, assign 1. Otherwise, set 0 for absence.
    datmat = data[assemblies].copy()
    datmat[datmat < 0] = 0
    datmat[datmat > 0] = 1

    # Read the graph length data
    datlen = pd.read_csv(node_length, sep="\t", header=None)
    datlen.columns = ["nodeid", "conlen", "chromo", "pos", "rrank"]

    # Create the ID match dataframe
    datid = pd.DataFrame({"rankid": range(len(assemblies)), "accessions": assemblies})

    # Update the data matrix with predefined ranks or assemblies
    for i, row in datlen.iterrows():
        ranks = row["rrank"]
        asid = datid[datid["rankid"] == ranks]["accessions"].values
        if len(asid) > 0:
            datmat.loc[i, asid] = 1

    # Extract present assemblies from each node
    colnode = []
    for i, row in datmat.iterrows():
        labcol = ",".join(datmat.columns[row == 1]) # boolean ; if 1, name is appended for that node
        colnode.append(labcol)

    # Output the node assemblies file
    datout = pd.DataFrame({"nodeid": data["nodeid"], "colnode": colnode})
    datout.to_csv(f"{prefix}_nodecol.tsv", sep="\t", index=False, header=True, quoting=False)

    # Output the node matrix file
    datmat["nodeid"] = data["nodeid"]
    datmat = datmat[["nodeid"] + assemblies]
    datmat.to_csv(f"{prefix}_nodemat.tsv", sep="\t", index=False, header=True, quoting=False)

if __name__ == "__main__":
    main()
