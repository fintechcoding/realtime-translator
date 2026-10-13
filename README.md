# RealTime Translator

Gerçek zamanlı ses çeviri uygulaması. Konuştuğunuz anda sesinizi hedef dile çevirip
sentezler ve VB-Cable üzerinden Zoom / Telegram gibi uygulamalara "mikrofon" olarak iletir.

**Deepgram STT → DeepL / Google Translate → Azure / Deepgram TTS**

## Özellikler

- 🎙️ Canlı konuşma tanıma (Deepgram Nova-2, WebSocket streaming)
- 🌍 15 dil desteği, DeepL veya Google Cloud Translation (seçimli)
- 🔊 Azure Speech + Deepgram Aura ile sesli çıkış (dil bazlı otomatik seçim)
- 🖥️ PyQt6 kurumsal koyu arayüz (Çeviri / İstatistik / Ayarlar)
- 🌐 Çoklu arayüz dili: Türkçe / English / Русский
- 📊 Oturum istatistikleri ve DeepL kullanım takibi

## Kurulum (geliştirme)

```bash
pip install -r requirements.txt
python main.py
```

API anahtarlarını uygulama içindeki **Ayarlar** sayfasından (veya `.env` dosyasından) girin.
Örnek için `.env.example` dosyasına bakın. Sanal ses yönlendirmesi için
[VB-Cable](https://vb-audio.com/Cable/) kurulu olmalıdır.

## Windows kurulum paketi oluşturma

```powershell
powershell -ExecutionPolicy Bypass -File build.ps1
```

- Portable uygulama → `dist\RealTimeTranslator\`
- Kurulum sihirbazı → `installer_output\RealTimeTranslator-Setup-<ver>.exe`

Detaylar: [BUILD.md](BUILD.md)

## Teknoloji

Python 3.11+ · PyQt6 + qasync · Deepgram SDK · DeepL · Google Cloud Translation ·
Azure Cognitive Services Speech · sounddevice

## Lisans

Kişisel kullanım. API sağlayıcılarının kendi kullanım koşulları geçerlidir.
