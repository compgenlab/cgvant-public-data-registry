#!/usr/bin/env python3

import sys

headers = None

cur_chrom = None
vals = []

for fname in sys.argv[1:]:
    file_header = None
    sys.stderr.write('%s\n' % fname)
    with open(fname, 'rt') as f:
        for line in f:
            cols = line.strip('\n').split(',')
            # remove hg19 coordinate
            del cols[1]
            if not headers:
                headers = cols
                sys.stdout.write('%s\n' % '\t'.join(cols))
            if not file_header:
                file_header = cols
                continue

            
            if cur_chrom != cols[0]:
                if vals:
                    for pos, cols1 in sorted(vals):
                        # convert to ucsc chr naming
                        cols1[0] = 'chr%s' % cols1[0]     
                        sys.stdout.write('%s\n' % '\t'.join(cols1))
                vals = []
                cur_chrom = cols[0]
                sys.stderr.write('>%s\n' % cur_chrom)

            if cols[1] != '.':
                vals.append((int(cols[1]), cols))
                # remove vars w/o hg38 coordinates

if vals:
    for pos, cols1 in sorted(vals):
        # convert to ucsc chr naming
        cols1[0] = 'chr%s' % cols1[0]     
        sys.stdout.write('%s\n' % '\t'.join(cols1))

