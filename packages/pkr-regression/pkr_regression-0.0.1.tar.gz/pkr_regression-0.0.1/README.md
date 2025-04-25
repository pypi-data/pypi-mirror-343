# Pure Kernel Regression (PKR)

A *rule‑based*, **explainable** alternative to black‑box regression that trusts only the "cleanest" regions of your feature space.

---
## 🌟 Why PKR?
* **Noise‑proof:** uses only regions where ≥90 % of training rows share the *same* extreme label.
* **Explainable:** every prediction is traced to a single kernel rule — or falls back to a safe median.
* **Plug‑and‑play:** one call to `pkr.fit(train)` and `pkr.predict(test)` — no hyper‑parameter hunt.

---
## ⚙️ Algorithm in 60 seconds
1. **Extreme–label flagging**  
   Compute the 20th (q20) and 80th (q80) percentiles of the target.  
   * y ≤ q20 ⇒ `y_bin = 0`  
   * y ≥ q80 ⇒ `y_bin = 1`
2. **Exhaustive window scan (1‑D → 3‑D)**  
   * Numeric cols: 0.5‑wide sliding windows, step 0.25  
   * Categorical : exact match
3. **Keep only _“clean kernels”_**  
   ≥90 % rows share the same `y_bin` **and** `count ≥ 10`.
4. **Representative values**  
   * `rep0` = 33rd percentile of rows with `y_bin = 0`  
   * `rep1` = 66th percentile of rows with `y_bin = 1`  
   * `rep_mid` = global median of *y*
5. **Prediction rule**  
   * *No matching kernel* → `rep_mid`  
   * *One match* → `rep0` or `rep1` (by label)  
   * *Many matches* → average of the matched reps

---
## 🔧 Quick start
```bash
pip install pkr   # (coming soon)
```
```python
from pkr import PKR

model = PKR(max_dim=3)
model.fit(train_df, target="Listening_Time_minutes")

pred = model.predict(test_df)
submission = test_df[["id"]].assign(Listening_Time_minutes=pred)
submission.to_csv("submission.csv", index=False)
```
A full Google Colab demo notebook is in **`/notebooks/PKR_demo.ipynb`**.

---
## 📂 Repository layout
```
├── src/                 # core library
│   └── pkr.py
├── notebooks/           # demos (Colab & Kaggle)
├── examples/            # sample data + CLI
└── README.md            # you are here
```

---
## 📈 Roadmap
- [ ] PyPI package
- [ ] Auto‑kernel pruning for high‑dim data
- [ ] Stacking helper (PKR + any ML model)

---
## 🖋 Citation
If you build on PKR, please cite (pending arXiv link):
```
@misc{yusuf2025pkr,
  title  = {Pure Kernel Regression: Noise‑free Region Rules for Fast Tabular Prediction},
  author = {Yusuf Burak …},
  year   = {2025},
  url    = {https://github.com/YusufBurak/PKR}
}
```

---
## 📜 License
MIT — free for personal & commercial use with attribution.

