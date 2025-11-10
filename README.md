# 🛰️ Planck Satellite Data Analysis — Understanding the Cosmic Microwave Background (CMB)

### 🌌 *A Data Science Approach to Exploring the Universe’s Oldest Light*

---

## 🧭 Overview

This project demonstrates how **real Planck satellite data** can be cleaned, processed, and visualized to study the **Cosmic Microwave Background (CMB)** — the faint afterglow of the Big Bang.

By applying data preprocessing and visualization techniques to Planck’s multi-band flux measurements, this project helps uncover:

- How radiation intensity varies across the sky  
- How galactic emissions differ from the uniform CMB signal  
- How data scientists transform raw astrophysical data into usable insights

---

## 🔭 Background

### 🌀 The Cosmic Microwave Background (CMB)

- The **CMB** is the leftover radiation from the **Big Bang**, released about **380,000 years after** the universe began.  
- At that time, the universe cooled enough for photons to travel freely — this is called **recombination**.  
- These photons have been stretching (redshifting) with the universe’s expansion and now appear as **microwave radiation** at a temperature of ~2.7 K.

### 🛰️ The Planck Mission

- **Launched by the European Space Agency (ESA)** in 2009, Planck measured the entire sky in **nine frequency bands** (30–857 GHz).  
- It collected **flux data** (brightness) for every pixel in the sky, helping map both:  
  - The **CMB** (cosmic signal), and  
  - **Foregrounds** (like galactic dust and synchrotron radiation).

This dataset forms the foundation of our project.

---

## 🗂️ Dataset Description

The dataset used here (a simplified version of Planck’s public data) includes the following columns:

| Column | Description |
|:--|:--|
| `name` | Source or region name |
| `ra`, `dec` | Right Ascension & Declination — celestial coordinates |
| `glon`, `glat` | Galactic longitude & latitude |
| `flux1` … `flux9` | Flux measurements (brightness) across 9 frequency bands |
| `flux_err1` … `flux_err9` | Measurement uncertainties for each flux |
| Derived Columns | `total_flux`, `mean_flux_err`, `brightness_class`, `spectral_index_proxy`, etc. |

---

## 🧹 Data Processing Pipeline

All data operations are implemented in **data_processing.py**.

| Step | Description | Why it Matters |
|:--|:--|:--|
| **1. Load Raw Data** | Reads the CSV file and prepares the DataFrame | Entry point for all further processing |
| **2. Basic Cleaning** | - Strip whitespace in column names <br> - Convert flux columns to numeric <br> - Replace invalid (≤0) flux/error values with NaN <br> - Drop rows with all fluxes missing <br> - Remove duplicates | Removes physically impossible and redundant entries |
| **3. Derived Features** | - `total_flux`: Sum of all fluxes <br> - `mean_flux_err`: Avg. uncertainty <br> - `flux_count`: Number of valid flux detections <br> - `brightness_class`: Low/Medium/High quantile grouping <br> - `spectral_index_proxy`: Ratio of flux1/flux9 over frequency ratio | Generates meaningful astrophysical indicators |
| **4. Normalization** | - Scales fluxes between 0–1 <br> - Adds z-score columns for statistical comparison | Standardizes data for fair analysis |
| **5. Reliability Filter** | Marks unreliable entries where `mean_flux_err` > 50% of `total_flux` | Ensures only credible data is used |
| **6. IQR Outlier Removal** | Removes extreme flux outliers using Interquartile Range (IQR) | Keeps only statistically consistent data |

---

## 📈 Data Visualizations

All visualization functions are implemented in **viz_helpers.py**.

| Visualization | Function | Description | Scientific Relevance |
|:--|:--|:--|:--|
| **Galactic Scatter Map** | `galactic_scatter()` | Plots galactic longitude vs latitude, color-coded by flux or brightness | Shows radiation variation across Milky Way and helps isolate uniform CMB regions |
| **Flux Histogram** | `flux_histogram()` | Displays flux distribution | Reveals that most sky regions show low flux (CMB level) while some are bright (galactic dust) |
| **Flux Correlation Heatmap** | `flux_corr_heatmap()` | Shows correlation between the nine frequency bands | Identifies which frequencies capture similar physical phenomena |
| **Spectral Energy Distribution (SED)** | `sed_plot()` | Plots flux vs band index for a chosen source | Helps identify source type — flat = CMB, steep = galactic radiation |
| **3D Brightness Cloud** | `plot_3d()` | 3D scatter of RA, DEC, total_flux | Reveals spatial distribution of radiation intensity |

---

## 🧠 Theoretical Concept: Spectral Index Proxy

The **spectral index** tells us how a source’s brightness changes with frequency.

\[
\text{Spectral Index} = \frac{\log(\text{flux}_1 / \text{flux}_9)}{\log(30 / 857)}
\]

- Here, **30 GHz** and **857 GHz** are Planck’s lowest and highest frequency bands.  
- A **flat spectral index (~0)** → uniform emission like the CMB.  
- A **steep spectral index** → strong frequency dependence (e.g., dust or synchrotron radiation).  

This helps distinguish **cosmic background** from **foreground contamination**.

---

## 💡 Key Insights

1. **Most sky regions** show *low and uniform flux values*, consistent with the CMB.  
2. **High flux regions** and *non-flat spectral indices* reveal galactic dust and star-forming regions.  
3. **Flux correlations** across bands highlight overlapping physical emissions.  
4. **Visualization-driven cleaning** mirrors how cosmologists isolate the CMB from foreground noise.

---

## 🚀 Project Summary

This project bridges **data science** and **cosmology**, demonstrating how raw satellite flux readings can be transformed into meaningful insights.

It provides:
- Real-world experience in **scientific data cleaning and normalization**
- Understanding of **Planck’s multi-band flux measurements**
- Visual proof of how **data science contributes to astrophysical discovery**

---

## 📚 References

- ESA Planck Mission: [https://www.esa.int/Planck](https://www.esa.int/Planck)  
- Planck Legacy Archive: [https://pla.esac.esa.int/](https://pla.esac.esa.int/)  
- NASA/IPAC Infrared Science Archive  
- *Planck 2018 Results — Overview and Cosmological Legacy*, A&A (2020)

---

## 👨‍💻 Author

**Siddhant Rana**  
B.Tech — Computer Science (Data Science)  
NMIMS Chandigarh  

