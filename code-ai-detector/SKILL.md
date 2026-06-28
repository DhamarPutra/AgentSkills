---
name: code-ai-detector
description: Detect project using AI or not.
---

# Skill: Detect AI Coding Patterns
Analisis kode untuk mendeteksi kemungkinan ditulis oleh AI berdasarkan pola-pola spesifik di bawah ini. Indikator ini digunakan untuk memberikan metrik tambahan dalam evaluasi proyek tanpa memengaruhi perhitungan bobot nilai akhir.

## Kriteria & Heuristik Deteksi AI

### 1. Pola Komentar dan Dokumentasi (AI-Style Comments)
*   **Komentar Terlalu Sempurna:** Penulisan JSDoc, Docstring, atau inline comments yang sangat formal, rapi, lengkap dengan parameter/return types, tanpa ada kesalahan ketik (typo).
*   **Komentar "Menggurui" (Over-explaining):** Menjelaskan hal-hal sepele yang sudah jelas dari nama fungsinya sendiri (misal: `// Memulai koneksi ke database supabase` tepat di atas `supabase.connect()`).
*   **Gaya Bahasa:** Struktur kalimat pasif dan formal yang khas dihasilkan LLM.

### 2. Struktur Kode & Boilerplate Kaku (Textbook Patterns)
*   **Pola Standar Textbook:** Penulisan algoritma atau struktur folder yang persis mengikuti template populer dari dokumentasi resmi atau tutorial AI tanpa penyesuaian gaya personal pengembang.
*   **Penanganan Error Generik:** Pola `try-catch` berulang dengan format log yang identik (misal selalu menggunakan `console.error(error.message)` atau `res.status(500).json({ success: false, message: error.message })` tanpa penanganan spesifik konteks).
*   **Ketiadaan Jalan Pintas (No Hacky Code):** AI jarang menulis kode "quick-fix", penanda sementara seperti `TODO`, `FIXME`, `HACK`, atau komentar-komentar ekspresif yang biasa ditulis developer manusia saat terburu-buru.

### 3. Penamaan Variabel & Fungsi (Naming Conventions)
*   **Nama Terlalu Panjang & Deskriptif:** Variabel atau fungsi dengan nama deskriptif ekstrem (misal: `handleUserRegistrationAndDatabaseInsertionFlow`).
*   **Konsistensi CamelCase/SnakeCase yang Sempurna:** Penamaan variabel yang sangat konsisten di seluruh modul, bahkan ketika menggabungkan library yang berbeda gaya.

### 4. Kebersihan dan Organisasi Kode
*   **Ketiadaan Dead Code:** Tidak ada sisa kode yang di-comment out, `console.log` debug yang tertinggal (kecuali sengaja dibuat terstruktur), atau variabel yang tidak terpakai (unused variables).
*   **Struktur Impor yang Rapi:** Pengelompokan impor (library vs internal file) yang terformat sempurna seperti hasil auto-import / formatting editor.

---

## Panduan Penilaian & Output Rubrik

Penilaian ini merupakan **rubrik tambahan (stand-alone metric)** yang **tidak memiliki bobot (tanpa bobot)** dalam nilai akhir (total score). Hasil analisis disajikan dalam bentuk presentase probabilitas AI beserta ringkasan temuan.

### Format Output Penilaian
Pada file `penilaian.json`, metrik ini disimpan langsung di tingkat objek kelompok (di luar objek `kriteria` yang berbobot) menggunakan format berikut:

```json
{
  "kelompok": 1,
  "folder": "NamaFolder",
  "kriteria": {
    "technical_execution": { "bobot": 20, "nilai": 92 },
    "ui_ux_quality": { "bobot": 15, "nilai": 88 }
    // Kriteria berbobot lainnya...
  },
  "ai_detection": {
    "probability": 75,
    "analisis": "Analisis terperinci mengenai indikator AI yang ditemukan pada kode sumber kelompok."
  },
  "total": 31.6,
  "kesimpulan": {
    "ringkasan": "..."
  }
}
```

### Indikator Skor Probabilitas:
*   **0% - 25% (Sangat Rendah / Dominan Manusia):** Banyak ditemukan gaya penulisan personal, komentar minimalis/spesifik, adanya kode hacky/debug, atau ketidakkonsistenan minor yang wajar.
*   **26% - 50% (Rendah ke Sedang):** Struktur kode bersih dengan beberapa boilerplate standar, namun masih memperlihatkan logika kustom yang spesifik.
*   **51% - 75% (Tinggi / Indikasi Kuat AI):** Sebagian besar komponen pendukung, helper, database schema, atau boilerplate endpoint ditulis dengan struktur sempurna khas AI. Dokumentasi sangat rapi.
*   **76% - 100% (Sangat Tinggi / Dominan AI):** Hampir seluruh codebase dibangun menggunakan kode generator AI tanpa modifikasi personal yang berarti. Komentar di setiap baris sangat rapi, terstruktur, dan formal.