# Lungs Exposure Risk Visualizer - Setup Guide

## Project Overview

A Flask-based web application that visualizes the impact of air pollution on lung health using:
- **Real-time AQI data** from OpenWeatherMap API
- **3D lung visualization** using Three.js
- **Health risk calculation** based on activity and exposure duration
- **Interactive controls** for different cities and activities

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)
- OpenWeatherMap API key (free tier available)

## Project Structure

```
lungs-visualizer/
├── app.py                    # Flask backend
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Frontend HTML with Three.js
└── .env                      # Environment variables (create this)
```

## Step 1: Get OpenWeatherMap API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Go to your API keys section
4. Copy your API key (free tier includes Air Pollution API)
5. Create a `.env` file in the project root:

```bash
OPENWEATHER_API_KEY=your_api_key_here
```

## Step 2: Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Run the Application

```bash
# Make sure you're in the project root directory
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

## Step 4: Access the Application

Open your browser and go to:
```
http://localhost:5000
```

## Features

### 1. Real-Time Air Quality Data
- **City Selection**: Click any city button to fetch live AQI data
- **Manual Input**: Enter custom AQI values
- **PM2.5 Conversion**: Automatic conversion from AQI to PM2.5 concentration

### 2. 3D Lung Visualization
- **Interactive Model**: Lungs rotate continuously in 3D space
- **Color Coding**: Changes color based on pollution level
- **Fill Animation**: Visualizes accumulated pollutant dose
- **Particle System**: Red particles represent pollutants

### 3. Activity-Based Calculation
- **Resting** (0.5 m³/hour) - Sitting indoors
- **Walking** (1.0 m³/hour) - Normal outdoor activity
- **Cycling** (1.4 m³/hour) - Moderate exertion
- **Running** (1.8 m³/hour) - High intensity exercise

### 4. Risk Assessment
- **6 Risk Levels**: Low → Moderate → High → Very High → Severe → Hazardous
- **Color-Coded Output**: Visual risk indicators
- **Health Advice**: Personalized recommendations based on risk level

## API Endpoints

### GET `/`
Returns the main HTML page with the interactive visualizer.

### GET `/api/air-quality`
Fetch real-time air quality data for a location.

**Parameters:**
- `lat` (float): Latitude (default: 28.6139 - Delhi)
- `lon` (float): Longitude (default: 77.2090 - Delhi)

**Response:**
```json
{
  "success": true,
  "aqi": 150,
  "pm25": 55.4,
  "raw_level": 3
}
```

### POST `/api/calculate-exposure`
Calculate lung exposure and health risk.

**Request Body:**
```json
{
  "aqi": 150,
  "activity": "walking",
  "duration": 60
}
```

**Response:**
```json
{
  "success": true,
  "aqi": 150,
  "pm25": 55.4,
  "duration": 60,
  "activity": "walking",
  "breathing_rate": 1.0,
  "total_exposure_micrograms": 55.4,
  "lung_fill_percentage": 11.1,
  "risk_level": "High",
  "risk_color": "#ef4444",
  "health_advice": "Unhealthy for sensitive groups..."
}
```

### GET `/api/cities`
Get list of major Indian cities with coordinates.

### GET `/api/activity-types`
Get available activity types with breathing rates.

## Understanding AQI Scale

| AQI Range | Category | Health Impact |
|-----------|----------|---------------|
| 0-50 | Good | Safe for all activities |
| 51-100 | Satisfactory | Generally safe |
| 101-150 | Moderately Polluted | Sensitive groups at risk |
| 151-200 | Poor | General population affected |
| 201-300 | Very Poor | Significant health effects |
| 301+ | Severe/Hazardous | Health emergency |

## Understanding PM2.5

PM2.5 (fine particulate matter) measures particles ≤2.5 micrometers in diameter. These can:
- Penetrate deep into lungs
- Enter the bloodstream
- Cause respiratory and cardiovascular issues

## Health Insights

### Equivalent Health Impact

- AQI 100 for 24 hours ≈ Smoking 1 cigarette
- Prolonged exposure to high pollution increases risk of:
  - Asthma and respiratory issues
  - Heart disease
  - Reduced lung function
  - Early mortality

### Recommendations

- **AQI < 100**: Safe to exercise outdoors
- **AQI 100-150**: Sensitive groups should limit outdoor activity
- **AQI 150-200**: Everyone should reduce strenuous outdoor activity
- **AQI 200+**: Wear N95 masks, prefer indoor air-filtered spaces
- **AQI 300+**: Stay indoors, use air purifiers

## Customization

### Change Default City
Edit `app.py`, line ~18:
```python
@app.route('/api/air-quality', methods=['GET'])
def fetch_air_quality():
    lat = request.args.get('lat', 28.6139, type=float)  # Change this
    lon = request.args.get('lon', 77.2090, type=float)  # Change this
```

### Add More Cities
Edit the `get_cities()` function in `app.py` to add your custom cities.

### Adjust Breathing Rates
Edit `BREATHING_RATES` dict in `app.py` to customize for different activities.

## Troubleshooting

### "Invalid API Key" Error
- Verify your OpenWeatherMap API key in `.env`
- Ensure the free tier includes Air Pollution API
- Wait 10 minutes after account creation for API activation

### Port 5000 Already in Use
```bash
# Change port in app.py, last line:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### 3D Visualization Not Rendering
- Ensure WebGL is enabled in your browser
- Update your graphics drivers
- Try a different browser

### CORS Errors
- Flask-CORS is already configured
- If issues persist, check firewall settings

## Performance Notes

- 3D rendering optimized for 60 FPS
- Particle system uses WebGL for smooth animation
- API calls cached to avoid rate limiting
- Responsive design for mobile devices

## Future Enhancements

- Time-series exposure tracking
- Comparison between indoor/outdoor air
- Indoor air filter effectiveness simulation
- Export exposure reports
- Multi-pollutant analysis
- Predictive modeling based on weather patterns

## Disclaimer

This tool is for **educational purposes** and provides approximate estimates. 
For medical advice regarding air quality exposure, consult a healthcare professional.

## License

Open source - feel free to modify and distribute.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify API key configuration
3. Review browser console for errors (F12)
4. Check Flask server logs

---

**Last Updated:** December 2024
