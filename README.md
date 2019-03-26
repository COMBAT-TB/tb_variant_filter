### tb_variant_filter

[![CircleCI](https://circleci.com/gh/COMBAT-TB/tb_variant_filter.svg?style=svg)](https://circleci.com/gh/COMBAT-TB/tb_variant_filter)

This tool offers multiple options for filtering variants (in
VCF files, relative to M. tuberculosis H37Rv).

It currently has 3 main modes:

1. Filter by region. Mask out variants in certain regions. Region lists available as:
    1. `pe_ppe`: PE/PPE genes from [Fishbein et al 2015](https://onlinelibrary.wiley.com/doi/full/10.1111/mmi.12981)
    2. `tbprofiler`: [TBProfiler](http://tbdr.lshtm.ac.uk/) list of antibiotic resistant genes
    3. `mtbseq`: [MTBseq](https://github.com/ngs-fzb/MTBseq_source) list of antibiotic resistant genes
    4. `uvp`: [UVP](https://github.com/CPTR-ReSeqTB/UVP) list of repetitive loci in M. tuberculosis genome
2. Filter by proximity to indels. Masks out variants within a certain distance (by default 5 bases) of an insertion or
 deletion site.
3. Filter by percentage of alternate allele bases. Mask out variants with less than a minimum percentage 
(by default 90%) alternative alleles.
4. Filter by depth of reads at a variant site. Masks out variants with less than a minimum depth of coverage 
(default 30) at the site
5. Filter all non-SNV variants. Masks out variants that are not single nucleotide variants.

Filtering by (SAM/BAM) mapping quality was omitted because these filters are performed by the upstream 
workflow we (SANBI) currently use.
 
When used together the effects of the filters are added (i.e. a variant is masked out if it is masked by any of the filters).

#### Installation

The software is available via [bioconda](https://bioconda.github.io/) and can be installed with:

```
conda install tb_variant_filter
```

#### Usage
```
usage: tb_variant_filter [-h] [--region_filter REGION_FILTER]
                         [--close_to_indel_filter]
                         [--indel_window_size INDEL_WINDOW_SIZE]
                         [--min_percentage_alt_filter]
                         [--min_percentage_alt MIN_PERCENTAGE_ALT]
                         [--min_depth_filter] [--min_depth MIN_DEPTH]
                         [--snv_only_filter]
                         input_file [output_file]

Filter variants from a VCF file (relative to M. tuberculosis H37Rv)

positional arguments:
  input_file            VCF input file (relative to H37Rv)
  output_file           Output file (VCF format)

optional arguments:
  -h, --help            show this help message and exit
  --region_filter REGION_FILTER, -R REGION_FILTER
  --close_to_indel_filter, -I
                        Mask out single nucleotide variants that are too close
                        to indels
  --indel_window_size INDEL_WINDOW_SIZE
                        Window around indel to mask out (mask this number of
                        bases upstream/downstream from the indel. Requires -I
                        option to selected)
  --min_percentage_alt_filter, -P
                        Mask out variants with less than a given percentage
                        variant allele at this site
  --min_percentage_alt MIN_PERCENTAGE_ALT
                        Variants with less than this percentage variants at a
                        site will be masked out
  --min_depth_filter, -D
                        Mask out variants with less than a given depth of
                        reads
  --min_depth MIN_DEPTH
                        Variants at sites with less than this depth of reads
                        will be masked out
  --snv_only_filter     Mask out variants that are not SNVs
```