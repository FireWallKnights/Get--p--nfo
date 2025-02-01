import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import platform
import socket
import uuid
import psutil
import re
import json
import time


# IP adresi formatını doğrulayan fonksiyon
def validate_ip(ip):
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return ip_pattern.match(ip)


# IP bilgilerini ve konum verilerini al
def get_ip_info(ip_address):
    try:
        response = requests.get(f'http://ipapi.co/{ip_address}/json')
        ip_info = response.json()

        # Konum bilgileri
        konum_bilgisi = {
            'Ülke': ip_info.get('country_name'),
            'Bölge': ip_info.get('region'),
            'Şehir': ip_info.get('city'),
            'Posta Kodu': ip_info.get('postal'),
            'Enlem': ip_info.get('latitude'),
            'Boylam': ip_info.get('longitude')
        }

        return ip_info, konum_bilgisi
    except Exception as e:
        return {"hata": str(e)}, {}


# Cihaz bilgilerini al
def get_device_info():
    system = platform.system()
    node = platform.node()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    processor = platform.processor()
    python_version = platform.python_version()
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    mac_address = ':'.join(
        ['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])
    fqdn = socket.getfqdn()

    uptime = psutil.boot_time()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return {
        'Sistem': system,
        'Cihaz İsmi': node,
        'Sürüm': release,
        'Versiyon': version,
        'Makine': machine,
        'İşlemci': processor,
        'Python Versiyonu': python_version,
        'Yerel IP': local_ip,
        'Hostname': hostname,
        'MAC Adresi': mac_address,
        'FQDN': fqdn,
        'Açık Kalma Süresi': uptime,
        'Bellek': memory,
        'Disk': disk,
    }


# Bilgileri göster ve yükleme animasyonu ekle
def show_info():
    ip_address = ip_entry.get()

    if not validate_ip(ip_address):
        messagebox.showwarning("Giriş Hatası", "Lütfen geçerli bir IP adresi girin.")
        return

    # Yükleme animasyonu
    loading_label.config(text="IP bilgileri getiriliyor, lütfen bekleyin...")
    root.update()

    time.sleep(1.5)  # Animasyonun görünmesi için kısa bir bekleme süresi

    ip_info, konum_bilgisi = get_ip_info(ip_address)
    if "hata" in ip_info:
        messagebox.showerror("Hata", f"Bilgiler alınamadı: {ip_info['hata']}")
        loading_label.config(text="")
        return

    device_info = get_device_info()

    info_text = "IP Bilgileri:\n"
    for key, value in ip_info.items():
        info_text += f"  {key}: {value}\n"

    info_text += "\nCihaz Bilgileri:\n"
    for key, value in device_info.items():
        info_text += f"  {key}: {value}\n"

    # Konum Bilgilerini Ekle
    info_text += "\nKonum Bilgileri:\n"
    for key, value in konum_bilgisi.items():
        info_text += f"  {key}: {value}\n"

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, info_text)

    history_list.insert(tk.END, ip_address)
    loading_label.config(text="")  # Yükleme animasyonunu kaldır


# Bilgileri temizle
def clear_info():
    output_text.delete(1.0, tk.END)
    ip_entry.delete(0, tk.END)


# Bilgileri dosyaya aktar
def export_info():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Metin Dosyaları", ".txt"), ("JSON Dosyaları", ".json")])
    if not file_path:
        return

    content = output_text.get(1.0, tk.END).strip()

    if file_path.endswith(".json"):
        try:
            content_dict = {}
            for line in content.splitlines():
                if ": " in line:
                    key, value = line.split(": ", 1)
                    content_dict[key.strip()] = value.strip()
            content = json.dumps(content_dict, indent=4)
        except Exception as e:
            messagebox.showerror("Aktarma Hatası", f"JSON olarak dışa aktarılamadı: {e}")
            return

    with open(file_path, 'w') as file:
        file.write(content)

    messagebox.showinfo("Başarılı", f"Bilgiler {file_path} dosyasına aktarıldı")


# Ana pencereyi oluştur
root = tk.Tk()
root.title("IP Adres Takip Sistemi")

# Modern arayüz için ttk
mainframe = ttk.Frame(root, padding="5")
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# IP Giriş Alanı
ttk.Label(mainframe, text="IP Adresi Girin:", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
ip_entry = ttk.Entry(mainframe, width=25, font=("Arial", 14))
ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

# Butonlar
buttons_frame = ttk.Frame(mainframe, padding="5")
buttons_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))

ttk.Button(buttons_frame, text="IP Tarama", command=show_info).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(buttons_frame, text="Temizle", command=clear_info).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(buttons_frame, text="Dışa Aktar", command=export_info).grid(row=0, column=2, padx=5, pady=5)

# Yükleme Animasyonu
loading_label = ttk.Label(mainframe, text="", font=("Arial", 10), foreground="blue")
loading_label.grid(row=2, column=0, columnspan=2)

# Çıktı Metin Kutusu
output_text = tk.Text(mainframe, wrap='word', width=50, height=15, font=("Arial", 12))
output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Arama Geçmişi
history_frame = ttk.Frame(mainframe, padding="5")
history_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))

ttk.Label(history_frame, text="Arama Geçmişi:", font=("Arial", 14)).grid(row=0, column=0, sticky=tk.W)
history_list = tk.Listbox(history_frame, height=5, font=("Arial", 12))
history_list.grid(row=1, column=0, sticky=(tk.W, tk.E))

# Pencere boyutlandırma
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)

# Ana döngüyü başlat
root.mainloop()
