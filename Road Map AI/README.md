<div align="center">

<img src="https://img.shields.io/badge/🛣️_RoadMind_AI-FF5A1F?style=for-the-badge&logoColor=white" alt="RoadMind AI" height="60"/>

# RoadMind AI

### Real-Time Road Intelligence · Hazard Detection · Smart Routing

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenStreetMap](https://img.shields.io/badge/OpenStreetMap-7EBC6F?style=flat-square&logo=openstreetmap&logoColor=white)](https://www.openstreetmap.org/)
[![Folium](https://img.shields.io/badge/Folium-77B829?style=flat-square&logo=leaflet&logoColor=white)](https://python-visualization.github.io/folium/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)
[![Cost](https://img.shields.io/badge/Cost-100%25_Free-22C55E?style=flat-square&logo=opensourceinitiative&logoColor=white)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

<br/>

> **An agentic AI system that analyses any road route in real-time — detecting broken roads, construction zones, and blockages, while suggesting the safest alternative paths.**

<br/>

![RoadMind AI Banner](https://img.shields.io/badge/-_🗺️_Live_Map_·_⚠️_Hazard_Scan_·_📷_Road_Images_·_🔀_Smart_Routes_-1C1C1C?style=for-the-badge)

</div>

---

## 📖 About

**RoadMind AI** is a free, real-time road intelligence platform built for engineers, commuters, infrastructure planners, and logistics teams. It transforms any two locations into a comprehensive road health report — powered entirely by open-source geospatial APIs with zero cost.

The system acts as an autonomous agent: it geocodes your journey, computes optimal driving routes, scans the road network for live hazards using OpenStreetMap data, fetches actual road condition images at key waypoints, and presents everything in a single unified dashboard.

Unlike conventional navigation apps, RoadMind AI is purpose-built for **infrastructure monitoring, mining logistics, tunnel assessment, and civil engineering field teams** who need structured hazard intelligence — not just turn-by-turn directions.

---

## 🎯 Why RoadMind AI?

| Problem | RoadMind AI Solution |
|---|---|
| No visibility into road conditions before travel | Real-time hazard scan via Overpass API |
| Navigation apps don't show construction details | Structured hazard cards with severity, type, location |
| No free tool for infrastructure route assessment | 100% free stack — OSM, OSRM, Nominatim, Overpass |
| Road images require expensive APIs | Stitched OSM tile images with Pillow — no cost |
| Single route blindspot | Up to 3 alternative routes with comparison |
| No downloadable field report | Auto-generated .txt report with all hazard data |

### Ideal Use Cases

- 🏗️ **Civil & Infrastructure Engineering** — Pre-survey route checks before site visits
- ⛏️ **Mining & Quarrying Logistics** — Heavy vehicle route clearance checks
- 🚇 **Tunnel & Underground Projects** — Access road monitoring for construction teams
- 🚚 **Fleet & Logistics Management** — Real-time route hazard briefings
- 🗺️ **Urban Planning** — Road health mapping across city corridors
- 🚨 **Emergency Response** — Rapid route assessment for field teams

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                               │
│                    Streamlit Frontend (app.py)                      │
│         Sidebar Input  ·  Live Map  ·  Hazard Report  ·  Images    │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                ┌───────────▼───────────┐
                │   ORCHESTRATOR LAYER  │
                │  Route Analysis Agent │
                │  (Python Backend)     │
                └──┬────┬────┬────┬────┘
                   │    │    │    │
       ┌───────────▼┐ ┌─▼──┐ ┌▼──────────┐ ┌▼────────────┐
       │  GEOCODING │ │ROUT│ │  HAZARD   │ │   IMAGERY   │
       │   MODULE   │ │ING │ │  SCANNER  │ │   MODULE    │
       │            │ │    │ │           │ │             │
       │ Nominatim  │ │OSRM│ │ Overpass  │ │  OSM Tile   │
       │ Free API   │ │Free│ │    API    │ │  Fetcher    │
       │            │ │    │ │  (Free)   │ │  + Pillow   │
       └─────┬──────┘ └─┬──┘ └─────┬─────┘ └──────┬──────┘
             │          │          │               │
             └──────────┴──────────┴───────────────┘
                                │
                    ┌───────────▼───────────┐
                    │    DATA PIPELINE      │
                    │                       │
                    │ • Haversine distance  │
                    │ • Route point sampler │
                    │ • Reverse geocoder    │
                    │ • Severity classifier │
                    │ • Report generator    │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │      OUTPUT LAYER     │
                    │                       │
                    │ • Interactive map     │
                    │ • Hazard cards (UI)   │
                    │ • OSM road images     │
                    │ • Turn-by-turn nav    │
                    │ • .txt report export  │
                    └───────────────────────┘
```

### Data Flow

```
User Input (Start / End Location)
         │
         ▼
[1] Nominatim Geocoding ──► lat/lon coordinates
         │
         ▼
[2] OSRM Routing Engine ──► GeoJSON route + steps (up to 3 alternatives)
         │
         ▼
[3] Route Point Sampler ──► 6 evenly-spaced waypoints along route
         │
         ├──► [4a] Overpass API ──► Real OSM hazard elements (construction, barriers, closures)
         │
         ├──► [4b] Nominatim Reverse ──► Human-readable place names per waypoint
         │
         └──► [4c] OSM Tile Fetcher ──► 3×2 tile grid stitched via Pillow → base64 PNG
                          │
                          ▼
         [5] Streamlit UI renders:
              ├── Folium dark-theme interactive map
              ├── Route comparison cards
              ├── Horizontal hazard report strip
              ├── Road condition image grid
              └── Downloadable field report
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose | Cost |
|---|---|---|---|
| **Frontend** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) | Interactive web dashboard | Free |
| **Map Rendering** | ![Folium](https://img.shields.io/badge/Folium-77B829?style=flat-square&logo=leaflet&logoColor=white) | Interactive Leaflet.js map | Free |
| **Geocoding** | ![OSM](https://img.shields.io/badge/Nominatim-7EBC6F?style=flat-square&logo=openstreetmap&logoColor=white) | Location → Coordinates | Free |
| **Routing** | ![OSRM](https://img.shields.io/badge/OSRM-2196F3?style=flat-square&logo=mapbox&logoColor=white) | Driving route calculation | Free |
| **Hazard Data** | ![Overpass](https://img.shields.io/badge/Overpass_API-E95420?style=flat-square&logo=openstreetmap&logoColor=white) | Live road hazard queries | Free |
| **Road Images** | ![OSM Tiles](https://img.shields.io/badge/OSM_Tiles-7EBC6F?style=flat-square&logo=openstreetmap&logoColor=white) | Map tile stitching | Free |
| **Image Processing** | ![Pillow](https://img.shields.io/badge/Pillow-3776AB?style=flat-square&logo=python&logoColor=white) | Tile stitching + pin marker | Free |
| **HTTP Client** | ![Requests](https://img.shields.io/badge/Requests-3776AB?style=flat-square&logo=python&logoColor=white) | API calls | Free |
| **Map Tiles** | ![CartoDB](https://img.shields.io/badge/CartoDB_Dark-1a1a2e?style=flat-square&logoColor=white) | Dark theme base map | Free |

</div>

### API Endpoints Used

```
Geocoding    →  https://nominatim.openstreetmap.org/search
Routing      →  http://router.project-osrm.org/route/v1/driving/
Hazards      →  https://overpass-api.de/api/interpreter
Rev. Geocode →  https://nominatim.openstreetmap.org/reverse
OSM Tiles    →  https://{a|b|c}.tile.openstreetmap.org/{z}/{x}/{y}.png
```

> ✅ **No API keys required.** All endpoints are public and free.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/hovarthans/roadmind-ai.git
cd roadmind-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run app.py
```

### Dependencies

```txt
streamlit>=1.32.0
folium>=0.16.0
streamlit-folium>=0.20.0
requests>=2.31.0
Pillow>=10.0.0
```

### Usage

1. Open your browser at `http://localhost:8501`
2. Enter a **Starting Point** (e.g. `Chennai, India`)
3. Enter a **Destination** (e.g. `Bangalore, India`)
4. Toggle options: alternative routes, hazard scan, road images
5. Click **🚀 Analyse Route**
6. Explore the live map, hazard report, road images, and navigation steps
7. Download the full `.txt` field report

---

## ✨ Features

### 🗺️ Real-Time Interactive Map
Full-screen dark-theme Folium map with the primary route highlighted in orange and up to 2 alternative routes overlaid. Hazard markers are colour-coded by severity and clickable for full details.

### ⚠️ Intelligent Hazard Detection
Queries OpenStreetMap's Overpass API at 6 sampled waypoints along the route. Detects and classifies:
- 🚫 Road blocked / no access
- 🏗️ Active construction zones
- 🚧 Highway construction corridors
- 🔒 Barriers and access restrictions

Each hazard card shows the **exact km from start**, place name, severity badge, and GPS coordinates.

### 🔀 Smart Route Alternatives
OSRM computes up to 3 driving route alternatives. All routes are rendered simultaneously on the map with distance and estimated time for easy comparison.

### 📷 Road Condition Images
At each sampled waypoint, a 3×2 grid of live OpenStreetMap tiles is fetched, stitched into a single image using Pillow, and displayed inline with a red pin marker — no external redirects, no broken images.

### 🧭 Turn-by-Turn Navigation
Full step-by-step manoeuvre instructions extracted from the OSRM response, with distance and time per segment.

### 📄 Downloadable Field Report
Auto-generated structured `.txt` report including journey summary, all hazard details with coordinates, and route comparison — ready for field teams.

---

## 📁 Project Structure

```
roadmind-ai/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── LICENSE                 # MIT License
```

---

## 🗺️ Roadmap

- [ ] Real-time traffic overlay via OpenTraffic
- [ ] AI image analysis of road surface quality (YOLOv8)
- [ ] Mobile-responsive layout
- [ ] PDF report export with embedded map screenshot
- [ ] SMS/email hazard alerts for field teams
- [ ] Historical hazard trend analysis
- [ ] Multi-stop route planning (waypoints)
- [ ] Elevation profile chart along route
- [ ] Offline mode with cached tile support

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

<div align="center">

<br/>

**Hovarthan S**

*AI Innovator · Software Engineer · Geospatial Systems*

[![GitHub](https://img.shields.io/badge/GitHub-@hovarthans-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/hovarthans)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Hovarthan_S-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/hovarthans)
[![Email](https://img.shields.io/badge/Email-Contact_Me-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:hovarthan@email.com)

<br/>

> *"Building intelligent systems that make the physical world smarter, safer, and more navigable."*

</div>

---

## 📬 Contact

Have a question, idea, or collaboration proposal?

| Channel | Details |
|---|---|
| 📧 **Email** | hovarthan@email.com |
| 💼 **LinkedIn** | [linkedin.com/in/hovarthans](https://linkedin.com/in/hovarthans) |
| 🐙 **GitHub** | [github.com/hovarthans](https://github.com/hovarthans) |
| 🐦 **Twitter / X** | [@hovarthans](https://twitter.com/hovarthans) |

---

<div align="center">

<br/>

**RoadMap — Make your Journey Easier.**

*© Copyright 2026 Hovarthan S · All rights reserved*

<br/>

[![Made with Python](https://img.shields.io/badge/Made_with-Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Powered by OSM](https://img.shields.io/badge/Powered_by-OpenStreetMap-7EBC6F?style=flat-square&logo=openstreetmap&logoColor=white)](https://openstreetmap.org)
[![Built with Streamlit](https://img.shields.io/badge/Built_with-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)

</div>
