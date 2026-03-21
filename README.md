# ReadsClassification Nextflow Pipeline

A reproducible Nextflow DSL2 pipeline for classifying long-read DNA methylation data into tissue and cell-type fractions using pre-trained methylation models.

This pipeline is designed for HPC environments and runs out-of-the-box using a pre-built Singularity (Apptainer) image — no Docker, no Conda setup required for end users.

⸻

## 🚀 Key Features
- End-to-end long-read methylation classification workflow
- Chunked BAM processing for massive scalability
- Dynamic resource allocation and automatic Out-Of-Memory (OOM) recovery
- Works on Slurm, PBS, or local execution
- Fully containerized with Singularity
- Generates interactive Plotly Sunburst diagrams for compositional fractions
- Minimal user inputs (just a CSV)

⸻

## 📂 Repository Structure

```text
readsClassification_nextflow_zarr/
├── main.nf                    # Pipeline logic (DSL2)
├── nextflow.config            # Configuration, profiles, parameters
├── conf/                      # Scheduler-specific configs (slurm / pbs)
├── bin/                       # Pipeline scripts (Python / R / Bash)
├── assets/                    # Reference & training data
│   ├── training_data/
│   ├── methylation_clustering/
│   └── references/
├── containers/                # Singularity image & definition file
│   └── readsClassification.sif
├── envs/                      # Conda environment definition (build-time only)
├── data/                      # Optional small example data
│   └── example/
│       ├── COLO829BL_random1pct.bam
│       ├── COLO829BL_random1pct.bam.bai
│       └── samples.csv
├── results/                   # Pipeline outputs
├── work/                      # Nextflow work directory (auto-generated)
└── README.md
```

⸻

## 🧬 Required Inputs

**1. Sample sheet (CSV)**

The pipeline requires a CSV file with at least two columns (`sampleID` and `bam`):

```csv
sampleID,bam
COLO829BL,/full/path/to/COLO829BL_hg38.bam
sample_2,/full/path/to/Sample_2.bam
```

**Notes:**
- BAM must be coordinate-sorted
- BAM must be indexed (a corresponding `.bam.bai` or `.bai` must be present next to it)
- Use absolute paths (highly recommended)

⸻

## ⚙️ Execution Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `--input` | File | ✅ Yes | Path to your metadata CSV file. |
| `--account` | String | ❌ No | HPC allocation account (e.g., `--account myproject`). |
| `--outputDir` | Path | ❌ No | Output directory. Defaults to `${projectDir}/results`. |
| `--profile` | String | ❌ No | Execution profile to use: `slurm`, `pbs`, or `local`. |
| `--email` | String | ❌ No | Email address for run completion/failure notifications. |

⸻

## ▶️ Running the Pipeline

**Local execution (default)**
```console
nextflow run main.nf --input data/example/samples.csv
```

**Slurm Cluster (Production)**
```console
nextflow run main.nf \
  -profile slurm \
  --input data/example/samples.csv \
  --account myproject \
  --email user@email.com
```

**PBS Cluster**
```console
nextflow run main.nf \
  -profile pbs \
  --input data/example/samples.csv \
  --account myproject \
  --email user@email.com
```

⸻

## 🔄 Internal Process Workflow

The pipeline automatically handles the following steps in sequence:

1. **`split_bam`**: Splits large input BAM files into manageable genomic chunks based on chromosomes.
2. **`MethyperCpG_forReads_chunk`**: Extracts CpG-level methylation arrays from the long read chunks using `02_MethyperCpG_forLongReads.py`.
3. **`generate_methy_freq_table`**: Generates a high-fidelity reference methylation frequency table per sample.
4. **`estimate_parameters`**: Fits Beta distributions to the methylation frequencies via a Genetic Algorithm to output statistical parameters.
5. **`calculate_reads_likelihood`**: Calculates the likelihood probability of each read belonging to the reference cell/tissue types using pre-computed Zarr training store weights (`04_Reads_likelihood_InTissueCellTypes.py`).
6. **`merge_likelihood_results`**: Merges all computed likelihood chunks back into a single comprehensive matrix per sample.
7. **`reads_classification`**: Classifies reads into cell types mapped against a provided hierarchical tree (`05_ReadsClassification.R`).
8. **`cellType_FractionPlots`**: Generates interactive HTML Sunburst plots showing compositional cell type fractions at various hard threshold cutoffs (`06_CellTypeFraction_SunburstPlot.py`).


<iframe src="dag.html" width="100%" height="800px" frameborder="0" style="border:none;"></iframe>


### 🛠 Resource & Error Management
- The pipeline utilizes automatic **dynamic resource allocation** for memory-intensive jobs.
- If a task like `calculate_reads_likelihood` or `reads_classification` runs out of memory (OOM `exitCode 137`), Nextflow will automatically intercept the failure and **retry the job while dynamically increasing (doubling) the requested RAM**.

⸻

## 📤 Outputs

Results are written incrementally to: `results/[sampleID]/`

Including:

- `01_BAMChunks/`: Intermediate BAM chunks.
- `03_CpG_priorData/`: Methylation frequency tables and Genetic Algorithm parameters.
- `04_Reads_likelihood_results/`: Per-read methylation likelihood chunks.
- `05_ReadsClassification/`: Merged likelihoods and Final tissue/cell-type fraction assignments.
- `06_CellFraction_SunburstPlots_from_FinalOutput/`: Interactive HTML Sunburst plots showing the fraction of cell-type specific reads.

<!-- 
 <iframe src="COLO829BL_test_th10_CellFrac_SunBurstPlot.html" width="100%" height="800px" frameborder="0" style="border:none;"></iframe>
-->

[👉 **Click here to download and open the Interactive HTML Sunburst Plot!**](COLO829BL_test_th10_CellFrac_SunBurstPlot.html)

![Cell Fraction Animation](CellsFrac.gif)


⸻



## 📊 Data Structures

Here are the primary internal data shapes for the major files produced during the pipeline:

### 1. CpG Methylation Array (`.bed`)
*Generated by `02_MethyperCpG_forLongReads.py`*
A tabulated subset of raw long-read modifications.
```tsv
readname                            chr   start    end      strand  methyloc               methyVal                   warning
m54311U_201124_221800/100/ccs       chr1  10234    14500    +       chr1_10234,chr1_10245  143,210                    None
```

### 2. Methylated Component Parameters (`Parameters.tsv`)
*Generated by `03b_GA_ParametersEstimation.R`*
Defines the fitted Beta distribution and mixture weights for each sample.
```tsv
          ms1       ms2       mWeight   umWeight
Sample_1  2.54      4.21      0.68      0.32
```

### 3. Read Likelihoods (`..._All_Reads_Likelihood_merged.tsv`)
*Generated by `04_Reads_likelihood_InTissueCellTypes.py`*
A giant matrix calculating the log-likelihood (LL) of each single read against every single cell type in the training data.
```tsv
readsID        chr   start  B_Cell_LL  T_Cell_LL  Neuron_LL  CpGs_onRead
m54311U...     chr1  10234  -42.3      -55.8      -120.4     24
```

### 4. Final Classified Fractions (`..._reads_labels.tsv`)
*Generated by `05_ReadsClassification.R`*
The ultimate assignment of each individual read to its most probable origin group at a given likelihood threshold cut-off.
```tsv
readsID        chr   start  Group         Likelihood_Score
m54311U...     chr1  10234  Blood.B_Cell  -42.3
```

⸻

## 🧪 Reference & Training Data

The following files are mapped internally in `nextflow.config` and bundled with the repository under `assets/`:

- **Training methylation models:** `ThirtyThreeTissues_75SubCells_Mh_Binomial_parameters_Cov.gt5.sorted.bed.zarr`
- **Cell-type clustering metadata:** `nodes_with_leaves_mannual.xlsx`
- **Reference genome (hg38):** `GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta`

No additional downloads or database setups are required.

⸻

## 🔁 Reproducibility & Containers

This pipeline ensures portability and reproducibility by utilizing a pre-built Singularity image (`containers/readsClassification.sif`) which contains Python, R, and all required system dependencies.

**When do you need to rebuild the container?**
Only if you intentionally edit `envs/ReadsClassification_env.yml` or introduce new script `import` libraries that aren't natively supported. You do **not** need to rebuild the container for typical changes to `main.nf`, `nextflow.config`, or the `bin/` execution scripts.

⸻

## 📜 Citation

If you use this pipeline, please cite:
*Vinod Singh et al., ReadsClassification pipeline, 2026*
