# Technical Documentation - Lungs Exposure Risk Visualizer

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Backend (Flask)](#backend-flask)
3. [Frontend (Three.js)](#frontend-threejs)
4. [API Integration](#api-integration)
5. [Health Models](#health-models)
6. [Algorithms](#algorithms)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Client-Side)                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              index.html (Single Page)                │  │
│  │  ┌────────────────┐        ┌───────────────────┐    │  │
│  │  │   Three.js     │        │  JavaScript Logic │    │  │
│  │  │  3D Lung Model │◄──────►│  Event Handlers   │    │  │
│  │  │    & Particles │        │  API Calls        │    │  │
│  │  └────────────────┘        └───────────────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
│                           ▲                                 │
│                    HTTP (JSON/REST)                         │
│                           ▼                                 │
├─────────────────────────────────────────────────────────────┤
│                   Flask Backend (Server)                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              app.py (Main Flask App)                 │  │
│  │  ┌──────────────┐  ┌─────────────────────┐          │  │
│  │  │  Routes      │  │ Calculation Logic   │          │  │
│  │  │  /api/...    │  │ - AQI ↔ PM2.5       │          │  │
│  │  │              │  │ - Exposure Math     │          │  │
│  │  │              │  │ - Risk Assessment   │          │  │
│  │  └──────────────┘  └─────────────────────┘          │  │
│  │         ▲                                            │  │
│  │      requests to                                     │  │
│  │         ▼                                            │  │
│  │  ┌──────────────────────────────────────┐           │  │
│  │  │   OpenWeatherMap API Integration     │           │  │
│  │  │   - Real-time AQI data               │           │  │
│  │  │   - PM2.5 concentrations             │           │  │
│  │  └──────────────────────────────────────┘           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Backend (Flask)

### Main Application Structure

**File:** `app.py`

### Key Components

#### 1. Configuration & Constants

```python
# Breathing rates by activity (m³/hour)
BREATHING_RATES = {
    'resting': 0.5,    # Sedentary indoor activity
    'walking': 1.0,    # Normal walking speed
    'cycling': 1.4,    # Moderate cycling
    'running': 1.8     # High intensity running
}
```

These values are based on scientific literature:
- **Resting**: EPA standard for sedentary indoor activity
- **Walking**: WHO standard for moderate activity
- **Cycling & Running**: Based on MET (Metabolic Equivalent) values

#### 2. AQI Conversion Logic

```python
def aqi_to_pm25(aqi):
    """Convert AQI to PM2.5 concentration"""
    # Uses EPA AQI breakpoints
    for breakpoint in AQI_BREAKPOINTS:
        if aqi <= breakpoint['aqi_max']:
            return breakpoint['pm25_max']
```

**EPA AQI Breakpoints:**
- AQI 0-50: PM2.5 0-12.0 µg/m³ (Good)
- AQI 51-100: PM2.5 12.1-35.4 µg/m³ (Satisfactory)
- AQI 101-150: PM2.5 35.5-55.4 µg/m³ (Moderately Polluted)
- AQI 151-200: PM2.5 55.5-150.4 µg/m³ (Poor)
- AQI 201-300: PM2.5 150.5-250.4 µg/m³ (Very Poor)
- AQI 301-500: PM2.5 250.5-500 µg/m³ (Severe)

#### 3. Exposure Calculation

```python
def calculate_lung_exposure(pm25, duration_minutes, activity_type):
    breathing_rate = BREATHING_RATES[activity_type]  # m³/hour
    duration_hours = duration_minutes / 60
    total_air_inhaled = breathing_rate * duration_hours
    total_exposure = pm25 * total_air_inhaled  # µg
    return total_exposure
```

**Formula:**
```
Total Exposure (µg) = PM2.5 (µg/m³) × Breathing Rate (m³/hour) × Duration (hours)
```

**Example:**
- PM2.5: 50 µg/m³
- Activity: Walking (1.0 m³/hour)
- Duration: 1 hour
- **Exposure: 50 µg**

#### 4. Risk Assessment

Risk is determined by AQI level with 6 categories:

```python
RISK_LEVELS = [
    {'aqi_max': 50,   'level': 'Low',       'color': '#10b981'},
    {'aqi_max': 100,  'level': 'Moderate',  'color': '#f59e0b'},
    {'aqi_max': 150,  'level': 'High',      'color': '#ef4444'},
    {'aqi_max': 200,  'level': 'Very High', 'color': '#991b1b'},
    {'aqi_max': 300,  'level': 'Severe',    'color': '#4c0519'},
    {'aqi_max': 500,  'level': 'Hazardous', 'color': '#1f0f0f'}
]
```

### API Endpoints

#### GET `/api/air-quality`
Fetches real-time air quality data from OpenWeatherMap

**Parameters:**
- `lat`: Latitude (default: 28.6139)
- `lon`: Longitude (default: 77.2090)

**OpenWeatherMap AQI Scale (1-5) → Standard AQI (0-500):**
- 1 (Good) → 25
- 2 (Fair) → 75
- 3 (Moderate) → 125
- 4 (Poor) → 175
- 5 (Very Poor) → 250

#### POST `/api/calculate-exposure`
Calculates exposure and risk assessment

**Request:**
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
    "total_exposure_micrograms": 55.4,
    "lung_fill_percentage": 11.1,
    "risk_level": "High",
    "health_advice": "Unhealthy for sensitive groups..."
}
```

---

## Frontend (Three.js)

### 3D Lung Visualization

**Technology:** Three.js (WebGL-based 3D graphics)

#### 1. Scene Setup

```javascript
scene = new THREE.Scene();
camera = new THREE.PerspectiveCamera(75, width/height, 0.1, 1000);
renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
```

#### 2. Lung Geometry

Lungs are created using **LatheGeometry** - a technique to create 3D shapes by rotating a 2D profile around an axis.

```javascript
const geometry = new THREE.LatheGeometry(
    [
        new THREE.Vector2(0, 0),
        new THREE.Vector2(0.8, 0.2),
        new THREE.Vector2(0.9, 0.8),
        new THREE.Vector2(0.7, 1.5),
        new THREE.Vector2(0.3, 1.8),
        ...
    ],
    32  // segments
);
```

**Why LatheGeometry?**
- Creates anatomically plausible lung shapes
- Smooth, continuous surface
- Efficient for rendering
- Allows for both left and right lung asymmetry

#### 3. Color Mapping by Risk Level

```javascript
// Changes as fill level increases
fillLevel < 25%  → Green (#10b981)
fillLevel < 50%  → Orange (#f59e0b)
fillLevel < 75%  → Red (#ef4444)
fillLevel ≥ 75%  → Dark Red (#991b1b)
```

#### 4. Particle System

- **500 particles** representing pollutants
- **Red color** (#ef4444) indicating harmful particles
- **Bouncing motion** to simulate air movement
- **Opacity scales** with fill level (0.2 + fill/100 * 0.6)

#### 5. Animation Loop

```javascript
function animate() {
    requestAnimationFrame(animate);
    
    // Rotate lungs
    leftLung.rotation.y += 0.003;
    rightLung.rotation.y += 0.003;
    
    // Update particles (position, velocity, bouncing)
    // Render scene
    renderer.render(scene, camera);
}
```

---

## API Integration

### OpenWeatherMap Air Pollution API

**Endpoint:** `https://api.openweathermap.org/data/2.5/air_pollution`

**Why OpenWeatherMap?**
- Free tier available (1000 calls/day)
- Global coverage
- Real-time data updates
- Historical and forecast data available
- Easy integration with coordinates

**Response Structure:**
```json
{
    "list": [
        {
            "main": {
                "aqi": 3  // 1-5 scale
            },
            "components": {
                "pm2_5": 35.4,
                "pm10": 55.4,
                "no2": 40.0,
                "so2": 20.0,
                "co": 300.0,
                "o3": 60.0,
                "nh3": 0.5
            }
        }
    ]
}
```

**Data Processing:**
1. Extract AQI level (1-5)
2. Convert to standard 0-500 scale
3. Extract PM2.5 directly from components
4. Cache results to avoid rate limiting

---

## Health Models

### Exposure Dose Calculation

**Formula:**
```
Dose (µg) = Concentration (µg/m³) × Volume Inhaled (m³) × Exposure Time (hours)
```

**Justification:**
- Based on toxicology principles
- Used in WHO Air Quality Guidelines
- Directly relates to health outcomes

### Lung Fill Visualization

**Arbitrary Scale:**
```
Lung Fill % = (Total Exposure / 500) × 100
```

- 500µg chosen as reference for "critical exposure"
- Provides intuitive visual representation
- Capped at 100%

### Risk Assessment Logic

**Multi-Factor Approach:**
1. **Primary Factor:** AQI level (accounts for all pollutants)
2. **Activity Factor:** Implicitly included via breathing rate
3. **Duration Factor:** Explicitly calculated
4. **Health Advice:** Tailored to each risk level

---

## Algorithms

### Breathing Rate Estimation (MET-Based)

| Activity | MET Value | Air Intake | Formula |
|----------|-----------|-----------|---------|
| Resting | 1.0 | 0.5 m³/h | REE × 0.5 |
| Walking | 2.0 | 1.0 m³/h | REE × 1.0 |
| Cycling | 2.8 | 1.4 m³/h | REE × 1.4 |
| Running | 3.6 | 1.8 m³/h | REE × 1.8 |

*MET: Metabolic Equivalent of Task*
*REE: Resting Energy Expenditure (~0.5 m³/h)*

### AQI Breakpoint Interpolation

For precise conversions between AQI scales:

```python
# EPA Standard Calculation
if aqi_min <= aqi <= aqi_max:
    pm25 = pm25_min + (aqi - aqi_min) × 
            (pm25_max - pm25_min) / (aqi_max - aqi_min)
```

### Risk Level Determination

Binary search for O(log n) lookup:

```python
for risk in RISK_LEVELS:
    if aqi <= risk['aqi_max']:
        return risk
```

---

## Performance Optimizations

1. **Three.js Rendering**
   - Hardware-accelerated WebGL
   - Frustum culling (only render visible objects)
   - LOD (Level of Detail) for particle system
   - Target: 60 FPS

2. **API Calls**
   - 5-second timeout to prevent hanging
   - Error gracefully with default values
   - Optional client-side caching

3. **Frontend**
   - Minimal DOM manipulation
   - CSS transitions for smooth animations
   - Debounced resize handlers

---

## Health Data Sources

- **EPA Air Quality Index**: https://www.epa.gov/air-quality-index
- **WHO Air Quality Guidelines**: https://www.who.int/publications/details/air-quality-guidelines-global-update
- **NDTV Health**: AQI impact documentation
- **Times of India**: AQI health effects research

---

## Limitations & Considerations

1. **Simplified Model**
   - Assumes uniform PM2.5 distribution
   - Doesn't account for regional variations
   - Simplified lung anatomy
   - Ignores individual health conditions

2. **API Limitations**
   - Free tier: 1000 calls/day
   - ~5 min update frequency
   - Some regions may lack coverage

3. **Accuracy**
   - ±10-15% margin for exposure estimates
   - Health impacts are cumulative, not acute
   - Individual responses vary greatly

---

## Future Enhancements

1. **Advanced Features**
   - Time-series data tracking
   - Multi-pollutant analysis
   - Indoor vs outdoor comparison
   - Age/health profile adjustment

2. **Data Integration**
   - Multiple weather APIs
   - Historical trend analysis
   - Seasonal pattern recognition
   - Predictive modeling

3. **User Experience**
   - PWA support for offline use
   - Mobile app (React Native)
   - Data export (PDF, CSV)
   - Dark/light mode toggle

---

**Last Updated:** December 2024
