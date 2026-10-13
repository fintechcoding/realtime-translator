# Build & Installer — RealTime Translator

Windows `.exe` paketleme (PyInstaller) ve kurulum sihirbazi (Inno Setup) uretimi.

## Gereksinimler

- Python 3.11+ ve proje bagimliliklari: `pip install -r requirements.txt`
- PyInstaller: `pip install pyinstaller` (build script gerekirse otomatik kurar)
- **Inno Setup 6** (setup.exe uretmek icin): https://jrsoftware.org/isdl.php
  - Kurulu degilse de sorun yok: script yine de `dist\RealTimeTranslator\` altinda
    calistirilabilir (portable) uygulamayi uretir, sadece setup.exe adimini atlar.

## Tek komutla build

```powershell
powershell -ExecutionPolicy Bypass -File build.ps1
```

Bu script sirayla:
1. App ikonunu uretir (`tools\make_icon.py` -> `app\gui\assets\app.ico`)
2. Eski `build\`, `dist\`, `installer_output\` klasorlerini temizler
3. PyInstaller ile uygulamayi paketler -> `dist\RealTimeTranslator\RealTimeTranslator.exe`
4. Inno Setup bulunursa kurulum sihirbazini derler -> `installer_output\RealTimeTranslator-Setup-<versiyon>.exe`

Sadece portable exe istiyorsan:
```powershell
powershell -ExecutionPolicy Bypass -File build.ps1 -SkipInstaller
```

## Manuel adimlar (istege bagli)

```powershell
# 1) Paketleme
python -m PyInstaller RealTimeTranslator.spec --noconfirm --clean

# 2) Kurulum sihirbazi (Inno Setup kuruluysa)
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

## Ciktilar

| Cikti | Yol |
|-------|-----|
| Portable uygulama | `dist\RealTimeTranslator\` (klasoru komple tasiyabilirsin) |
| Kurulum sihirbazi | `installer_output\RealTimeTranslator-Setup-0.1.0.exe` |

## Kurulum davranisi

- Uygulama `C:\Program Files\RealTime Translator` altina kurulur (admin gerekir).
- Baslat menusu kisayolu olusur; masaustu kisayolu kurulumda secmelidir (varsayilan kapali).
- **Kullanici ayarlari ve API anahtarlari** `%APPDATA%\RealTime Translator\`
  (`config.yaml` + `.env`) altina yazilir — Program Files salt-okunur oldugundan
  uygulama ayarlari oraya kaydetmez. Bu sayede kaldirma islemi API anahtarlarini silmez.

## Surum yukseltme

Surumu degistirmek icin iki yeri guncelle:
- `app/utils/constants.py` -> `APP_VERSION`
- `installer.iss` -> `#define MyAppVersion`

## Notlar

- Build ilk seferde birkac dakika surer (Azure Speech ve PortAudio ikili dosyalari toplanir).
- Antivirus bazen PyInstaller exe'lerini yanlis pozitif olarak isaretleyebilir; imzalama
  (code signing) bunu azaltir ama bu projede yapilandirilmamistir.
