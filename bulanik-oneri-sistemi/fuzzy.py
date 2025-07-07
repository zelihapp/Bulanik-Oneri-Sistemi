
"""
E-Ticaret Bulanık Mantık Öneri Sistemi
Bulanık mantık kullanarak kişiselleştirilmiş ürün önerisi yapan sistem

Gerekli kütüphaneler:
pip install scikit-fuzzy matplotlib numpy
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt



import warnings
warnings.filterwarnings('ignore')

# Türkçe karakter desteği için matplotlib ayarları
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

class EticaretBulanikOneriSistemi:
    """
    E-ticaret sitesi için bulanık mantık tabanlı ürün öneri sistemi
    """
    
    def __init__(self):
        self.sistem_kurulumu()
        self.kontrol_sistemi_olustur()
        
    def sistem_kurulumu(self):
        """
        Bulanık değişkenleri ve üyelik fonksiyonlarını tanımlar
        """
        print("🔧 Sistem kuruluyor...")
        
        # Giriş değişkenleri tanımlama
        self.musteri_yasi = ctrl.Antecedent(np.arange(18, 81, 1), 'musteri_yasi')
        self.aylik_gelir = ctrl.Antecedent(np.arange(1000, 15001, 100), 'aylik_gelir')
        self.onceki_satin_alma = ctrl.Antecedent(np.arange(0, 101, 1), 'onceki_satin_alma')
        self.kategori_ilgisi = ctrl.Antecedent(np.arange(0, 101, 1), 'kategori_ilgisi')
        
        # Çıkış değişkeni tanımlama
        self.oneri_puani = ctrl.Consequent(np.arange(0, 101, 1), 'oneri_puani')
        
        # Müşteri yaşı üyelik fonksiyonları
        self.musteri_yasi['genc'] = fuzz.trimf(self.musteri_yasi.universe, [18, 18, 35])
        self.musteri_yasi['orta_yas'] = fuzz.trimf(self.musteri_yasi.universe, [30, 42, 55])
        self.musteri_yasi['yasli'] = fuzz.trimf(self.musteri_yasi.universe, [50, 80, 80])
        
        # Aylık gelir üyelik fonksiyonları
        self.aylik_gelir['dusuk'] = fuzz.trimf(self.aylik_gelir.universe, [1000, 1000, 5000])
        self.aylik_gelir['orta'] = fuzz.trimf(self.aylik_gelir.universe, [4000, 7000, 10000])
        self.aylik_gelir['yuksek'] = fuzz.trimf(self.aylik_gelir.universe, [8000, 15000, 15000])
        
        # Önceki satın alma skoru üyelik fonksiyonları
        self.onceki_satin_alma['dusuk'] = fuzz.trimf(self.onceki_satin_alma.universe, [0, 0, 40])
        self.onceki_satin_alma['orta'] = fuzz.trimf(self.onceki_satin_alma.universe, [20, 50, 70])
        self.onceki_satin_alma['yuksek'] = fuzz.trimf(self.onceki_satin_alma.universe, [50, 100, 100])
        
        # Kategori ilgisi üyelik fonksiyonları
        self.kategori_ilgisi['dusuk'] = fuzz.trimf(self.kategori_ilgisi.universe, [0, 0, 40])
        self.kategori_ilgisi['orta'] = fuzz.trimf(self.kategori_ilgisi.universe, [20, 50, 70])
        self.kategori_ilgisi['yuksek'] = fuzz.trimf(self.kategori_ilgisi.universe, [50, 100, 100])
        
        # Öneri puanı üyelik fonksiyonları
        self.oneri_puani['dusuk'] = fuzz.trimf(self.oneri_puani.universe, [0, 0, 40])
        self.oneri_puani['orta'] = fuzz.trimf(self.oneri_puani.universe, [20, 50, 70])
        self.oneri_puani['yuksek'] = fuzz.trimf(self.oneri_puani.universe, [50, 100, 100])
        
        print("✅ Üyelik fonksiyonları tanımlandı")
        
    def kontrol_sistemi_olustur(self):
        """
        Bulanık kuralları tanımlar ve kontrol sistemini oluşturur
        """
        # Bulanık kurallar
        self.kural1 = ctrl.Rule(self.kategori_ilgisi['yuksek'] & self.onceki_satin_alma['yuksek'], 
                               self.oneri_puani['yuksek'])
        self.kural2 = ctrl.Rule(self.aylik_gelir['yuksek'] & self.kategori_ilgisi['orta'], 
                               self.oneri_puani['yuksek'])
        self.kural3 = ctrl.Rule(self.musteri_yasi['genc'] & self.kategori_ilgisi['yuksek'], 
                               self.oneri_puani['yuksek'])
        self.kural4 = ctrl.Rule(self.onceki_satin_alma['dusuk'] & self.kategori_ilgisi['dusuk'], 
                               self.oneri_puani['dusuk'])
        self.kural5 = ctrl.Rule(self.aylik_gelir['dusuk'] & self.onceki_satin_alma['dusuk'], 
                               self.oneri_puani['dusuk'])
        self.kural6 = ctrl.Rule(self.musteri_yasi['orta_yas'] & self.aylik_gelir['orta'], 
                               self.oneri_puani['orta'])
        self.kural7 = ctrl.Rule(self.kategori_ilgisi['orta'] & self.onceki_satin_alma['orta'], 
                               self.oneri_puani['orta'])
        
        # Kontrol sistemi oluşturma
        self.oneri_sistemi = ctrl.ControlSystem([self.kural1, self.kural2, self.kural3, 
                                                self.kural4, self.kural5, self.kural6, self.kural7])
        
        # Simülasyon objesi oluşturma
        self.simulasyon = ctrl.ControlSystemSimulation(self.oneri_sistemi)
        
        print("✅ Kontrol sistemi oluşturuldu")
        
    def uyelik_fonksiyonlari_gorsellestir(self):
        """
        Üyelik fonksiyonlarını görselleştirir
        """
        print("📊 Üyelik fonksiyonları görselleştiriliyor...")
        
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
        
        # Müşteri yaşı grafiği
        self.musteri_yasi.view(ax=axes[0, 0])
        axes[0, 0].set_title('Müşteri Yaşı', fontsize=12, fontweight='bold')
        axes[0, 0].set_xlabel('Yaş')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Aylık gelir grafiği
        self.aylik_gelir.view(ax=axes[0, 1])
        axes[0, 1].set_title('Aylık Gelir', fontsize=12, fontweight='bold')
        axes[0, 1].set_xlabel('Gelir (TL)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Önceki satın alma skoru grafiği
        self.onceki_satin_alma.view(ax=axes[0, 2])
        axes[0, 2].set_title('Önceki Satın Alma Skoru', fontsize=12, fontweight='bold')
        axes[0, 2].set_xlabel('Skor')
        axes[0, 2].grid(True, alpha=0.3)
        
        # Kategori ilgisi grafiği
        self.kategori_ilgisi.view(ax=axes[1, 0])
        axes[1, 0].set_title('Kategori İlgisi', fontsize=12, fontweight='bold')
        axes[1, 0].set_xlabel('İlgi Puanı')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Öneri puanı grafiği
        self.oneri_puani.view(ax=axes[1, 1])
        axes[1, 1].set_title('Öneri Puanı', fontsize=12, fontweight='bold')
        axes[1, 1].set_xlabel('Puan')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Boş eksenin kaldırılması
        axes[1, 2].axis('off')
        
        plt.tight_layout()
        plt.show()
        
    def oneri_hesapla(self, yas, gelir, onceki_skor, kategori_ilgi):
        """
        Verilen parametreler için öneri puanı hesaplar
        """
        try:
            # Giriş değerlerini sisteme verme
            self.simulasyon.input['musteri_yasi'] = yas
            self.simulasyon.input['aylik_gelir'] = gelir
            self.simulasyon.input['onceki_satin_alma'] = onceki_skor
            self.simulasyon.input['kategori_ilgisi'] = kategori_ilgi
            
            # Hesaplama
            self.simulasyon.compute()
            
            return self.simulasyon.output['oneri_puani']
        except Exception as e:
            print(f"❌ Hesaplama hatası: {e}")
            return 0
    
    def ornek_musterileri_test_et(self):
        """
        Örnek müşteri profilleri için test yapar
        """
        print("\n🧪 Örnek müşteri profilleri test ediliyor...")
        print("=" * 60)
        
        # Örnek müşteri profilleri
        musteriler = [
            {
                'ad': '👨‍💻 Genç Teknoloji Meraklısı',
                'yas': 25,
                'gelir': 6000,
                'onceki_skor': 80,
                'kategori_ilgi': 95
            },
            {
                'ad': '👔 Orta Yaş Profesyonel',
                'yas': 40,
                'gelir': 12000,
                'onceki_skor': 60,
                'kategori_ilgi': 70
            },
            {
                'ad': '💰 Düşük Gelirli Müşteri',
                'yas': 35,
                'gelir': 3000,
                'onceki_skor': 20,
                'kategori_ilgi': 30
            },
            {
                'ad': '🌟 Yüksek Gelirli Yeni Müşteri',
                'yas': 45,
                'gelir': 14000,
                'onceki_skor': 10,
                'kategori_ilgi': 85
            }
        ]
        
        # Her müşteri için öneri puanı hesaplama
        for i, musteri in enumerate(musteriler, 1):
            oneri_puani = self.oneri_hesapla(
                musteri['yas'], 
                musteri['gelir'],
                musteri['onceki_skor'], 
                musteri['kategori_ilgi']
            )
            
            print(f"\n{i}. {musteri['ad']}:")
            print(f"   📊 Yaş: {musteri['yas']}, Gelir: {musteri['gelir']:,} TL")
            print(f"   📈 Önceki Skor: {musteri['onceki_skor']}, Kategori İlgisi: {musteri['kategori_ilgi']}")
            print(f"   🎯 Öneri Puanı: {oneri_puani:.2f}")
            
            # Öneri seviyesi belirleme
            if oneri_puani >= 70:
                print(f"   ✅ Yüksek öncelik - Güçlü öneri yapın!")
            elif oneri_puani >= 40:
                print(f"   ⚠️ Orta öncelik - Koşullu öneri yapın")
            else:
                print(f"   ❌ Düşük öncelik - Öneri yapmayın")
        
        return musteriler
    
    def farkli_senaryolar_test_et(self):
        """
        Sistemin farklı senaryolar altında nasıl davrandığını test eder
        """
        print("\n🔬 Farklı senaryolar test ediliyor...")
        print("=" * 60)
        
        senaryolar = [
            {
                'ad': '🎯 Yüksek Sadakat - Düşük İlgi',
                'yas': 30, 'gelir': 8000, 'onceki': 90, 'kategori': 20
            },
            {
                'ad': '🏃‍♂️ Genç - Fakir - Yüksek İlgi',
                'yas': 22, 'gelir': 2500, 'onceki': 10, 'kategori': 95
            },
            {
                'ad': '👴 Yaşlı - Zengin - Orta İlgi',
                'yas': 55, 'gelir': 13000, 'onceki': 40, 'kategori': 50
            },
            {
                'ad': '⚖️ Dengeli Müşteri',
                'yas': 40, 'gelir': 7000, 'onceki': 60, 'kategori': 60
            }
        ]
        
        for i, senaryo in enumerate(senaryolar, 1):
            oneri_puani = self.oneri_hesapla(
                senaryo['yas'], 
                senaryo['gelir'],
                senaryo['onceki'], 
                senaryo['kategori']
            )
            
            print(f"\n{i}. {senaryo['ad']}:")
            print(f"   📊 Yaş: {senaryo['yas']}, Gelir: {senaryo['gelir']:,} TL")
            print(f"   📈 Önceki: {senaryo['onceki']}, Kategori: {senaryo['kategori']}")
            print(f"   🎯 Öneri Puanı: {oneri_puani:.2f}")
    
    def sonuc_gorsellestir(self, musteri_bilgi):
        """
        Belirli bir müşteri için sonucu görselleştirir
        """
        print(f"\n📊 {musteri_bilgi['ad']} için sonuç görselleştiriliyor...")
        
        # Öneri puanını hesapla
        oneri_puani = self.oneri_hesapla(
            musteri_bilgi['yas'],
            musteri_bilgi['gelir'],
            musteri_bilgi['onceki_skor'],
            musteri_bilgi['kategori_ilgi']
        )
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Müşteri profili grafiği
        kategoriler = ['Yaş\n(18-80)', 'Gelir\n(K TL)', 'Önceki\nSkor', 'Kategori\nİlgisi']
        degerler = [
            musteri_bilgi['yas'],
            musteri_bilgi['gelir'] / 1000,  # Bin TL cinsinden
            musteri_bilgi['onceki_skor'],
            musteri_bilgi['kategori_ilgi']
        ]
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        bars = ax1.bar(kategoriler, degerler, color=colors, alpha=0.7, edgecolor='black')
        
        ax1.set_title(f'{musteri_bilgi["ad"]} - Müşteri Profili', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Değer', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # Değerleri barların üstüne yazma
        for i, (bar, deger) in enumerate(zip(bars, degerler)):
            if i == 1:  # Gelir için
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                        f'{deger:.1f}K', ha='center', va='bottom', fontweight='bold')
            else:
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                        f'{deger:.0f}', ha='center', va='bottom', fontweight='bold')
        
        # Öneri puanı grafiği
        self.oneri_puani.view(sim=self.simulasyon, ax=ax2)
        ax2.set_title(f'Öneri Puanı: {oneri_puani:.2f}', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        return oneri_puani

class EticaretUygulamasi:
    """
    Gerçek e-ticaret uygulaması için örnek sınıf
    """
    
    def __init__(self):
        self.oneri_sistemi = EticaretBulanikOneriSistemi()
        self.urun_katalog = self.ornek_urun_katalog_olustur()
        
    def ornek_urun_katalog_olustur(self):
        return [
            {'id': 1, 'ad': 'iPhone 15 Pro', 'kategori': 'smartphone', 'fiyat': 45000},
            {'id': 2, 'ad': 'Samsung Galaxy S24', 'kategori': 'smartphone', 'fiyat': 35000},
            {'id': 3, 'ad': 'MacBook Pro', 'kategori': 'laptop', 'fiyat': 65000},
            {'id': 4, 'ad': 'Dell XPS 13', 'kategori': 'laptop', 'fiyat': 25000},
            {'id': 5, 'ad': 'iPad Pro', 'kategori': 'tablet', 'fiyat': 20000},
            {'id': 6, 'ad': 'Sony WH-1000XM5', 'kategori': 'kulaklık', 'fiyat': 8000},
            {'id': 7, 'ad': 'Apple Watch Series 9', 'kategori': 'akıllı_saat', 'fiyat': 12000},
            {'id': 8, 'ad': 'AirPods Pro', 'kategori': 'kulaklık', 'fiyat': 6000}
        ]
    
    def musteri_icin_oneri_getir(self, musteri_profil, kategori_filter=None):
        """
        Müşteri profili için ürün önerilerini getirir
        """
        print(f"\n🛍️ {musteri_profil['ad']} için ürün önerileri getiriliyor...")
        
        urun_onerileri = []
        
        # Kategori bazlı ilgi puanları (gerçek uygulamada ML ile hesaplanır)
        kategori_ilgi_puanlari = {
            'smartphone': 85,
            'laptop': 70,
            'tablet': 60,
            'kulaklık': 75,
            'akıllı_saat': 55
        }
        
        # Her ürün için öneri puanı hesapla
        for urun in self.urun_katalog:
            if kategori_filter and urun['kategori'] != kategori_filter:
                continue
                
            kategori_ilgi = kategori_ilgi_puanlari.get(urun['kategori'], 50)
            
            oneri_puani = self.oneri_sistemi.oneri_hesapla(
                musteri_profil['yas'],
                musteri_profil['gelir'],
                musteri_profil['onceki_skor'],
                kategori_ilgi
            )
            
            urun_onerileri.append({
                'urun': urun,
                'oneri_puani': oneri_puani,
                'kategori_ilgi': kategori_ilgi
            })
        
        # Puanlara göre sırala
        urun_onerileri.sort(key=lambda x: x['oneri_puani'], reverse=True)
        
        return urun_onerileri
    
    def oneri_raporu_goster(self, musteri_profil, top_n=5):
        """
        Müşteri için öneri raporunu gösterir
        """
        oneriler = self.musteri_icin_oneri_getir(musteri_profil)
        
        print(f"\n📋 {musteri_profil['ad']} için TOP {top_n} Öneri:")
        print("=" * 80)
        
        for i, oneri in enumerate(oneriler[:top_n], 1):
            urun = oneri['urun']
            puan = oneri['oneri_puani']
            
            # Öneri seviyesi ikonu
            if puan >= 70:
                ikon = "🔥"
                seviye = "Güçlü Öneri"
            elif puan >= 50:
                ikon = "⭐"
                seviye = "Orta Öneri"
            else:
                ikon = "💡"
                seviye = "Zayıf Öneri"
            
            print(f"{i}. {ikon} {urun['ad']}")
            print(f"   💰 Fiyat: {urun['fiyat']:,} TL")
            print(f"   📱 Kategori: {urun['kategori']}")
            print(f"   🎯 Öneri Puanı: {puan:.2f} ({seviye})")
            print(f"   📊 Kategori İlgisi: {oneri['kategori_ilgi']}")
            print()

def main():
    """
    Ana fonksiyon - Sistem demonstrasyonu
    """
    print("🚀 E-Ticaret Bulanık Mantık Öneri Sistemi")
    print("=" * 50)
    
    # Sistem oluştur
    sistem = EticaretBulanikOneriSistemi()
    
    # Üyelik fonksiyonlarını göster
    sistem.uyelik_fonksiyonlari_gorsellestir()
    
    # Örnek müşterileri test et
    ornek_musteriler = sistem.ornek_musterileri_test_et()
    
    # Farklı senaryoları test et
    sistem.farkli_senaryolar_test_et()
    
    # İlk müşteri için detaylı görselleştirme
    sistem.sonuc_gorsellestir(ornek_musteriler[0])
    
    # E-ticaret uygulaması örneği
    print("\n🛒 E-Ticaret Uygulaması Örneği")
    print("=" * 50)
    
    eticaret = EticaretUygulamasi()
    
    # Örnek müşteri için ürün önerileri
    eticaret.oneri_raporu_goster(ornek_musteriler[0])
    eticaret.oneri_raporu_goster(ornek_musteriler[1])
    
    print("\n✅ Sistem demonstrasyonu tamamlandı!")
    print("💡 Kendi müşteri profillerinizi test etmek için sistem.oneri_hesapla() fonksiyonunu kullanabilirsiniz.")

if __name__ == "__main__":
    main()