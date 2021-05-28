### tb_variant_filter

![tb variant filter build status](https://github.com/COMBAT-TB/tb_variant_filter/actions/workflows/tb_variant_filter.yml/badge.svg)

This tool offers multiple options for filtering variants (in VCF files, relative to M. tuberculosis H37Rv coordinates).

It currently has 5 main modes:

1. Filter by region. Mask out variants in certain regions. Region lists available as:
    1. `farhat_rlc`: Refined Low Confidence regions from [Marin et al](https://www.biorxiv.org/content/10.1101/2021.04.08.438862v1.full)
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
workflow we ([SANBI](https://www.sanbi.ac.za)) currently use.
 
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

To export a region (from the list of possible region masks) in BED format, use the `tb_region_list_to_bed` command:


```
usage: tb_region_list_to_bed [-h] [--chromosome_name CHROMOSOME_NAME]
                             {farhat_rlc, mtbseq,pe_ppe,tbprofiler,uvp} [output_file]

Output region filter in BED format

positional arguments:
  {mtbseq,pe_ppe,tbprofiler,uvp}
                        Name of region list
  output_file           File to write output to

optional arguments:
  -h, --help            show this help message and exit
  --chromosome_name CHROMOSOME_NAME
                        Chromosome name to use in BED
```

### Testing and development environment

The repository contains a file, [test_environment.yml](test_environment.yml), for creating a [conda](https://docs.conda.io/en/latest/#)
environment for testing and development. Tests can be run with `pytest` and `tox`, where `tox` also uses conda
to create the testing environment.

For some tests, locus locations are looked up using the [COMBAT-TB NeoDB](https://combattb.org/combat-tb-neodb/). This requires an
environment variable, `COMBATTB_BOLT_URL`. If this is not set, tests requiring this lookup are skipped. The default in `tox.ini` uses the [SANBI](https://www.sanbi.ac.za/) hosted NeoDB instance.

### Licensing and distribution

This code free software and is licensed under the terms specified in [COPYING](COPYING), i.e under the terms of the
[GNU General Public License version 3](https://www.gnu.org/licenses/gpl-3.0-standalone.html).
