import os
import mimetypes
import requests
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import math

load_dotenv()

mimetypes.add_type('model/gltf-binary', '.glb')
mimetypes.add_type('model/gltf+json', '.gltf')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=BASE_DIR, static_folder=STATIC_DIR)
CORS(app)

@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:;"
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

# API Configuration
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'YOUR_API_KEY_HERE')

# Activity-based breathing rates (m³/hour)
BREATHING_RATES = {
    'resting': 0.5,
    'walking': 1.0,
    'cycling': 1.4,
    'running': 1.8
}

MASK_EFFICIENCY = {
    'none': 0.0,
    'cloth': 0.4,
    'n95': 0.95
}

CIGARETTE_EQUIVALENCE_MICROGRAMS = 22  # µg inhaled per cigarette

# AQI to PM2.5 conversion (EPA breakpoints)
AQI_BREAKPOINTS = [
    {'aqi_max': 50, 'pm25_max': 12.0, 'category': 'Good'},
    {'aqi_max': 100, 'pm25_max': 35.4, 'category': 'Satisfactory'},
    {'aqi_max': 150, 'pm25_max': 55.4, 'category': 'Moderately Polluted'},
    {'aqi_max': 200, 'pm25_max': 150.4, 'category': 'Poor'},
    {'aqi_max': 300, 'pm25_max': 250.4, 'category': 'Very Poor'},
    {'aqi_max': 500, 'pm25_max': 500, 'category': 'Severe'}
]

RISK_LEVELS = [
    {'aqi_max': 50, 'level': 'Low', 'color': '#10b981', 'advice': 'Air quality is good. Safe to exercise outdoors.'},
    {'aqi_max': 100, 'level': 'Moderate', 'color': '#f59e0b', 'advice': 'Acceptable. Sensitive groups should avoid prolonged outdoor activity.'},
    {'aqi_max': 150, 'level': 'High', 'color': '#ef4444', 'advice': 'Unhealthy for sensitive groups. General public should reduce outdoor activity.'},
    {'aqi_max': 200, 'level': 'Very High', 'color': '#991b1b', 'advice': 'Unhealthy. Everyone should reduce outdoor exertion.'},
    {'aqi_max': 300, 'level': 'Severe', 'color': '#4c0519', 'advice': 'Very unhealthy. Avoid outdoor activity. Wear N95 masks.'},
    {'aqi_max': 500, 'level': 'Hazardous', 'color': '#1f0f0f', 'advice': 'Hazardous. Stay indoors. Use air purifiers.'}
]

def aqi_to_pm25(aqi):
    """Convert AQI to PM2.5 concentration (µg/m³)"""
    for breakpoint in AQI_BREAKPOINTS:
        if aqi <= breakpoint['aqi_max']:
            return breakpoint['pm25_max']
    return 500

def get_risk_level(aqi):
    """Get risk level based on AQI"""
    for risk in RISK_LEVELS:
        if aqi <= risk['aqi_max']:
            return risk
    return RISK_LEVELS[-1]

def calculate_lung_exposure(pm25, duration_minutes, activity_type):
    """
    Calculate lung exposure based on:
    - PM2.5 concentration (µg/m³)
    - Duration of exposure (minutes)
    - Activity type (affects breathing rate)
    
    Returns pollutant dose in µg
    """
    if activity_type not in BREATHING_RATES:
        activity_type = 'resting'
    
    breathing_rate = BREATHING_RATES[activity_type]  # m³/hour
    duration_hours = duration_minutes / 60
    
    # Total air inhaled
    total_air_inhaled = breathing_rate * duration_hours  # m³
    
    # Total pollutant inhaled (assuming even distribution)
    # PM2.5 * air_volume = pollutant_dose
    total_exposure = pm25 * total_air_inhaled  # µg
    
    return total_exposure

def get_real_time_aqi(lat, lon):
    """Fetch real-time AQI from OpenWeatherMap API"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            aqi_level = data['list'][0]['main']['aqi']
            pm25 = data['list'][0]['components'].get('pm2_5', 0)
            
            # Convert OpenWeather AQI (1-5) to standard AQI (0-500)
            aqi_mapping = {1: 25, 2: 75, 3: 125, 4: 175, 5: 250}
            standard_aqi = aqi_mapping.get(aqi_level, 75)
            
            return {
                'success': True,
                'aqi': standard_aqi,
                'pm25': pm25,
                'raw_level': aqi_level
            }
        else:
            return {'success': False, 'error': 'API Error'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/air-quality', methods=['GET'])
def fetch_air_quality():
    """Fetch air quality data from API"""
    lat = request.args.get('lat', 28.6139, type=float)
    lon = request.args.get('lon', 77.2090, type=float)
    
    result = get_real_time_aqi(lat, lon)
    return jsonify(result)

@app.route('/api/calculate-exposure', methods=['POST'])
def calculate_exposure():
    """Calculate lung exposure and risk"""
    data = request.json
    
    aqi = data.get('aqi', 100)
    duration = data.get('duration', 60)  # minutes
    activity = data.get('activity', 'walking')
    mask_type = data.get('maskType', 'none')
    future_mode = data.get('futureMode', False)
    
    # Convert AQI to PM2.5
    pm25 = aqi_to_pm25(aqi)
    
    # Calculate exposure
    exposure = calculate_lung_exposure(pm25, duration, activity)

    mask_efficiency = MASK_EFFICIENCY.get(mask_type, 0.0)
    adjusted_exposure = exposure * (1 - mask_efficiency)
    
    # Get risk level
    risk = get_risk_level(aqi)
    
    # Calculate lung fill percentage (subjective scale for visualization)
    # Arbitrary scale: 500µg exposure = 100% lung fill
    lung_fill = min(100, (adjusted_exposure / 500) * 100)

    cigarette_equivalent = adjusted_exposure / CIGARETTE_EQUIVALENCE_MICROGRAMS
    annual_exposure = adjusted_exposure * 365
    
    return jsonify({
        'success': True,
        'aqi': aqi,
        'pm25': round(pm25, 2),
        'duration': duration,
        'activity': activity,
        'breathing_rate': BREATHING_RATES.get(activity, 0.5),
        'raw_exposure_micrograms': round(exposure, 2),
        'adjusted_exposure_micrograms': round(adjusted_exposure, 2),
        'annual_exposure_micrograms': round(annual_exposure, 2),
        'cigarette_equivalent': round(cigarette_equivalent, 2),
        'lung_fill_percentage': round(lung_fill, 1),
        'risk_level': risk['level'],
        'risk_color': risk['color'],
        'health_advice': risk['advice'],
        'mask_type': mask_type,
        'mask_efficiency': mask_efficiency,
        'future_mode': future_mode,
        'indoor_reduction': 'Indoor exposure is ~50-70% lower than outdoor'
    })

@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Return list of major Indian cities with coordinates"""
    cities = [
        {'name': 'Delhi', 'lat': 28.6139, 'lon': 77.2090},
        {'name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777},
        {'name': 'Bangalore', 'lat': 12.9716, 'lon': 77.5946},
        {'name': 'Kolkata', 'lat': 22.5726, 'lon': 88.3639},
        {'name': 'Chennai', 'lat': 13.0827, 'lon': 80.2707},
        {'name': 'Pune', 'lat': 18.5204, 'lon': 73.8567},
        {'name': 'Hyderabad', 'lat': 17.3850, 'lon': 78.4867},
        {'name': 'Ahmedabad', 'lat': 23.0225, 'lon': 72.5714},
        {'name': 'Jaipur', 'lat': 26.9124, 'lon': 75.7873},
        {'name': 'Lucknow', 'lat': 26.8467, 'lon': 80.9462}
    ]
    return jsonify(cities)

@app.route('/api/activity-types', methods=['GET'])
def get_activity_types():
    """Return available activity types"""
    activities = [
        {'id': 'resting', 'name': 'Resting (Indoors)', 'breathingRate': 0.5},
        {'id': 'walking', 'name': 'Walking', 'breathingRate': 1.0},
        {'id': 'cycling', 'name': 'Cycling', 'breathingRate': 1.4},
        {'id': 'running', 'name': 'Running/Jogging', 'breathingRate': 1.8}
    ]
    return jsonify(activities)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
