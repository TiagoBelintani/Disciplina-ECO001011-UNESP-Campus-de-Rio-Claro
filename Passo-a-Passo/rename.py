#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment


def rename_id(old_id):
    # remove aspas do NEXUS
    old_id = old_id.replace("'", "").replace('"', "")

    # mantém só o nome do táxon (últimos dois campos)
    parts = old_id.split("_")
    if len(parts) >= 2:
        return "_".join(parts[-2:])
    else:
        return old_id


def main():
    parser = argparse.ArgumentParser(
        description="Rename taxa in NEXUS alignments"
    )
    parser.add_argument("--alignments", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--input-format", default="nexus")
    parser.add_argument("--output-format", default="nexus")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    for fname in os.listdir(args.alignments):
        if not fname.endswith(".nex") and not fname.endswith(".nexus"):
            continue

        infile = os.path.join(args.alignments, fname)
        outfile = os.path.join(args.output, fname)

        new_align = MultipleSeqAlignment([])

        for aln in AlignIO.parse(infile, args.input_format):
            for seq in aln:
                new_id = rename_id(seq.id)
                seq.id = new_id
                seq.name = ""
                seq.description = ""
                seq.annotations = {"molecule_type": "DNA"}
                new_align.append(seq)

        AlignIO.write(new_align, outfile, args.output_format)
        print(f"Renamed: {fname}")


if __name__ == "__main__":
    main()
