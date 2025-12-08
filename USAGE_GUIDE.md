# Usage Guide & Troubleshooting - Lungs Exposure Risk Visualizer

## Quick Usage Examples

### Example 1: Check Air Quality in Delhi During Pollution Season

1. **Open the application** → http://localhost:5000
2. **Click "Delhi"** from city selector
3. **Check the current AQI** (automatically fetched)
4. **Select "Walking"** as activity
5. **Set duration to 30 minutes**
6. **Click "Calculate Exposure"**

**Result:** See lung visualization fill up showing safe level, with health advice

---

### Example 2: Compare Different Activities in Same Pollution Conditions

**Scenario:** AQI = 200 (Unhealthy)

| Activity | Duration | Breathing Rate | Total Exposure | Lung Fill % |
|----------|----------|----------------|-----------------|------------|
| Resting | 1 hour | 0.5 m³/h | 75 µg | 15% |
| Walking | 1 hour | 1.0 m³/h | 150 µg | 30% |
| Cycling | 1 hour | 1.4 m³/h | 210 µg | 42% |
| Running | 1 hour | 1.8 m³/h | 270 µg | 54% |

**Insight:** Running during high pollution is 3.6x more exposure than resting

---

### Example 3: Exercise Safety Decision

**Question:** Should I jog today?

**Input:**
- Current AQI: 180 (Unhealthy for sensitive groups)
- Activity: Running
- Planned Duration: 30 minutes

**Calculation:**
```
PM2.5 = 73.7 µg/m³ (converted from AQI 180)
Breathing Rate = 1.8 m³/h
Duration = 0.5 hours

Exposure = 73.7 × 1.8 × 0.5 = 66.3 µg
Lung Fill = (66.3 / 500) × 100 = 13.26%
```

**Health Advice:** "Unhealthy. Everyone should reduce outdoor exertion."

**Recommendation:** Skip the jog, or wear an N95 mask if it's essential

---

### Example 4: Indoor vs Outdoor Activity

**Indoor Activity (Resting):**
- AQI: 150 (Unhealthy)
- Activity: Resting
- Duration: 8 hours (work day)
- Exposure: 150 × 0.5 × 8 = 600 µg
- **Lung Fill: 120%** (exceeds safe threshold)

**Same Location, Outdoor Walking:**
- Same AQI: 150
- Activity: Walking
- Duration: 2 hours
- Exposure: 150 × 1.0 × 2 = 300 µg
- **Lung Fill: 60%**

**Important:** Indoor exposure is typically 50-70% lower than outdoors due to:
- Infiltration reduction (air doesn't flow freely)
- Settling of larger particles
- HVAC filtration (if present)

---

## Troubleshooting Guide

### Issue 1: "API Error" or "Error fetching air quality data"

**Symptoms:**
- Error message when clicking city buttons or "Get Live Data"
- AQI field shows 0

**Causes & Solutions:**

1. **Invalid or missing API key**
   ```
   Solution:
   - Open .env file
   - Verify OPENWEATHER_API_KEY is set correctly
   - Check you copied the entire key (no spaces)
   - If lost, get new key from https://openweathermap.org/api
   ```

2. **API key not yet activated**
   ```
   Solution:
   - New keys take ~10 minutes to activate
   - Try again after 10 minutes
   - Check OpenWeatherMap account for confirmation email
   ```

3. **Rate limiting exceeded**
   ```
   Solution:
   - Free tier: 1000 calls/day
   - Wait 24 hours or upgrade to paid plan
   ```

4. **Network connectivity issue**
   ```
   Solution:
   - Check internet connection
   - Try accessing https://openweathermap.org in browser
   - Check firewall/proxy settings
   ```

---

### Issue 2: "ModuleNotFoundError: No module named 'flask'"

**Symptoms:**
- Error when starting app.py
- Command line shows module not found

**Solution:**
```bash
# Make sure virtual environment is activated
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Then reinstall dependencies
pip install -r requirements.txt
```

---

### Issue 3: Port 5000 Already in Use

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**

**Option A: Change port in app.py**
```python
# Last line of app.py
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Changed from 5000
```

Then access: http://localhost:5001

**Option B: Kill process using port 5000**

Windows:
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

macOS/Linux:
```bash
lsof -i :5000
kill -9 <PID>
```

---

### Issue 4: 3D Visualization Not Rendering

**Symptoms:**
- Canvas appears blank (black)
- No lung model visible

**Causes & Solutions:**

1. **WebGL not enabled**
   ```
   Solution:
   - Chrome: Settings → Advanced → Graphics → Enable WebGL
   - Firefox: about:config → webgl.disabled = false
   - Safari: Develop menu → Enable WebGL
   ```

2. **Incompatible graphics driver**
   ```
   Solution:
   - Update graphics drivers
   - Try different browser
   - Try in incognito/private mode
   ```

3. **Three.js library not loaded**
   ```
   Solution:
   - Check browser console (F12)
   - Look for failed script loading
   - Verify CDN link is accessible
   ```

4. **Browser console errors**
   ```
   Solution:
   - Open Developer Tools (F12)
   - Check Console tab for errors
   - Check Network tab for failed requests
   - Report error message in logs
   ```

---

### Issue 5: Calculations Look Wrong

**Symptoms:**
- Lung fill percentage seems incorrect
- Risk level doesn't match AQI

**Verification:**

Check the formula: `Total Exposure = PM2.5 × Breathing Rate × Duration`

**Example verification:**
- Input: AQI 100, Walking, 1 hour
- Expected: PM2.5 ≈ 35.4 µg/m³
- Expected: Exposure = 35.4 × 1.0 × 1 = 35.4 µg
- Expected: Fill = (35.4 / 500) × 100 = 7.08%

**If different:**
1. Check AQI conversion (confirm PM2.5 value shown)
2. Check activity breathing rate (should see 1.0 for walking)
3. Check duration input (in minutes, converted to hours)

---

### Issue 6: Browser Shows Blank Page

**Symptoms:**
- Loading forever
- Completely blank page
- No error message

**Solutions:**

1. **Flask server not running**
   ```
   Check terminal for:
   * Running on http://127.0.0.1:5000
   ```

2. **Wrong URL**
   ```
   Make sure using: http://localhost:5000
   NOT: https:// (no SSL)
   NOT: 127.0.0.1:5000 (may have CORS issues)
   ```

3. **Cache issue**
   ```
   Solution:
   - Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
   - Clear browser cache
   - Try incognito mode
   ```

4. **JavaScript disabled**
   ```
   Solution:
   - Enable JavaScript in browser settings
   - Three.js and interactive features require JS
   ```

---

### Issue 7: Slow Performance / Lagging Animation

**Symptoms:**
- Low FPS (less than 30)
- Jerky particle animation
- Lung rotation stutters

**Solutions:**

1. **Close other applications**
   ```
   - Flask + WebGL can be GPU intensive
   - Close browsers, games, video players
   - Reduce other background apps
   ```

2. **Reduce particle count** (edit templates/index.html)
   ```javascript
   // Find this line around line 250:
   const particleCount = 500;  // Reduce to 200
   ```

3. **Lower resolution**
   ```javascript
   renderer.setPixelRatio(0.5);  // Instead of 1.0
   ```

4. **Update graphics drivers**
   ```
   - NVIDIA/AMD/Intel drivers
   - Browser WebGL implementation
   ```

5. **Try different browser**
   ```
   - Chrome typically best WebGL performance
   - Firefox if having issues with Chrome
   - Safari for Mac users
   ```

---

## Common Questions (FAQ)

### Q: Is the visualization scientifically accurate?

**A:** The model is educational and simplified. It:
- ✓ Correctly converts AQI to PM2.5
- ✓ Uses accurate breathing rates by activity
- ✓ Correctly calculates total exposure dose
- ✓ Uses evidence-based risk categories

However, it:
- ✗ Simplified lung anatomy (for visualization)
- ✗ Assumes uniform pollution distribution
- ✗ Doesn't account for personal health factors
- ✗ Uses arbitrary scale for "lung fill %"

**For medical concerns:** Consult healthcare professionals

---

### Q: Why PM2.5 and not PM10?

**A:** PM2.5 (fine particles ≤2.5 micrometers) is more important because:
- Can penetrate deep into alveoli (air sacs)
- Can cross into bloodstream
- Associated with cardiovascular disease
- Longer term health effects
- Used in most health studies

---

### Q: Can I use this offline?

**A:** Partially:
- 3D visualization works offline
- Manual AQI entry works offline
- Real-time API requires internet
- Consider PWA enhancement for future

---

### Q: How often is air quality data updated?

**A:** OpenWeatherMap API provides:
- Real-time data (current conditions)
- Updated every 5-10 minutes on average
- Varies by location coverage
- Historical data available

---

### Q: What about pollution indoors?

**A:** Key points:
- Indoor is typically 50-70% lower than outdoors
- Depends on filtration, sealed windows
- App shows outdoor exposure
- Health advice applies to outdoor activity

---

### Q: Can I customize the app?

**A:** Yes! Key customizations:

1. **Change default city:**
   ```python
   # app.py line ~140
   lat = request.args.get('lat', 28.6139, type=float)  # Change
   lon = request.args.get('lon', 77.2090, type=float)
   ```

2. **Add more cities:**
   ```python
   # In get_cities() function
   {'name': 'Your City', 'lat': LAT, 'lon': LON}
   ```

3. **Adjust breathing rates:**
   ```python
   BREATHING_RATES = {
       'your_activity': 1.5,  # m³/hour
   }
   ```

4. **Change color scheme:**
   ```css
   /* templates/index.html <style> section */
   --color-primary: #your-color;
   ```

---

## Performance Benchmarks

**Expected Performance:**
- Initial load: 2-3 seconds
- API response: 1-2 seconds
- Calculation: <100ms
- 3D rendering: 60 FPS (60Hz displays)
- Memory usage: 100-150MB

---

## Support & Reporting Issues

### Getting Help

1. **Check this guide** for your specific issue
2. **Check browser console** (F12) for error messages
3. **Verify setup** (API key, Python version)
4. **Try different browser** (Chrome/Firefox)

### Providing Bug Reports

Include:
```
- Operating System (Windows/Mac/Linux)
- Python version (python --version)
- Browser and version
- Error message (from console)
- Steps to reproduce
- Screenshots if possible
```

---

**Last Updated:** December 2024
