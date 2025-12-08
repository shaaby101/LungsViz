# Configuration Guide - Lungs Exposure Risk Visualizer

## Environment Variables (.env)

Create a `.env` file in the project root with the following content:

### Minimal Configuration (Required)
```bash
# OpenWeatherMap API Configuration
OPENWEATHER_API_KEY=your_api_key_here
```

### Full Configuration (Optional)
```bash
# OpenWeatherMap API
OPENWEATHER_API_KEY=your_api_key_here

# Flask Configuration
FLASK_ENV=development          # or production
FLASK_DEBUG=True               # or False for production
FLASK_HOST=0.0.0.0            # Accessible from any interface
FLASK_PORT=5000                # Port number

# Application Settings
DEFAULT_CITY_LAT=28.6139        # Default: Delhi
DEFAULT_CITY_LON=77.2090
EXPOSURE_SCALE=500             # Reference exposure for 100% lung fill
```

---

## Getting OpenWeatherMap API Key

### Step-by-Step Guide

1. **Visit OpenWeatherMap**
   - URL: https://openweathermap.org/api

2. **Create Free Account**
   - Click "Sign Up"
   - Enter email, password
   - Verify email address

3. **Access API Keys**
   - Log in to account
   - Go to "API keys" section
   - You'll see a default key with name "Default"

4. **Copy Your Key**
   - Select entire key (usually 32-character string)
   - Copy to clipboard

5. **Create .env File**
   - In project root, create new file: `.env`
   - Add: `OPENWEATHER_API_KEY=your_copied_key_here`
   - Save file

6. **Test Configuration**
   - Run app: `python app.py`
   - Click any city button
   - Should see live AQI data

### Free Tier Details

```
API Calls/Day:     1000
Data Update Rate:  ~5-10 minutes
Geographic Coverage: Global
Pollutants Included: PM2.5, PM10, NO₂, SO₂, CO, O₃, NH₃
Cost:              Free
Restrictions:      None for educational use
```

---

## Configurable Constants

### In `app.py`

#### 1. Breathing Rates (Line ~15)
```python
BREATHING_RATES = {
    'resting': 0.5,    # m³/hour - Sitting indoors
    'walking': 1.0,    # m³/hour - Normal walking
    'cycling': 1.4,    # m³/hour - Moderate cycling
    'running': 1.8     # m³/hour - High intensity running
}
```

**To customize:**
- Edit values based on research or specific needs
- Keep units consistent (m³/hour)
- Lower values = less exposure, higher = more exposure

**Examples:**
```python
# Sedentary lifestyle
'sleeping': 0.3,
'office_work': 0.6,

# Active sports
'volleyball': 1.5,
'basketball': 2.0,
'tennis': 2.2,
```

#### 2. AQI Breakpoints (Line ~25)
```python
AQI_BREAKPOINTS = [
    {'aqi_max': 50, 'pm25_max': 12.0, 'category': 'Good'},
    {'aqi_max': 100, 'pm25_max': 35.4, 'category': 'Satisfactory'},
    # ... etc
]
```

**Standard Values (EPA):**
- Good: 0-50 → PM2.5: 0-12.0 µg/m³
- Satisfactory: 51-100 → PM2.5: 12.1-35.4 µg/m³
- Moderately Polluted: 101-150 → PM2.5: 35.5-55.4 µg/m³
- Poor: 151-200 → PM2.5: 55.5-150.4 µg/m³
- Very Poor: 201-300 → PM2.5: 150.5-250.4 µg/m³
- Severe: 301-500 → PM2.5: 250.5-500 µg/m³

**Note:** Don't modify unless using different standards (India has slightly different breakpoints)

#### 3. Risk Levels (Line ~35)
```python
RISK_LEVELS = [
    {'aqi_max': 50, 'level': 'Low', 'color': '#10b981', 'advice': '...'},
    {'aqi_max': 100, 'level': 'Moderate', 'color': '#f59e0b', 'advice': '...'},
    # ... etc
]
```

**Customize:**
- Change 'level' name
- Modify 'color' (hex code)
- Update 'advice' with custom health recommendations

### In `templates/index.html`

#### 1. Particle Count (Line ~250)
```javascript
const particleCount = 500;  // Number of particles in 3D scene
```

**Performance impact:**
- 500: Balanced (recommended)
- 200: Lower systems
- 1000: High-end systems only

#### 2. Lung Fill Scale (Line ~520)
```javascript
// In calculateExposure():
lung_fill = min(100, (exposure / 500) * 100);
```

**Change reference exposure:**
- Current: 500µg = 100% fill
- Lower value: More dramatic visualization
- Higher value: Subtler visualization

#### 3. Colors (CSS variables, Line ~50-100)
```css
--color-primary: #06b6d4;      /* Cyan - Primary color */
--color-bg: #0f172a;           /* Dark blue - Background */
--color-success: #10b981;      /* Green - Low risk */
--color-warning: #f59e0b;      /* Orange - Moderate risk */
--color-danger: #ef4444;       /* Red - High risk */
```

**Dark mode colors (CSS):**
- Change for different theme
- Ensure contrast ratio ≥4.5:1 for text

#### 4. Animation Speed (Line ~330)
```javascript
leftLung.rotation.y += 0.003;  // Rotation speed
particleGeometry.userData.velocity  // Particle movement
```

**Lower value** = slower rotation
**Higher value** = faster rotation

---

## Advanced Configuration

### Custom Cities List

In `app.py`, modify `get_cities()` function:

```python
@app.route('/api/cities', methods=['GET'])
def get_cities():
    cities = [
        {'name': 'New York', 'lat': 40.7128, 'lon': -74.0060},
        {'name': 'London', 'lat': 51.5074, 'lon': -0.1278},
        {'name': 'Tokyo', 'lat': 35.6762, 'lon': 139.6503},
        {'name': 'Your City', 'lat': YOUR_LAT, 'lon': YOUR_LON},
    ]
    return jsonify(cities)
```

**Find coordinates:**
- Google Maps: Right-click → "What's here?" → Bottom left
- GPS Coordinates: Search "GPS coordinates [city name]"
- OpenStreetMap: Click location → Details panel

### Custom Default City

In `app.py`, line ~140:
```python
@app.route('/api/air-quality', methods=['GET'])
def fetch_air_quality():
    lat = request.args.get('lat', 35.6762, type=float)    # Tokyo latitude
    lon = request.args.get('lon', 139.6503, type=float)   # Tokyo longitude
    # ... rest of function
```

### Custom Health Advice

In `app.py`, modify `RISK_LEVELS`:

```python
RISK_LEVELS = [
    {
        'aqi_max': 50,
        'level': 'Excellent',
        'color': '#10b981',
        'advice': 'Perfect day for outdoor activities! Breathe freely.'
    },
    # ... etc
]
```

### Custom Port

In `app.py`, last line:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)  # Changed from 5000
```

Then access: `http://localhost:8080`

---

## Production Configuration

### For Deployment

```python
# In app.py
FLASK_ENV = 'production'
FLASK_DEBUG = False
```

### Using Gunicorn (Recommended)

```bash
# Install
pip install gunicorn

# Run
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables (Server)

Set these on your server:
```bash
export OPENWEATHER_API_KEY="your_key"
export FLASK_ENV="production"
```

### Security Headers (Production)

Consider adding to `app.py`:
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

---

## Troubleshooting Configuration

### "API key not valid"
```
Solution:
1. Copy entire key (no spaces)
2. Wait 10 minutes after creating key
3. Check you're using free tier (not paid key)
4. Visit https://openweathermap.org/api to verify
```

### "Address already in use"
```
Solution 1: Change port in app.py
Solution 2: Kill existing process on port 5000
  Windows: netstat -ano | findstr :5000 → taskkill /PID <pid> /F
  macOS/Linux: lsof -i :5000 → kill -9 <pid>
```

### "ModuleNotFoundError"
```
Solution:
1. Activate virtual environment
2. Run: pip install -r requirements.txt
3. Verify all packages installed: pip list
```

### Slow API responses
```
Solutions:
1. Check internet connection
2. Reduce API call frequency
3. Consider caching responses
4. Use paid tier for higher limits
```

---

## Performance Tuning

### Reduce Memory Usage
```python
# In app.py
BREATHING_RATES = {'resting': 0.5}  # Fewer activities if needed
```

### Optimize 3D Rendering
```javascript
// In templates/index.html
particleCount = 200;  // Instead of 500
renderer.setPixelRatio(0.5);  // Lower resolution
```

### Cache API Responses
```python
# Add to app.py
from functools import lru_cache

@lru_cache(maxsize=100)
def get_real_time_aqi(lat, lon):
    # Responses cached for repeated calls
    ...
```

---

## Version Compatibility

### Python Versions
- ✅ 3.8 (Tested)
- ✅ 3.9 (Tested)
- ✅ 3.10 (Tested)
- ✅ 3.11 (Tested)
- ❌ 3.7 (Not supported)
- ❌ 2.7 (Not supported)

### Browser Compatibility
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ⚠️ Older versions may lack WebGL support

### Dependencies
- Flask 2.3.3
- Flask-CORS 4.0.0
- Requests 2.31.0
- Python-dotenv 1.0.0

---

## Configuration Checklists

### Before Running
- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] requirements.txt installed via pip
- [ ] .env file created with OPENWEATHER_API_KEY
- [ ] API key tested (OpenWeatherMap account verified)

### Before Deploying
- [ ] FLASK_DEBUG set to False
- [ ] FLASK_ENV set to production
- [ ] API key rotated/secured
- [ ] CORS properly configured for domain
- [ ] Error logging enabled
- [ ] HTTPS enabled (if internet-facing)

### Performance Optimization
- [ ] Caching configured
- [ ] Database indexed (if added)
- [ ] API rate limiting considered
- [ ] Frontend minified
- [ ] 3D particle count optimized

---

**Last Updated:** December 2024
