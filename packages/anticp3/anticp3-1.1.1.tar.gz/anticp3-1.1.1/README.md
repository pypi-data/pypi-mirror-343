# ANTICP3 — Anticancer Protein Prediction

**ANTICP3** is a LLM-based tool for binary classification of proteins into *Anticancer* or *Non-Anticancer* classes, based solely on their primary amino acid sequences. It leverages the powerful [ESM2-t33](https://huggingface.co/facebook/esm2_t33_650M_UR50D) transformer model, fine-tuned specifically for anticancer protein prediction.

> Developed by **Prof. G. P. S. Raghava's Lab**, IIIT-Delhi  
> 📄 Please cite: [ANTICP3](https://webs.iiitd.edu.in/raghava/anticp3)

---

## Features

- Fine-tuned ESM2 model for accurate prediction.
- Accepts input in FASTA format.
- Outputs CSV with predicted labels and probabilities.
- Supports CPU and CUDA for faster inference.
- Easy to integrate into pipelines and large-scale datasets.

---

## Model Details

- **Base Model:** facebook/esm2_t33_650M_UR50D
- **Fine-Tuned On:** Anticancer protein dataset
- **Classification Type:** Binary (Anticancer / Non-Anticancer)
- **Output Format:** CSV with prediction scores and labels

---

### Installation:
```bash 
pip install anticp3
```