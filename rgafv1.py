import argparse
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description="Run different scripts based on the mode.")
    subparsers = parser.add_subparsers(dest="mode", help="Mode of operation")
    
    # Subparser for gfa mode
    parser_gfa = subparsers.add_parser("gfa", help="Mode for processing GFA files")
    parser_gfa.add_argument("-g", "--graph", help="Graph path", required=True)
    parser_gfa.add_argument("-p", "--prefix", help="Prefix for output files in gfa mode", default="graph")

    # Subparser for gaf mode
    parser_gaf = subparsers.add_parser("gaf", help="Mode for processing GAF files")
    parser_gaf.add_argument("-g", "--graph", help="Graph prefix", required=True)
    parser_gaf.add_argument("-a", "--assembly", help="Assembly prefixes", nargs="+", required=True)

    # Subparser for mtx mode
    parser_mtx = subparsers.add_parser("mtx", help="Mode for processing matrix files")
    parser_mtx.add_argument("-c", "--coverage", help="Coverage file in tsv", required=True)
    parser_mtx.add_argument("-n", "--node_length", help="Parsed segment/node information in tsv", required=True)
    parser_mtx.add_argument("-a", "--asms", help="List of assemblies", nargs="+", required=True)
    parser_mtx.add_argument("-p", "--prefix", help="Output prefix for tsv files", required=True)

    args = parser.parse_args()

    if args.mode == "gfa":
        if not os.path.isfile(args.graph):
            print("Error: The specified graph file does not exist.")
            return
        # Run parse_gfa.py with the specified arguments
        subprocess.run(["python", "scripts/parse_gfa.py", args.graph, args.prefix])
    elif args.mode == "gaf":
        if not args.graph or not args.assembly:
            print("Error: Missing arguments for mode 'gaf'.")
            return
        # Run x_coverage.py with the specified arguments
        subprocess.run(["python", "scripts/x_coverage.py", "-g", args.graph, "-a"] + args.assembly)
    elif args.mode == "mtx":
        if not os.path.isfile(args.coverage):
            print("Error: The specified coverage file does not exist.")
            return
        if not os.path.isfile(args.node_length):
            print("Error: The specified node length file does not exist.")
            return
        if not args.asms:
            print("Error: Missing assembly arguments for mode 'mtx'.")
            return
        if not args.prefix:
            print("Error: Missing prefix for mode 'mtx'.")
            return
        # Run matrix.py with the specified arguments
        subprocess.run(["python", "scripts/matrix.py", "-c", args.coverage, "-n", args.node_length, "-a"] + args.asms + ["-p", args.prefix])
    else:
        print("Unsupported mode. Please use 'gfa', 'gaf', or 'mtx' mode.")

if __name__ == "__main__":
    main()
