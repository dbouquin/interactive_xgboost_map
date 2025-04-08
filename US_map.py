import folium
import base64
import os

# Create a map centered on the United States
us_map = folium.Map(location=[39.8283, -98.5795], zoom_start=4)

# Title and description
title_html = '''
<div style="position: fixed; 
            top: 10px; left: 50px; width: 400px; height: auto;
            background-color: white; border:2px solid grey; z-index:9999; 
            padding: 10px; border-radius: 5px; opacity: 0.85;">
    <h3 style="margin-top: 0;">XGBoost Performance by Location</h3>
    <p>XGBoost does <span style="color:green; font-weight:bold;">well</span> in locations where forecast uncertainty or spread is stable over time. This occurs in places with less volatile weather patterns.</p>
    <p>XGBoost does <span style="color:red; font-weight:bold;">red</span> in areas where the forecast errors can be more sporadic (timing errors from convective-driven local rainfall).</p>
    <p><b>Color code:</b></p>
    <ul style="padding-left: 20px; margin-bottom: 5px;">
        <li>Good GXBoost performance is noted with <span style="color:green; font-weight:bold;">green</span> borders</li>
        <li>Poor GXBoost performance is noted with <span style="color:red; font-weight:bold;">red</span> borders</li>
    </ul>
    <div style="text-align: right; margin-top: 5px;">
        <button onclick="this.parentElement.parentElement.style.display='none'" 
                style="padding: 5px; border-radius: 3px; background-color: #f0f0f0; border: 1px solid #ccc;">
            Close
        </button>
    </div>
</div>
'''
us_map.get_root().html.add_child(folium.Element(title_html))

# List of US cities with their coordinates
cities = [
    {"name": "Seattle", "lat": 47.6062, "lon": -122.3321, "image": "bias_Seattle_Tacoma.png"}, 
    {"name": "Minneapolis", "lat": 44.9778, "lon": -93.2650, "image": "bias_Minneapolis.png"}, 
    {"name": "Denver", "lat": 39.7392, "lon": -104.9903, "image": "bias_Denver.png"}, 
    {"name": "Las Vegas", "lat": 36.1699, "lon": -115.1398, "image": "bias_Las_Vegas.png"}, 
    {"name": "Boston", "lat": 42.3601, "lon": -71.0589, "image": "bias_Boston.png"},
    {"name": "Orlando", "lat": 28.5383, "lon": -81.3792, "image": "bias_Orlando.png"},
    {"name": "Little Rock", "lat": 34.7465, "lon": -92.2896, "image": "bias_Little_Rock.png"},
    {"name": "Cincinnati", "lat": 39.1031, "lon": -84.5120, "image": "bias_Cincinnati.png"}
]

# Define colors
colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'darkblue', 'darkgreen']

# Function to create HTML for an image popup
def create_image_popup(image_path, city_name):
    """
    Creates an HTML popup with an image for a city marker.
    
    Args:
        image_path (str): Path to the image file
        city_name (str): Name of the city
        
    Returns:
        str: HTML code for the popup
    """
    try:
        # Check if image exists
        if not os.path.isfile(image_path):
            return f"<h4>{city_name}</h4><p>Image not found: {image_path}</p>"
            
        # Read and encode the image
        with open(image_path, 'rb') as img_file:
            img_data = base64.b64encode(img_file.read()).decode('utf-8')
        
        # Determine content type based on file extension
        if image_path.lower().endswith('.png'):
            content_type = "image/png"
        elif image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
            content_type = "image/jpeg"
        else:
            content_type = "image/png"  # Default to PNG
        
        # Determine border color
        green_cities = ["Seattle", "Minneapolis", "Denver", "Las Vegas"]
        border_color = "green" if city_name in green_cities else "red"
        border_thickness = "5px"
        
        # Create HTML with the image and border
        img_html = f"""
        <div style="text-align:center;">
            <img src="data:{content_type};base64,{img_data}" width="300px" 
                 style="border: {border_thickness} solid {border_color}; border-radius: 8px;">
        </div>
        """
        return img_html
    except Exception as e:
        return f"<h4>{city_name}</h4><p>Error loading image: {str(e)}</p>"

# Add each city to the map
for i, city in enumerate(cities):
    # Create popup with image
    popup_html = create_image_popup(city["image"], city["name"])
    
    # Add a marker for the city
    folium.Marker(
        location=[city["lat"], city["lon"]],
        popup=folium.Popup(popup_html, max_width=350),
        tooltip=city["name"],
        icon=folium.Icon(color=colors[i % len(colors)])
    ).add_to(us_map)

# Save the map to an HTML file
us_map.save("US_cities_map.html")

print("Map created and saved as 'US_cities_map.html'")
print("Make sure the following image files exist in the same directory:")
for city in cities:
    print(f"- {city['image']}")