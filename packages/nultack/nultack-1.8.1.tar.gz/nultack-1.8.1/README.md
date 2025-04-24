# Nültack - Python Code Steganography Library

**Versi:** 1.8.0  
**Lisensi:** MIT  
**Author:** [Eternals-Satya](https://github.com/Eternals-Satya)

## Apa Itu Nültack?

**Nültack** adalah pustaka Python untuk menyembunyikan (`encode`), mengeksekusi (`execute`), dan melindungi (`protect`) kode Python dalam bentuk payload yang sulit dianalisis secara statis. Cocok untuk penggunaan seperti anti-debugging, anti-AI, dan sistem keamanan tingkat lanjut.

---

## Instalasi

```bash
pip install nultack
```
Atau untuk memastikan versi terbaru:
```bash
pip install --upgrade --no-cache-dir nultack==1.8.0
```

---

## Fitur Utama

**Encode:** Mengubah kode Python menjadi payload yang terenkripsi.
**Execute:** Menjalankan payload terenkripsi tanpa perlu decode manual.
**Protect:** Menyisipkan mekanisme perlindungan seperti anti-decode, anti-debugger, dan anti-AI static analyzer.
**Hide:** Membuat payload siap eksekusi dengan satu baris.



---

## Contoh Penggunaan

1. Encode Kode Python
```
import nultack

source_code = '''
print("Halo dari dalam payload!")
'''

payload = nultack.encode(source_code)
print(payload)
```
2. Eksekusi Payload
```
import nultack

payload = "<payload yang dihasilkan>"
nultack.execute(payload)
```
3. Shortcut: hide()
```
import nultack

source = '''
print("Payload rahasia...")
'''

print(nultack.hide(source))
```
Output:
```
import nultack; nultack.execute("payload_terenkripsi_di_sini")
```

---

## Fitur Perlindungan
Kelas NültackProtector dapat digunakan untuk menyisipkan proteksi tambahan terhadap kode:
```
from nultack.protection import NültackProtector

protected_code = NültackProtector().protect('''
print("Coba bypass aku kalau bisa.")
''')

print(protected_code)
```

---

### Docs
GitHub: [Eternals](github.com/Eternals-Satya/Nultack)
TikTok: [gw](@anakkecil_s)
PyPI: pypi.org/project/nultack



---

## Contribute
Pull request dan laporan isu sangat diterima! Jangan ragu untuk ikut serta dalam pengembangan.


---

Copyright © 2025
Eternals dari [Vlazars](https://whatsapp.com/channel/0029VaZLpqf8aKvHckUi4f1z)

---

