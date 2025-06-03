import re
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Komut satırından dosya okuma
lines = open(sys.argv[1], encoding='utf-8').read().splitlines()

# Noktalama karakterleri
PUNCTUATIONS = r"[!\"#$%&'()*+,-./:;<=>?@\[\\\]^_`{|}~]"

# Öznitelik çıkarma fonksiyonu
def extract_features(line):
    puncts = [m for m in re.finditer(PUNCTUATIONS, line)]
    return {
        "punct_count": len(puncts),
        "punct_types": len(set(m.group() for m in puncts)),
        "punct_mean_pos": np.mean([m.start() / len(line) for m in puncts]) if puncts else 0.0
    }

# Özellik çıkarımı
feature_list = [extract_features(line) for line in lines]
df = pd.DataFrame(feature_list)

# Toplam noktalama sayısı (k üst sınırı olarak)
total_punct = df["punct_count"].sum()

# Elbow Yöntemi ile optimal k bulma
inertias = []
K_range = range(1, min(21, len(df)))  # Çok veri varsa max 20 küme
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(df)
    inertias.append(km.inertia_)

# Elbow grafiği
plt.figure(figsize=(8, 5))
plt.plot(K_range, inertias, marker='o')
plt.title('Elbow Yöntemi ile Optimal K Seçimi')
plt.xlabel('Küme Sayısı (k)')
plt.ylabel('Inertia (Toplam Hata)')
plt.grid(True)
plt.tight_layout()
plt.savefig("elbow_k.png")
plt.close()

# Nihai kümeleme (otomatik k seçmek için burada sabit 5 kullanabilirsin ya da K=optimal seçilebilir)
optimal_k = 5  # ya da elbow grafik analizine göre manuel gir
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
df['cluster'] = kmeans.fit_predict(df)

# Sonuçları yazdırma
result = pd.concat([pd.Series(lines, name="dizi"), df], axis=1)
print(result)

# Seaborn ile görselleştirme
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="punct_mean_pos", y="punct_count", hue="cluster", palette="Set2", s=60)
plt.title(f"K-means Kümeleme (k={optimal_k})")
plt.xlabel("Noktalama Konum Ort.")
plt.ylabel("Noktalama Sayısı")
plt.legend(title="Küme")
plt.tight_layout()
plt.savefig("kmeans_scatter.png")
plt.close()
