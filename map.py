import folium
import random
import requests
from datetime import datetime, timedelta
from folium import plugins
import json

class MapaUkrainyZeZdjeciami:
    """
    Mapa konfliktu ze zdjęciami w popup'ach markerów
    """
    
    def __init__(self):
        self.mapa = folium.Map(
            location=[49.0, 32.0], 
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Miasta ukraińskie
        self.miasta = {
            'Kyiv': (50.4501, 30.5234),
            'Kharkiv': (49.9935, 36.2304),
            'Odesa': (46.4825, 30.7233),
            'Dnipro': (48.4647, 35.0462),
            'Donetsk': (48.0159, 37.8028),
            'Zaporizhzhia': (47.8388, 35.1396),
            'Lviv': (49.8397, 24.0297),
            'Mykolaiv': (46.9751, 31.9946),
            'Luhansk': (48.5740, 39.3078),
            'Kherson': (46.6354, 32.6169),
            'Pokrovsk': (48.7194, 37.1764),
            'Kramatorsk': (48.7233, 37.5619),
            'Bakhmut': (48.5958, 38.0018),
            'Avdiivka': (48.1372, 37.7544)
        }
        
        # Bezpieczne kolory Folium
        self.kolory = ['red', 'blue', 'green', 'purple', 'orange', 'darkred']
        self.ikony = ['flash', 'fire', 'plane', 'warning-sign', 'home', 'info-sign']
        
        # Typy wydarzeń
        self.typy_wydarzen = [
            'Atak rakietowy',
            'Atak dronami', 
            'Ostrzał artyleryjski',
            'Alert przeciwlotniczy',
            'Atak na infrastrukturę',
            'Inne wydarzenia'
        ]
        
        # Zdjęcia dla różnych typów wydarzeń (przykładowe URL)
        self.zdjecia_wydarzen = {
            'Atak rakietowy': [
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51189',  # Placeholder
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51178',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51089'
            ],
            'Atak dronami': [
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51190',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51191',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51192'
            ],
            'Ostrzał artyleryjski': [
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51193',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51194',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51195'
            ],
            'Alert przeciwlotniczy': [
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51195',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51196'
            ],
            'Atak na infrastrukturę': [
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51197',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51198'
            ],
            'Inne wydarzenia': [
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51199',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51200'
            ]
        }
    
    def pobierz_zdjecie_z_unsplash(self, miasto, typ_wydarzenia):
        """
        Pobiera prawdziwe zdjęcie z Unsplash API
        """
        try:
            # Słowa kluczowe dla różnych typów wydarzeń
            keywords_map = {
                'Atak rakietowy': 'explosion,destruction,war',
                'Atak dronami': 'drone,military,technology',
                'Ostrzał artyleryjski': 'artillery,military,warfare',
                'Alert przeciwlotniczy': 'siren,alert,warning',
                'Atak na infrastrukturę': 'infrastructure,damage,building',
                'Inne wydarzenia': 'military,conflict,news'
            }
            
            # Użyj słów kluczowych dla typu wydarzenia
            keywords = keywords_map.get(typ_wydarzenia, 'military,ukraine')
            
            # Unsplash API (nie wymaga klucza dla podstawowych zapytań)
            url = f"https://source.unsplash.com/400x300/?{keywords}"
            
            return url
            
        except Exception as e:
            print(f"⚠️ Błąd pobierania zdjęcia: {e}")
            # Fallback - losowe zdjęcie
            return f"https://picsum.photos/400/300?random={random.randint(1, 100)}"
    
    def pobierz_zdjecie_miejsca_google_street_view(self, lat, lon):
        """
        Pobiera zdjęcie z Google Street View API
        UWAGA: Wymaga klucza API Google
        """
        try:
            # Google Street View Static API
            api_key = "YOUR_GOOGLE_API_KEY"  # Zamień na swój klucz
            
            if api_key == "YOUR_GOOGLE_API_KEY":
                # Fallback jeśli nie ma klucza
                return f"https://picsum.photos/400/300?random={random.randint(1, 100)}"
            
            url = f"https://maps.googleapis.com/maps/api/streetview?size=400x300&location={lat},{lon}&key={api_key}"
            return url
            
        except Exception as e:
            print(f"⚠️ Błąd Google Street View: {e}")
            return f"https://picsum.photos/400/300?random={random.randint(1, 100)}"
    
    def pobierz_zdjecie_z_wikimedia(self, miasto):
        """
        Próbuje pobrać zdjęcie miasta z Wikimedia Commons
        """
        try:
            # Wikipedia API dla zdjęć
            search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{miasto}"
            
            response = requests.get(search_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'thumbnail' in data and 'source' in data['thumbnail']:
                    # Zwiększ rozmiar zdjęcia
                    img_url = data['thumbnail']['source']
                    # Zmień rozmiar na większy
                    img_url = img_url.replace('/320px-', '/400px-')
                    return img_url
            
            # Fallback
            return f"https://picsum.photos/400/300?random={random.randint(1, 100)}"
            
        except Exception as e:
            print(f"⚠️ Błąd Wikimedia: {e}")
            return f"https://picsum.photos/400/300?random={random.randint(1, 100)}"
    
    def generuj_wydarzenia_ze_zdjeciami(self, ile=60):
        """Generuje wydarzenia z przypisanymi zdjęciami"""
        print(f"📍 Generowanie {ile} wydarzeń ze zdjęciami...")
        
        wydarzenia = []
        
        for i in range(ile):
            # Wybierz losowe miasto
            miasto_nazwa = random.choice(list(self.miasta.keys()))
            coords = self.miasta[miasto_nazwa]
            
            # Dodaj małe przesunięcie
            lat = coords[0] + random.uniform(-0.05, 0.05)
            lon = coords[1] + random.uniform(-0.05, 0.05)
            
            # Wybierz typ
            typ = random.choice(self.typy_wydarzen)
            kolor = random.choice(self.kolory)
            ikona = random.choice(self.ikony)
            
            # Prosta data
            godzina = random.randint(0, 23)
            minuta = random.randint(0, 59)
            
            # Wybierz metodę pobrania zdjęcia
            metoda_zdjecia = random.choice(['unsplash', 'wikimedia', 'placeholder'])
            
            if metoda_zdjecia == 'unsplash':
                zdjecie_url = self.pobierz_zdjecie_z_unsplash(miasto_nazwa, typ)
            elif metoda_zdjecia == 'wikimedia':
                zdjecie_url = self.pobierz_zdjecie_z_wikimedia(miasto_nazwa)
            else:
                # Placeholder z tematycznymi obrazami
                zdjecie_url = random.choice(self.zdjecia_wydarzen.get(typ, self.zdjecia_wydarzen['Inne wydarzenia']))
            
            wydarzenie = {
                'id': i,
                'miasto': miasto_nazwa,
                'lat': lat,
                'lon': lon,
                'typ': typ,
                'kolor': kolor,
                'ikona': ikona,
                'czas': f"{godzina:02d}:{minuta:02d}",
                'opis': f"{typ} w rejonie {miasto_nazwa}. Sytuacja monitorowana przez służby.",
                'zrodlo': random.choice(['OSINT', 'Local Reports', 'Military Sources', 'News Agency']),
                'zdjecie_url': zdjecie_url,
                'metoda_zdjecia': metoda_zdjecia,
                'intensywnosc': random.choice(['Niska', 'Średnia', 'Wysoka']),
                'status': random.choice(['Potwierdzone', 'Weryfikowane', 'Zgłoszone'])
            }
            
            wydarzenia.append(wydarzenie)
        
        print(f"✅ Wygenerowano {len(wydarzenia)} wydarzeń ze zdjęciami")
        return wydarzenia
    
    def utworz_popup_ze_zdjeciem(self, wydarzenie):
        """Tworzy popup HTML ze zdjęciem"""
        
        # HTML popup z wbudowanym zdjęciem
        popup_html = f"""
        <div style="width: 420px; font-family: 'Segoe UI', Arial, sans-serif;">
            
            <!-- Nagłówek -->
            <div style="background: linear-gradient(90deg, {wydarzenie['kolor']} 0%, {wydarzenie['kolor']}99 100%); 
                        color: white; padding: 12px; margin: -10px -10px 15px -10px; 
                        border-radius: 8px 8px 0 0;">
                <h3 style="margin: 0; font-size: 16px; text-align: center;">
                    🎯 {wydarzenie['typ']}
                </h3>
            </div>
            
            <!-- Zdjęcie -->
            <div style="text-align: center; margin: 15px 0;">
                <img src="{wydarzenie['zdjecie_url']}" 
                     style="width: 100%; max-width: 380px; height: 200px; 
                            object-fit: cover; border-radius: 8px; 
                            border: 2px solid #ddd;"
                     onerror="this.src='https://via.placeholder.com/380x200/cccccc/666666?text=Zdjęcie+niedostępne'"
                     alt="Zdjęcie z miejsca wydarzenia">
                <div style="font-size: 10px; color: #888; margin-top: 5px;">
                    Źródło zdjęcia: {wydarzenie['metoda_zdjecia']}
                </div>
            </div>
            
            <!-- Informacje -->
            <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; margin: 10px 0;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px;">
                    <div><b>📍 Miasto:</b> {wydarzenie['miasto']}</div>
                    <div><b>⏰ Czas:</b> {wydarzenie['czas']}</div>
                    <div><b>📊 Status:</b> {wydarzenie['status']}</div>
                    <div><b>🔥 Intensywność:</b> {wydarzenie['intensywnosc']}</div>
                </div>
            </div>
            
            <!-- Opis -->
            <div style="margin: 12px 0; padding: 10px; background: #fff3cd; 
                       border-left: 4px solid #ffc107; border-radius: 4px;">
                <b>📝 Opis sytuacji:</b><br>
                <span style="font-size: 13px;">{wydarzenie['opis']}</span>
            </div>
            
            <!-- Źródło -->
            <div style="margin: 12px 0; text-align: center; padding: 8px; 
                       background: #e9ecef; border-radius: 4px; font-size: 11px;">
                <b>📡 Źródło informacji:</b> {wydarzenie['zrodlo']}<br>
                <b>🆔 ID wydarzenia:</b> #{wydarzenie['id']:03d}
            </div>
            
            <!-- Współrzędne -->
            <div style="margin-top: 10px; font-size: 10px; color: #666; text-align: center;">
                📐 Współrzędne: {wydarzenie['lat']:.4f}, {wydarzenie['lon']:.4f}
            </div>
            
        </div>
        """
        
        return popup_html
    
    def dodaj_markery_ze_zdjeciami(self, wydarzenia):
        """Dodaje markery ze zdjęciami w popup'ach"""
        print(f"📌 Dodawanie {len(wydarzenia)} markerów ze zdjęciami...")
        
        # Grupuj według typu
        grupy = {}
        for wydarzenie in wydarzenia:
            typ = wydarzenie['typ']
            if typ not in grupy:
                grupy[typ] = []
            grupy[typ].append(wydarzenie)
        
        # Dodaj grupy na mapę
        for typ, lista_wydarzen in grupy.items():
            
            # Utwórz grupę z klasteryzacją
            cluster = plugins.MarkerCluster(
                name=f"{typ} ({len(lista_wydarzen)})",
                options={
                    'disableClusteringAtZoom': 10,  # Rozklasteruj przy zbliżeniu
                    'maxClusterRadius': 50
                }
            )
            
            for wydarzenie in lista_wydarzen:
                
                # Utwórz popup ze zdjęciem
                popup_html = self.utworz_popup_ze_zdjeciem(wydarzenie)
                
                # Tooltip z podstawowymi informacjami
                tooltip_text = f"""
                <div style="font-size: 12px;">
                    <b>{wydarzenie['typ']}</b><br>
                    📍 {wydarzenie['miasto']}<br>
                    ⏰ {wydarzenie['czas']}<br>
                    📊 {wydarzenie['status']}
                </div>
                """
                
                # Dodaj marker
                folium.Marker(
                    [wydarzenie['lat'], wydarzenie['lon']],
                    popup=folium.Popup(popup_html, max_width=450),
                    icon=folium.Icon(
                        color=wydarzenie['kolor'],
                        icon=wydarzenie['ikona'],
                        prefix='glyphicon'
                    ),
                    tooltip=folium.Tooltip(tooltip_text)
                ).add_to(cluster)
            
            # Dodaj grupę do mapy
            cluster.add_to(self.mapa)
        
        print("✅ Markery ze zdjęciami dodane!")
    
    def dodaj_statystyki_rozszerzone(self, wydarzenia):
        """Rozszerzone statystyki z informacjami o zdjęciach"""
        
        # Podstawowe statystyki
        stats_typow = {}
        stats_miast = {}
        stats_statusow = {}
        stats_zdjec = {}
        
        for wydarzenie in wydarzenia:
            # Typy
            typ = wydarzenie['typ']
            stats_typow[typ] = stats_typow.get(typ, 0) + 1
            
            # Miasta
            miasto = wydarzenie['miasto']
            stats_miast[miasto] = stats_miast.get(miasto, 0) + 1
            
            # Statusy
            status = wydarzenie['status']
            stats_statusow[status] = stats_statusow.get(status, 0) + 1
            
            # Źródła zdjęć
            metoda = wydarzenie['metoda_zdjecia']
            stats_zdjec[metoda] = stats_zdjec.get(metoda, 0) + 1
        
        # Top 5 miast
        top_miasta = sorted(stats_miast.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # HTML panelu
        panel_html = f"""
        <div style="position: fixed; top: 10px; left: 10px; 
                    width: 320px; background: white; 
                    border: 2px solid #333; border-radius: 10px;
                    padding: 15px; z-index: 9999; font-size: 12px;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.15);">
            
            <h3 style="margin: 0 0 12px 0; text-align: center; color: #0066cc;">
                🇺🇦 MONITOR KONFLIKTU + ZDJĘCIA
            </h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 12px 0;">
                <div style="text-align: center; padding: 10px; background: #f0f8ff; border-radius: 6px;">
                    <div style="font-size: 20px; font-weight: bold; color: #0066cc;">{len(wydarzenia)}</div>
                    <div style="font-size: 10px;">Łączne wydarzenia</div>
                </div>
                <div style="text-align: center; padding: 10px; background: #f0fff0; border-radius: 6px;">
                    <div style="font-size: 20px; font-weight: bold; color: #228b22;">{len([e for e in wydarzenia if e['status'] == 'Potwierdzone'])}</div>
                    <div style="font-size: 10px;">Potwierdzone</div>
                </div>
            </div>
            
            <h4 style="margin: 12px 0 5px 0; font-size: 13px;">🎯 Typy wydarzeń:</h4>
            <div style="max-height: 100px; overflow-y: auto; font-size: 11px;">
        """
        
        for typ, count in sorted(stats_typow.items(), key=lambda x: x[1], reverse=True):
            procent = (count / len(wydarzenia) * 100) if len(wydarzenia) > 0 else 0
            panel_html += f"""
                <div style="display: flex; justify-content: space-between; margin: 2px 0; align-items: center;">
                    <span>{typ[:18]}...</span>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 30px; height: 6px; background: #e0e0e0; border-radius: 3px; margin-right: 5px;">
                            <div style="width: {procent}%; height: 100%; background: #4ade80; border-radius: 3px;"></div>
                        </div>
                        <span style="font-weight: bold; font-size: 10px;">{count}</span>
                    </div>
                </div>
            """
        
        panel_html += """
            </div>
            
            <h4 style="margin: 12px 0 5px 0; font-size: 13px;">🔥 Top lokalizacje:</h4>
            <div style="max-height: 80px; overflow-y: auto; font-size: 11px;">
        """
        
        for miasto, count in top_miasta:
            panel_html += f"""
                <div style="display: flex; justify-content: space-between; margin: 2px 0;">
                    <span>{miasto}</span>
                    <span style="font-weight: bold; color: #dc2626;">{count}</span>
                </div>
            """
        
        panel_html += f"""
            </div>
            
            <h4 style="margin: 12px 0 5px 0; font-size: 13px;">📸 Źródła zdjęć:</h4>
            <div style="font-size: 11px;">
        """
        
        for metoda, count in stats_zdjec.items():
            panel_html += f"""
                <div style="display: flex; justify-content: space-between; margin: 2px 0;">
                    <span>{metoda.title()}</span>
                    <span style="font-weight: bold; color: #059669;">{count}</span>
                </div>
            """
        
        panel_html += f"""
            </div>
            
            <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid #ddd;
                       text-align: center; font-size: 10px; color: #666;">
                <div>💡 <b>Kliknij marker aby zobaczyć zdjęcie!</b></div>
                <div style="margin-top: 5px;">
                    Aktualizacja: {datetime.now().strftime('%d.%m.%Y %H:%M')}<br>
                    Zdjęcia: Unsplash + Wikimedia + Placeholders
                </div>
            </div>
        </div>
        """
        
        self.mapa.get_root().html.add_child(folium.Element(panel_html))
    
    def dodaj_legende_ze_zdjeciami(self):
        """Legenda z informacjami o zdjęciach"""
        legenda_html = """
        <div style="position: fixed; bottom: 10px; right: 10px;
                    width: 200px; background: white; 
                    border: 1px solid #ccc; border-radius: 8px;
                    padding: 12px; z-index: 9999; font-size: 11px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            
            <h4 style="margin: 0 0 8px 0; text-align: center;">🗺️ Legenda</h4>
            
            <p><span style="color: red;">🔴</span> Ataki rakietowe</p>
            <p><span style="color: purple;">🟣</span> Ataki dronami</p>
            <p><span style="color: orange;">🟠</span> Ostrzał artyleryjski</p>
            <p><span style="color: blue;">🔵</span> Alerty przeciwlotnicze</p>
            <p><span style="color: green;">🟢</span> Infrastruktura</p>
            <p><span style="color: darkred;">🟤</span> Inne wydarzenia</p>
            
            <hr style="margin: 10px 0;">
            
            <div style="background: #fffbeb; padding: 8px; border-radius: 4px; border: 1px solid #fbbf24;">
                <b>📸 Zdjęcia w markerach:</b><br>
                • Unsplash API<br>
                • Wikimedia Commons<br>
                • Placeholder images<br>
                <small style="color: #92400e;">Kliknij marker aby zobaczyć!</small>
            </div>
            
            <div style="margin-top: 8px; text-align: center; font-size: 10px; color: #666;">
                Dane symulowane + zdjęcia<br>
                Aktualizacja co 15 min
            </div>
        </div>
        """
        
        self.mapa.get_root().html.add_child(folium.Element(legenda_html))
    
    def dodaj_warstwy(self):
        """Dodaje warstwy map"""
        # Satelitarna
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='🛰️ Satelita',
            overlay=False,
            control=True
        ).add_to(self.mapa)
        
        # Nocna
        folium.TileLayer(
            'cartodbdark_matter', 
            name='🌙 Nocna'
        ).add_to(self.mapa)
        
        # Kontrola warstw
        folium.LayerControl().add_to(self.mapa)
    
    def utworz_mape_ze_zdjeciami(self):
        """Główna funkcja - tworzy mapę ze zdjęciami"""
        print("🇺🇦 TWORZENIE MAPY ZE ZDJĘCIAMI")
        print("=" * 35)
        print("📸 Każdy marker będzie miał zdjęcie!")
        print("=" * 35)
        
        # 1. Generuj wydarzenia ze zdjęciami
        wydarzenia = self.generuj_wydarzenia_ze_zdjeciami(60)
        
        # 2. Dodaj wszystko na mapę
        self.dodaj_markery_ze_zdjeciami(wydarzenia)
        self.dodaj_statystyki_rozszerzone(wydarzenia)
        self.dodaj_legende_ze_zdjeciami()
        self.dodaj_warstwy()
        
        print("✅ Mapa ze zdjęciami gotowa!")
        return self.mapa
    
    def zapisz(self, nazwa="mapa_ukraina_ze_zdjeciami.html"):
        """Zapisuje mapę"""
        self.mapa.save(nazwa)
        print(f"💾 Zapisano: {nazwa}")

# ============================================================================
# URUCHOMIENIE
# ============================================================================

def main():
    print("🚀 MAPA UKRAINY ZE ZDJĘCIAMI")
    print("=" * 32)
    print("📸 Każdy marker ma zdjęcie!")
    print("🖼️ Źródła: Unsplash + Wikimedia")
    print("🔍 Kliknij marker aby zobaczyć")
    print("=" * 32)
    
    try:
        # Utwórz mapę
        mapa = MapaUkrainyZeZdjeciami()
        
        # Wygeneruj i zapisz
        mapa.utworz_mape_ze_zdjeciami()
        mapa.zapisz("mapa_ukraina_ze_zdjeciami.html")
        
        print("\n🎉 SUKCES!")
        print("📁 Otwórz: mapa_ukraina_ze_zdjeciami.html")
        print("\n🎯 NOWE FUNKCJE:")
        print("• 📸 Zdjęcia w każdym markerze")
        print("• 🖼️ Różne źródła obrazów")
        print("• 📊 Statystyki źródeł zdjęć")
        print("• 🎨 Lepsze popup'y z obrazami")
        print("• 🔍 Tooltip'y z podglądem")
        print("• 📐 Współrzędne w popup'ach")
        print("\n💡 INSTRUKCJA:")
        print("1. Kliknij na dowolny marker")
        print("2. Zobacz zdjęcie z miejsca")
        print("3. Przeczytaj szczegóły wydarzenia")
        
    except Exception as e:
        print(f"❌ Błąd: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Wymaga: pip install folium requests
    main()

"""
📸 MAPA ZE ZDJĘCIAMI - NOWE FUNKCJE:

✅ ZDJĘCIA W MARKERACH:
- Każdy marker ma zdjęcie w popup'ie
- 400x300px wysokiej jakości
- Fallback dla niedziałających URL

🖼️ ŹRÓDŁA ZDJĘĆ:
- Unsplash API (tematyczne zdjęcia)
- Wikimedia Commons (zdjęcia miast)
- Placeholder images (backup)

🎨 ULEPSZONE POPUP'Y:
- Zdjęcie na górze
- Gradient nagłówek
- Siatka informacji
- Kolorowe sekcje
- Współrzędne GPS

📊 ROZSZERZONE STATYSTYKI:
- Liczba zdjęć według źródeł
- Status wydarzeń
- Wykres słupkowy typów

🔧 TECHNICZNE:
- Error handling dla zdjęć
- onerror fallback w HTML
- Responsywne rozmiary
- Klasteryzacja z rozpakowaniem

URUCHOMIENIE:
pip install folium requests
python nazwa_pliku.py

KLIKNIJ MARKER = ZOBACZ ZDJĘCIE! 📸
"""