import folium
import random
import requests
from datetime import datetime, timedelta
from folium import plugins
import json

class UkraineMapWithImages:
    """
    Conflict map with images in marker popups
    """
    
    def __init__(self):
        self.map = folium.Map(
            location=[49.0, 32.0], 
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Ukrainian cities
        self.cities = {
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
        
        # Safe Folium colors
        self.colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred']
        self.icons = ['flash', 'fire', 'plane', 'warning-sign', 'home', 'info-sign']
        
        # Event types
        self.event_types = [
            'Missile strike',
            'Drone attack', 
            'Artillery shelling',
            'Air raid alert',
            'Infrastructure attack',
            'Other events'
        ]
        
        # Images for different event types (example URLs)
        self.event_images = {
            'Missile strike': [
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51189',  # Placeholder
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51178',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51089'
            ],
            'Drone attack': [
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51190',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51191',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51192'
            ],
            'Artillery shelling': [
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51193',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51194',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51195'
            ],
            'Air raid alert': [
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51195',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51196'
            ],
            'Infrastructure attack': [
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51197',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51198'
            ],
            'Other events': [
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51199',
                'https://war.ukraine.ua/imagebank-category/infrustrucure-destruction/?photo=51200'
            ]
        }
    
    def get_local_image(self, city, event_type):
        """
        Gets local image from Pics folder
        """
        try:
            import os
            
            # Check if Pics folder exists
            pics_folder = "Pics"
            if not os.path.exists(pics_folder):
                print(f"⚠️ Pics folder not found, creating it...")
                os.makedirs(pics_folder)
                return f"https://picsum.photos/400/300?random={random.randint(1, 100)}"
            
            # Get list of available images (1.jpg to 10.jpg)
            available_images = []
            for i in range(1, 11):  # 1 to 10
                image_path = os.path.join(pics_folder, f"{i}.jpg")
                if os.path.exists(image_path):
                    available_images.append(f"{i}.jpg")
            
            if not available_images:
                print(f"⚠️ No images found in Pics folder")
                return f"https://picsum.photos/400/300?random={random.randint(1, 100)}"
            
            # Select random image from available ones
            selected_image = random.choice(available_images)
            image_path = os.path.join(pics_folder, selected_image)
            
            # Convert backslashes to forward slashes for web compatibility
            web_path = image_path.replace('\\', '/')
            
            print(f"📸 Using local image: {web_path}")
            return web_path
            
        except Exception as e:
            print(f"⚠️ Error getting local image: {e}")
            # Fallback - random image
            return f"https://picsum.photos/400/300?random={random.randint(1, 100)}"
    
    def get_google_street_view_image(self, lat, lon):
        """
        Gets image from Google Street View API (DISABLED - using local images)
        WARNING: Requires Google API key
        """
        # Always return local image instead
        return self.get_local_image("", "")
    
    def get_image_from_wikimedia(self, city):
        """
        Gets city image from Wikimedia Commons (DISABLED - using local images)
        """
        # Always return local image instead
        return self.get_local_image(city, "")
    
    def generate_events_with_images(self, count=60):
        """Generates events with assigned images"""
        print(f"📍 Generating {count} events with images...")
        
        events = []
        
        for i in range(count):
            # Choose random city
            city_name = random.choice(list(self.cities.keys()))
            coords = self.cities[city_name]
            
            # Add small offset
            lat = coords[0] + random.uniform(-0.05, 0.05)
            lon = coords[1] + random.uniform(-0.05, 0.05)
            
            # Choose type
            event_type = random.choice(self.event_types)
            color = random.choice(self.colors)
            icon = random.choice(self.icons)
            
            # Simple time
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            
            # Choose image retrieval method - now always uses local images
            image_method = 'local'
            image_url = self.get_local_image(city_name, event_type)
            
            event = {
                'id': i,
                'city': city_name,
                'lat': lat,
                'lon': lon,
                'type': event_type,
                'color': color,
                'icon': icon,
                'time': f"{hour:02d}:{minute:02d}",
                'description': f"{event_type} in {city_name} area. Situation monitored by services.",
                'source': random.choice(['OSINT', 'Local Reports', 'Military Sources', 'News Agency']),
                'image_url': image_url,
                'image_method': image_method,
                'intensity': random.choice(['Low', 'Medium', 'High']),
                'status': random.choice(['Confirmed', 'Verifying', 'Reported'])
            }
            
            events.append(event)
        
        print(f"✅ Generated {len(events)} events with images")
        return events
    
    def create_popup_with_image(self, event):
        """Creates HTML popup with image"""
        
        # HTML popup with embedded image
        popup_html = f"""
        <div style="width: 420px; font-family: 'Segoe UI', Arial, sans-serif;">
            
            <!-- Header -->
            <div style="background: linear-gradient(90deg, {event['color']} 0%, {event['color']}99 100%); 
                        color: white; padding: 12px; margin: -10px -10px 15px -10px; 
                        border-radius: 8px 8px 0 0;">
                <h3 style="margin: 0; font-size: 16px; text-align: center;">
                    🎯 {event['type']}
                </h3>
            </div>
            
            <!-- Image -->
            <div style="text-align: center; margin: 15px 0;">
                <img src="{event['image_url']}" 
                     style="width: 100%; max-width: 380px; height: 200px; 
                            object-fit: cover; border-radius: 8px; 
                            border: 2px solid #ddd;"
                     onerror="this.src='https://via.placeholder.com/380x200/cccccc/666666?text=Image+unavailable'"
                     alt="Image from event location">
                <div style="font-size: 10px; color: #888; margin-top: 5px;">
                    Image source: {event['image_method']}
                </div>
            </div>
            
            <!-- Information -->
            <div style="background: #f8f9fa; padding: 12px; border-radius: 6px; margin: 10px 0;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px;">
                    <div><b>📍 City:</b> {event['city']}</div>
                    <div><b>⏰ Time:</b> {event['time']}</div>
                    <div><b>📊 Status:</b> {event['status']}</div>
                    <div><b>🔥 Intensity:</b> {event['intensity']}</div>
                </div>
            </div>
            
            <!-- Description -->
            <div style="margin: 12px 0; padding: 10px; background: #fff3cd; 
                       border-left: 4px solid #ffc107; border-radius: 4px;">
                <b>📝 Situation description:</b><br>
                <span style="font-size: 13px;">{event['description']}</span>
            </div>
            
            <!-- Source -->
            <div style="margin: 12px 0; text-align: center; padding: 8px; 
                       background: #e9ecef; border-radius: 4px; font-size: 11px;">
                <b>📡 Information source:</b> {event['source']}<br>
                <b>🆔 Event ID:</b> #{event['id']:03d}
            </div>
            
            <!-- Coordinates -->
            <div style="margin-top: 10px; font-size: 10px; color: #666; text-align: center;">
                📐 Coordinates: {event['lat']:.4f}, {event['lon']:.4f}
            </div>
            
        </div>
        """
        
        return popup_html
    
    def add_markers_with_images(self, events):
        """Adds markers with images in popups"""
        print(f"📌 Adding {len(events)} markers with images...")
        
        # Group by type
        groups = {}
        for event in events:
            event_type = event['type']
            if event_type not in groups:
                groups[event_type] = []
            groups[event_type].append(event)
        
        # Add groups to map
        for event_type, event_list in groups.items():
            
            # Create group with clustering
            cluster = plugins.MarkerCluster(
                name=f"{event_type} ({len(event_list)})",
                options={
                    'disableClusteringAtZoom': 10,  # Uncluster when zoomed in
                    'maxClusterRadius': 50
                }
            )
            
            for event in event_list:
                
                # Create popup with image
                popup_html = self.create_popup_with_image(event)
                
                # Tooltip with basic information
                tooltip_text = f"""
                <div style="font-size: 12px;">
                    <b>{event['type']}</b><br>
                    📍 {event['city']}<br>
                    ⏰ {event['time']}<br>
                    📊 {event['status']}
                </div>
                """
                
                # Add marker
                folium.Marker(
                    [event['lat'], event['lon']],
                    popup=folium.Popup(popup_html, max_width=450),
                    icon=folium.Icon(
                        color=event['color'],
                        icon=event['icon'],
                        prefix='glyphicon'
                    ),
                    tooltip=folium.Tooltip(tooltip_text)
                ).add_to(cluster)
            
            # Add group to map
            cluster.add_to(self.map)
        
        print("✅ Markers with images added!")
    
    def add_extended_statistics(self, events):
        """Extended statistics with image information"""
        
        # Basic statistics
        type_stats = {}
        city_stats = {}
        status_stats = {}
        image_stats = {}
        
        for event in events:
            # Types
            event_type = event['type']
            type_stats[event_type] = type_stats.get(event_type, 0) + 1
            
            # Cities
            city = event['city']
            city_stats[city] = city_stats.get(city, 0) + 1
            
            # Status
            status = event['status']
            status_stats[status] = status_stats.get(status, 0) + 1
            
            # Image sources
            method = event['image_method']
            image_stats[method] = image_stats.get(method, 0) + 1
        
        # Top 5 cities
        top_cities = sorted(city_stats.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # HTML panel
        panel_html = f"""
        <div style="position: fixed; top: 10px; left: 10px; 
                    width: 320px; background: white; 
                    border: 2px solid #333; border-radius: 10px;
                    padding: 15px; z-index: 9999; font-size: 12px;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.15);">
            
            <h3 style="margin: 0 0 12px 0; text-align: center; color: #0066cc;">
                🇺🇦 CONFLICT MONITOR + IMAGES
            </h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 12px 0;">
                <div style="text-align: center; padding: 10px; background: #f0f8ff; border-radius: 6px;">
                    <div style="font-size: 20px; font-weight: bold; color: #0066cc;">{len(events)}</div>
                    <div style="font-size: 10px;">Total events</div>
                </div>
                <div style="text-align: center; padding: 10px; background: #f0fff0; border-radius: 6px;">
                    <div style="font-size: 20px; font-weight: bold; color: #228b22;">{len([e for e in events if e['status'] == 'Confirmed'])}</div>
                    <div style="font-size: 10px;">Confirmed</div>
                </div>
            </div>
            
            <h4 style="margin: 12px 0 5px 0; font-size: 13px;">🎯 Event types:</h4>
            <div style="max-height: 100px; overflow-y: auto; font-size: 11px;">
        """
        
        for event_type, count in sorted(type_stats.items(), key=lambda x: x[1], reverse=True):
            percent = (count / len(events) * 100) if len(events) > 0 else 0
            panel_html += f"""
                <div style="display: flex; justify-content: space-between; margin: 2px 0; align-items: center;">
                    <span>{event_type[:18]}...</span>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 30px; height: 6px; background: #e0e0e0; border-radius: 3px; margin-right: 5px;">
                            <div style="width: {percent}%; height: 100%; background: #4ade80; border-radius: 3px;"></div>
                        </div>
                        <span style="font-weight: bold; font-size: 10px;">{count}</span>
                    </div>
                </div>
            """
        
        panel_html += """
            </div>
            
            <h4 style="margin: 12px 0 5px 0; font-size: 13px;">🔥 Top locations:</h4>
            <div style="max-height: 80px; overflow-y: auto; font-size: 11px;">
        """
        
        for city, count in top_cities:
            panel_html += f"""
                <div style="display: flex; justify-content: space-between; margin: 2px 0;">
                    <span>{city}</span>
                    <span style="font-weight: bold; color: #dc2626;">{count}</span>
                </div>
            """
        
        panel_html += f"""
            </div>
            
            <h4 style="margin: 12px 0 5px 0; font-size: 13px;">📸 Image sources:</h4>
            <div style="font-size: 11px;">
        """
        
        for method, count in image_stats.items():
            panel_html += f"""
                <div style="display: flex; justify-content: space-between; margin: 2px 0;">
                    <span>{method.title()}</span>
                    <span style="font-weight: bold; color: #059669;">{count}</span>
                </div>
            """
        
        panel_html += f"""
            </div>
            
            <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid #ddd;
                       text-align: center; font-size: 10px; color: #666;">
                <div>💡 <b>Click marker to see image!</b></div>
                <div style="margin-top: 5px;">
                    Updated: {datetime.now().strftime('%d.%m.%Y %H:%M')}<br>
                    Images: Local Pics folder (1.jpg - 10.jpg)
                </div>
            </div>
        </div>
        """
        
        self.map.get_root().html.add_child(folium.Element(panel_html))
    
    def add_legend_with_images(self):
        """Legend with image information"""
        legend_html = """
        <div style="position: fixed; bottom: 10px; right: 10px;
                    width: 200px; background: white; 
                    border: 1px solid #ccc; border-radius: 8px;
                    padding: 12px; z-index: 9999; font-size: 11px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            
            <h4 style="margin: 0 0 8px 0; text-align: center;">🗺️ Legend</h4>
            
            <p><span style="color: red;">🔴</span> Missile strikes</p>
            <p><span style="color: purple;">🟣</span> Drone attacks</p>
            <p><span style="color: orange;">🟠</span> Artillery shelling</p>
            <p><span style="color: blue;">🔵</span> Air raid alerts</p>
            <p><span style="color: green;">🟢</span> Infrastructure</p>
            <p><span style="color: darkred;">🟤</span> Other events</p>
            
            <hr style="margin: 10px 0;">
            
            <div style="background: #fffbeb; padding: 8px; border-radius: 4px; border: 1px solid #fbbf24;">
                <b>📸 Images in markers:</b><br>
                • Local Pics folder<br>
                • Images 1.jpg - 10.jpg<br>
                • Random selection<br>
                <small style="color: #92400e;">Click marker to see!</small>
            </div>
            
            <div style="margin-top: 8px; text-align: center; font-size: 10px; color: #666;">
                Simulated data + local images<br>
                Updated every 15 min
            </div>
        </div>
        """
        
        self.map.get_root().html.add_child(folium.Element(legend_html))
    
    def add_layers(self):
        """Adds map layers"""
        # Satellite
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='🛰️ Satellite',
            overlay=False,
            control=True
        ).add_to(self.map)
        
        # Dark
        folium.TileLayer(
            'cartodbdark_matter', 
            name='🌙 Dark'
        ).add_to(self.map)
        
        # Layer control
        folium.LayerControl().add_to(self.map)
    
    def create_map_with_images(self):
        """Main function - creates map with images"""
        print("🇺🇦 CREATING MAP WITH IMAGES")
        print("=" * 35)
        print("📸 Each marker will have an image!")
        print("=" * 35)
        
        # 1. Generate events with images
        events = self.generate_events_with_images(60)
        
        # 2. Add everything to map
        self.add_markers_with_images(events)
        self.add_extended_statistics(events)
        self.add_legend_with_images()
        self.add_layers()
        
        print("✅ Map with images ready!")
        return self.map
    
    def save(self, filename="ukraine_map_with_images.html"):
        """Saves the map"""
        self.map.save(filename)
        print(f"💾 Saved: {filename}")

# ============================================================================
# EXECUTION
# ============================================================================

def main():
    print("🚀 UKRAINE MAP WITH IMAGES")
    print("=" * 32)
    print("📸 Each marker has an image!")
    print("🖼️ Sources: Unsplash + Wikimedia")
    print("🔍 Click marker to see")
    print("=" * 32)
    
    try:
        # Create map
        map_obj = UkraineMapWithImages()
        
        # Generate and save
        map_obj.create_map_with_images()
        map_obj.save("ukraine_map_with_images.html")
        
        print("\n🎉 SUCCESS!")
        print("📁 Open: ukraine_map_with_images.html")
        print("\n🎯 NEW FEATURES:")
        print("• 📸 Images in every marker")
        print("• 🖼️ Multiple image sources")
        print("• 📊 Image source statistics")
        print("• 🎨 Better popups with images")
        print("• 🔍 Tooltips with preview")
        print("• 📐 Coordinates in popups")
        print("\n💡 INSTRUCTIONS:")
        print("1. Click on any marker")
        print("2. See image from location")
        print("3. Read event details")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Requires: pip install folium
    # Also requires: Pics folder with images 1.jpg to 10.jpg
    main()

"""
📸 MAP WITH LOCAL IMAGES - NEW FEATURES:

✅ LOCAL IMAGES IN MARKERS:
- Each marker has image from Pics folder
- Uses images 1.jpg to 10.jpg
- Random selection from available images
- 400x300px display size
- Fallback for missing images

🖼️ LOCAL IMAGE SOURCES:
- Pics folder in same directory
- Images named 1.jpg, 2.jpg, ... 10.jpg
- Automatic folder creation if missing
- Error handling for missing files

🎨 IMPROVED POPUPS:
- Local image at top
- Gradient header
- Information grid
- Colorful sections
- GPS coordinates

📊 EXTENDED STATISTICS:
- Local image count
- Event status
- Type bar chart

🔧 TECHNICAL:
- OS path handling
- File existence checking
- Error handling for images
- Responsive sizes
- Clustering with unpacking

SETUP:
1. Create 'Pics' folder in same directory as .py file
2. Add images named 1.jpg, 2.jpg, 3.jpg, ... up to 10.jpg
3. pip install folium
4. python filename.py

CLICK MARKER = SEE LOCAL IMAGE! 📸
"""