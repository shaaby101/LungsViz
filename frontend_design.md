# Project Requirements Document (PRD): LUNG//TRACE

## 1. Project Overview
**LUNG//TRACE** is a high-fidelity environmental intelligence platform that translates abstract air quality data into tangible human respiratory impact. Moving beyond simple numerical readouts, the system utilizes predictive modeling and immersive visualizations to create a "digital twin" of a user's respiratory health in response to their environment.

### 1.1 Mission Statement
To bridge the gap between environmental data and personal health awareness through bold, scientific, and interactive storytelling.

---

## 2. Target Audience
- **Urban Residents**: Individuals in high-pollution zones seeking to manage daily exposure.
- **Health-Conscious Users**: People tracking respiratory wellness and physical performance.
- **Environmental Researchers**: Professionals requiring a unified dashboard for AQI comparative analysis.

---

## 3. Core Features & Functional Requirements

### 3.1 Intelligence Dashboard (Command Center)
- **Real-time Monitoring**: Display AQI, PM2.5, PM10, CO, NO₂, SO₂, and O₃.
- **Breath Score™**: A proprietary algorithm-driven 0-100 score calculating immediate respiratory wellness.
- **24H Intelligence Forecast**: Predictive bar charts showing upcoming pollution spikes.
- **Live Environmental Map**: Geo-synced heatmap showing "Safe Zones" vs. "Hazard Zones."

### 3.2 Digital Lung Simulation
- **Dynamic Visualization**: A central anatomical lung model that changes state (speed, color, particle accumulation) based on real-time AQI.
- **Pulmonary Load Tracking**: Visualizing the current "strain" on lung tissue.
- **Air Age Est.**: Estimating the accelerated aging of lung tissue (e.g., "+3.2 Hours/Day") based on exposure duration.

### 3.3 Pollution Footprint (Exposure Timeline)
- **Location History**: Tracking AQI across a user's daily transit (e.g., Home → Office → Gym).
- **Activity Engine**: Smart recommendations on whether to exercise outdoors based on real-time pollutant density.
- **Monthly Analytics**: Aggregated data showing peak exposure events and total air filtered.

### 3.4 City Battle Mode (Comparative Analysis)
- **Benchmarking**: Side-by-side comparison of two urban centers.
- **Metric Parity**: Comparing PM2.5, NO₂, and Lung Stress indices between locations.
- **Victory Status**: A diagnostic summary of which location is safer for respiratory health.

---

## 4. Design System: Neo-Brutalist Intelligence
The platform adheres to a "Neo-Brutalist" aesthetic—combining scientific rigor with bold, confident UI patterns.

### 4.1 Visual Principles
- **High Contrast**: Pure white (#FFFFFF) or Off-white (#F5F5F0) backgrounds with pure black (#000000) borders.
- **Bold Geometry**: 2-3px solid black borders on all containers; sharp 0-4px corner radii.
- **Tactile Depth**: 4-6px hard offset shadows (no blur) for interactive elements.
- **Functional Color**:
    - **Hazard**: Coral Red (#FF5C5C)
    - **Safe**: Electric Green (#00FF85)
    - **Warning**: Bright Yellow (#FFD600)
    - **Data**: Sky Blue (#5CC8FF)

### 4.2 Typography
- **Headlines**: Space Grotesk (Bold/Extra Bold).
- **Hero Numbers**: Massive 900-weight black type for AQI values.
- **Labels**: All-caps, monospaced (Space Mono) for a technical/terminal feel.

---

## 5. Technical Stack (Proposed)
- **Frontend**: React.js, Tailwind CSS (for Neo-Brutalist utility classes), Framer Motion (for physics-based UI transitions).
- **Visuals**: Three.js or Lottie for the anatomical lung simulation.
- **Data APIs**: OpenWeather Air Pollution API, WAQI (World Air Quality Index), Mapbox GL.
- **Backend**: Node.js/Express with MongoDB for storing user exposure history and personal health profiles.

---

## 6. Success Metrics
- **Engagement**: User frequency of checking the "Can I go outside?" engine.
- **Awareness**: Percentage of users reporting a better understanding of PM2.5 impacts.
- **Accuracy**: Delta between predicted forecast and actual recorded AQI.