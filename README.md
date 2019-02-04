# Navigome
Scripts for visualizations used in Navigome (navigome.com). Most visualizations in Navigome are powered by [vega-lite](https://vega.github.io/vega-lite/) and [altair](https://altair-viz.github.io/).

## Usage
The update_all.py python script in the scripts directory calls all visualization scripts used in Navigome. It takes as argument the Navigome directory, which should contain (1) an "input" directory, that would be regularly updated (minimal structure provided in the GitHub directory) (2) an empty "output" directory (3) the "scripts" directory (provided in the GitHub directory as well):
```
python update_all.py {navigome_directory}
```

The input directory on GitHub contains a minimal structure to create visualizations for a new phenotype (e.g. phenotype code SCHI01) and update all gene profile visualizations. At the moment, the directory only contains scripts to generate visualizations, not input files.

## Requirements
- altair>=2.2.2
- scikit-learn>=0.20.0
- numpy>=1.15.4
- pandas>=0.23.4
- umap-learn>=0.3.7
- ugtm>=2.0.0
- bs4>=0.0.1

