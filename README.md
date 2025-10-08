# Backend for Gender Detection 🔬

Ini merupakan repositori backend dari [proyek AR for Gender Prediction](https://github.com/FajarRamadhanBBX/AR-for-gender-prediction). Fungsi utamanya adalah untuk menerima gambar dari aplikasi AR, memprosesnya menggunakan model AI, dan mengembalikan hasil prediksi gender.

---
## 🚦 Endpoint API

* **`GET /`**: Endpoint dasar untuk menguji konektivitas server. Akan mengembalikan pesan jika server berjalan dengan baik.
* **`POST /predict`**: Endpoint utama untuk prediksi. Menerima payload berisi gambar dalam format string Base64, memprosesnya, dan mengembalikan hasil prediksi.

---
## 📋 Prasyarat

* Python
* `pip` (Manajer paket Python)
* `git` (Untuk kloning repositori)
* Akun AWS (Opsional, jika ingin melakukan deploy ke cloud EC2)

---
## 💻 Panduan Deploy Aplikasi Secara Lokal

Gunakan panduan ini untuk menjalankan server di komputer lokal untuk pengembangan.

### 1. Kloning Repositori

```bash
git clone [https://github.com/FajarRamadhanBBX/backend-for-AR-gender-detection.git](https://github.com/FajarRamadhanBBX/backend-for-AR-gender-detection.git)
cd AR-for-gender-prediction-backend
```

### 2. Buat dan Aktifkan Virtual Environment

Digunakan untuk mengisolasi dependensi proyek.

```bash
# Membuat virtual environment bernama 'venv'
python -m venv venv
```
Aktifkan environment dengan cara:
- Windows : `venv\Scripts\activate`
- macOS/Linux : `source venv/bin/activate`

### 3. Instal Dependensi
```bash
pip install -r requirements.txt
```

### 4. Jalankan server
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Verifikasi
Buka browser dan navigasi ke `http://localhost:8000/docs`. Jika halaman dokumentasi interaktif Swagger UI muncul, artinya server sudah berjalan dengan sukses!


---
## ☁️ Panduan Deploy Backend melalui Cloud (EC2)

### 1. Siapkan dan Hubungkan ke EC2
- Launch sebuah instance EC2 baru di AWS. Direkomendasikan menggunakan AMI bernama Amazon Linux
- Pilih instance type sesuai kebutuhan
- Saat mengkonfigurasi Security Group, pastikan:
  - ubah `SSH` menjadi dari **anywhere** menjadi **my ip**. Ini dilakukan untuk menjaga port SSH agar tidak bisa diakses orang sembarangan
  - Centang **Allow HTTP traffic from internet** dan biarkan menjadi **anywhere** agar bisa diakses semua orang
- Buat keypair sesuai dengan sistem operasi
- Masuk ke EC2 dengan memanfaatkan keypair tersebut

### 2. Setup Lingkungan di Server EC2
Jalankan perintah berikut
```bash
# Update semua paket yang terinstal
sudo yum update -y
# Install git, python3-devel, dan gcc (diperlukan untuk beberapa paket pip)
sudo yum install git python3-devel gcc -y
# Install paket untuk membuat virtual environment
sudo yum install python3-venv -y
```

### 3. Kloning Repositori Proyek Anda
```bash
# Kloning repositori Anda
git clone https://github.com/FajarRamadhanBBX/backend-for-AR-gender-detection.git

# Masuk ke direktori proyek
cd backend-for-gender-prediction # <-- Ganti dengan nama folder repo Anda
```

### 4. Setup Aplikasi Python
```bash
# Buat virtual environment bernama 'venv' menggunakan python3
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate

# Instal semua dependensi dari file requirements.txt
pip install -r requirements.txt
```

### 5. Buat dan Konfigurasi `systemd` Service
Ini adalah cara agar server Anda tetap berjalan 24/7 dan otomatis menyala saat EC2 *reboot*.
- Buat file service `systemd`:
```bash
sudo nano /etc/systemd/system/genderapp.service
```
- Isi file service tersebut dengan menyalin konfigurasi di bawah ini.
```bash
[Unit]
Description=Gunicorn service for Gender Prediction FastAPI App
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/AR-for-gender-prediction
ExecStart=/home/ec2-user/AR-for-gender-prediction/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app -b 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```
- Simpan file (tekan `Ctrl+X`, lalu `Y`, lalu `Enter`).

### 6. Jalankan dan Aktifkan Service
```bash
# Muat ulang systemd untuk membaca file service baru Anda
sudo systemctl daemon-reload

# Jalankan service Anda sekarang
sudo systemctl start genderapp

# Aktifkan service agar berjalan otomatis setiap kali server boot
sudo systemctl enable genderapp
```

### 7. Verifikasi
```bash
sudo systemctl status genderapp
```

Periksa status, jika `active (running)` berwarna hijau, maka server sudah berjalan.
Untuk mengaksesnya dapat menggunakan browser dengan mengetikkan melalui `http://<Alamat_IP_Publik_EC2>:8000/` , atau diimplementasikan pada Unity dan melakukan hit untuk prediksi pada `http://<Alamat_IP_Publik_EC2>:8000/predict`
