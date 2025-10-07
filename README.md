# Backend for Gender Detection
Ini merupakan repositori backend dari [proyek ini](https://github.com/FajarRamadhanBBX/AR-for-gender-prediction), yang memiliki fungsi utama untuk melakukan prediksi gender dari hasil tangkapan gambar pada aplikasi AR.

## Endpoint
- `/` : Path ini bisa digunakan untuk menguji apakah URL sudah dapat diakses atau tidak
- `/predict` : Path ini digunakan untuk melakukan prediksi. Cara kerjanya dengan menerima data gambar yang sudah dikonversi menjadi string base64, lalu dilakukan preprocessing, dikonsumsi oleh model, lalu hasilnya akan dikembalikan lagi 

## Prasyarat
### Deploy secara lokal
- Python
- `pip`
- git
  
### Deploy di AWS EC2
- Akun AWS (Opsional, jika ingin menggunakan cloud)

---
## Panduan Deploy Aplikasi secara Lokal
### 1. Kloning repositori
```bash
  git clone https://github.com/FajarRamadhanBBX/AR-for-gender-prediction-backend.git
  cd AR-for-gender-prediction-backend
```

### 2. Buat dan Aktifkan Virtual Environment
buat virtual environment menggunakan perintah berikut
```bash
  python -m venv venv
```
Lalu aktifkan dengan menggunakan perintah berikut
- Windows
```bash
  venv\Scripts\activate
```
- macOS / Linux
```bash
  source venv\Scripts\activate
```

### 3. Instal Dependensi yang Dibutuhkan
Instal semua library Python yang dibutuhkan oleh proyek dengan satu perintah
```bash
  pip install -r requirements.txt
```

### 4. Jalankan Server
```bash
  uvicorn app:app --host 0.0.0.0 --port 8000
```
`--host 0.0.0.0` berarti semua ip dapat mengakses server yang ada pada layanan ini.

### 5. Verifikasi
Buka browser dan navigasi ke sini
```bash
  http://localhost:8000/
```
Jika muncul pesan bahwa API sudah berjalan, maka artinya server sukses berjalan

---
## Panduan deploy ke EC2 dan integrasi 
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
