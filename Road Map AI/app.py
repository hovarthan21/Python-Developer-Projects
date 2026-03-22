import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import math
import time
from datetime import datetime
from PIL import Image, ImageDraw
from io import BytesIO
import base64

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RoadMind AI — Road Intelligence System",
    page_icon="🛩️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&display=swap');

:root {
    --orange: #FF5A1F;
    --dark: #0D0D0D;
    --panel: #141414;
    --card: #1C1C1C;
    --border: #2A2A2A;
    --text: #E8E8E8;
    --muted: #888;
    --green: #22C55E;
    --red: #EF4444;
    --yellow: #F59E0B;
    --blue: #3B82F6;
}

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background: var(--dark) !important;
    color: var(--text) !important;
}

.stApp { background: var(--dark) !important; }

[data-testid="stSidebar"] {
    background: var(--panel) !important;
    border-right: 1px solid var(--border);
}

.road-header {
    background: linear-gradient(135deg, #0D0D0D 0%, #1a0a00 100%);
    border: 1px solid var(--border);
    border-left: 4px solid var(--orange);
    padding: 24px 28px;
    border-radius: 12px;
    margin-bottom: 20px;
}
.road-header h1 { font-size: 2rem; font-weight: 800; margin: 0; color: white; }
.road-header h1 span { color: var(--orange); }
.road-header p { color: var(--muted); margin: 6px 0 0; font-family: 'Space Mono', monospace; font-size: 0.75rem; }

.stat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
    margin-bottom: 12px;
}
.stat-card .val { font-size: 1.8rem; font-weight: 800; color: var(--orange); font-family: 'Space Mono', monospace; }
.stat-card .label { font-size: 0.7rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

/* Hazard cards — horizontal strip layout */
.hazard-strip {
    display: flex;
    flex-direction: row;
    gap: 12px;
    overflow-x: auto;
    padding-bottom: 8px;
    margin: 8px 0;
}
.hazard-strip::-webkit-scrollbar { height: 4px; }
.hazard-strip::-webkit-scrollbar-track { background: var(--dark); }
.hazard-strip::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

.hazard-h-card {
    min-width: 220px;
    max-width: 240px;
    flex-shrink: 0;
    border-radius: 10px;
    padding: 14px 16px;
    border-left: 4px solid;
    font-size: 0.82rem;
}
.hazard-h-card.alert-danger  { background: rgba(239,68,68,0.1);  border-color: var(--red); }
.hazard-h-card.alert-warning { background: rgba(245,158,11,0.1); border-color: var(--yellow); }
.hazard-h-card.alert-info    { background: rgba(59,130,246,0.1); border-color: var(--blue); }
.hazard-h-card.alert-success { background: rgba(34,197,94,0.1);  border-color: var(--green); }
.hazard-h-card .alert-title  { font-weight: 700; margin-bottom: 6px; font-size: 0.85rem; line-height: 1.3; }
.hazard-h-card .alert-meta   { color: var(--muted); font-family: 'Space Mono', monospace; font-size: 0.68rem; line-height: 1.5; }

.section-head {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--orange);
    margin: 20px 0 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}

.stTextInput > div > div > input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 2px rgba(255,90,31,0.2) !important;
}

.stButton > button {
    background: var(--orange) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 12px 28px !important;
    width: 100%;
    transition: all 0.2s;
}
.stButton > button:hover { background: #e04a10 !important; transform: translateY(-1px); }

.route-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 18px;
    margin: 8px 0;
}
.route-card.best { border-color: var(--green); }
.route-card .route-name { font-weight: 700; font-size: 0.95rem; }
.route-card .route-meta { color: var(--muted); font-size: 0.75rem; font-family: 'Space Mono', monospace; margin-top: 4px; }

/* Road images — inline static map tiles */
.road-img-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 8px;
}
.road-img-card img { width: 100%; height: 160px; object-fit: cover; display: block; }
.road-img-card .img-info { padding: 10px 12px; font-size: 0.78rem; }
.road-img-card .img-info .place { font-weight: 700; color: var(--text); }
.road-img-card .img-info .desc { color: var(--muted); font-family: 'Space Mono', monospace; font-size: 0.68rem; margin-top: 3px; }

.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.badge-red    { background: rgba(239,68,68,0.2);  color: #EF4444; }
.badge-yellow { background: rgba(245,158,11,0.2); color: #F59E0B; }
.badge-green  { background: rgba(34,197,94,0.2);  color: #22C55E; }
.badge-blue   { background: rgba(59,130,246,0.2); color: #60A5FA; }

.footer-box {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
    margin-top: 8px;
    font-size: 0.7rem;
    font-family: 'Space Mono', monospace;
    color: var(--muted);
    line-height: 1.8;
    text-align: center;
}
.footer-box .dev { font-size: 0.78rem; font-weight: 700; color: var(--orange); font-family: 'Syne', sans-serif; }
.footer-box .tagline { font-size: 0.72rem; color: var(--text); margin-top: 2px; font-family: 'Syne', sans-serif; font-style: italic; }

.stSpinner { color: var(--orange) !important; }
div[data-testid="stMarkdownContainer"] p { color: var(--text); }
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ─────────────────────────────────────────────────────────────────
OSRM_BASE      = "http://router.project-osrm.org"
NOMINATIM_BASE = "https://nominatim.openstreetmap.org"
OVERPASS_BASE  = "https://overpass-api.de/api/interpreter"

# ─── BACKEND FUNCTIONS ─────────────────────────────────────────────────────────

def geocode(place: str):
    try:
        r = requests.get(
            f"{NOMINATIM_BASE}/search",
            params={"q": place, "format": "json", "limit": 1},
            headers={"User-Agent": "RoadMindAI/1.0"},
            timeout=10
        )
        data = r.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"]), data[0].get("display_name", place)
        return None
    except Exception as e:
        st.error(f"Geocoding error: {e}")
        return None


def get_route(start_ll, end_ll, alternative=False):
    try:
        coords = f"{start_ll[1]},{start_ll[0]};{end_ll[1]},{end_ll[0]}"
        params = {
            "overview": "full",
            "geometries": "geojson",
            "steps": "true",
            "annotations": "true",
        }
        if alternative:
            params["alternatives"] = "true"
        r = requests.get(
            f"{OSRM_BASE}/route/v1/driving/{coords}",
            params=params, timeout=15
        )
        return r.json()
    except Exception as e:
        st.error(f"Routing error: {e}")
        return None


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi    = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def reverse_geocode(lat, lon):
    try:
        r = requests.get(
            f"{NOMINATIM_BASE}/reverse",
            params={"lat": lat, "lon": lon, "format": "json"},
            headers={"User-Agent": "RoadMindAI/1.0"},
            timeout=8
        )
        d    = r.json()
        addr = d.get("address", {})
        road = addr.get("road") or addr.get("street") or addr.get("hamlet") or ""
        city = addr.get("city") or addr.get("town") or addr.get("village") or addr.get("county") or ""
        return f"{road}, {city}".strip(", ") or d.get("display_name", f"{lat:.4f},{lon:.4f}")
    except:
        return f"{lat:.4f}, {lon:.4f}"


def query_road_hazards(lat, lon, radius=500):
    query = f"""
    [out:json][timeout:25];
    (
      way(around:{radius},{lat},{lon})[highway][construction];
      way(around:{radius},{lat},{lon})[highway="construction"];
      way(around:{radius},{lat},{lon})[access=no];
      node(around:{radius},{lat},{lon})[barrier];
      node(around:{radius},{lat},{lon})[highway=construction];
    );
    out center tags;
    """
    try:
        r = requests.post(OVERPASS_BASE, data={"data": query}, timeout=20)
        return r.json().get("elements", [])
    except:
        return []


def sample_route_points(geometry_coords, n=8):
    if not geometry_coords:
        return []
    total = len(geometry_coords)
    if total <= n:
        return geometry_coords
    step = total // n
    return [geometry_coords[i] for i in range(0, total, step)][:n]


def analyze_route_hazards(route_data, start_ll):
    hazards = []
    if not route_data or "routes" not in route_data:
        return hazards
    coords = route_data["routes"][0]["geometry"]["coordinates"]
    points = sample_route_points(coords, 6)
    for lon, lat in points:
        dist_from_start = haversine(start_ll[0], start_ll[1], lat, lon)
        osm_hazards     = query_road_hazards(lat, lon, radius=300)
        place_name      = reverse_geocode(lat, lon)
        for h in osm_hazards:
            tags         = h.get("tags", {})
            hazard_type  = "Road Construction"
            severity     = "high"
            if tags.get("construction"):
                hazard_type = f"Under Construction ({tags['construction']})"
                severity    = "high"
            elif tags.get("access") == "no":
                hazard_type = "Road Blocked / No Access"
                severity    = "critical"
            elif tags.get("barrier"):
                hazard_type = f"Barrier: {tags['barrier'].replace('_',' ').title()}"
                severity    = "medium"
            elif tags.get("highway") == "construction":
                hazard_type = "Highway Construction Zone"
                severity    = "high"
            h_lat = h.get("center", {}).get("lat", lat)
            h_lon = h.get("center", {}).get("lon", lon)
            hazards.append({
                "type":         hazard_type,
                "severity":     severity,
                "lat":          h_lat,
                "lon":          h_lon,
                "km_from_start": round(dist_from_start, 1),
                "place":        place_name,
                "tags":         tags
            })
    return hazards


def build_map(start_ll, end_ll, route_data, hazards, show_alt=True):
    center_lat = (start_ll[0] + end_ll[0]) / 2
    center_lon = (start_ll[1] + end_ll[1]) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles="CartoDB dark_matter")
    if not route_data or "routes" not in route_data:
        return m
    routes = route_data.get("routes", [])
    colors = ["#FF5A1F", "#3B82F6", "#22C55E"]
    labels = ["🟠 Primary Route", "🔵 Alternative Route A", "🟢 Alternative Route B"]
    for idx, route in enumerate(routes[:3]):
        coords   = [[c[1], c[0]] for c in route["geometry"]["coordinates"]]
        dist_km  = round(route["distance"] / 1000, 1)
        dur_min  = round(route["duration"] / 60, 0)
        folium.PolyLine(
            coords,
            color=colors[idx],
            weight=5 if idx == 0 else 3,
            opacity=1.0 if idx == 0 else 0.5,
            tooltip=f"{labels[idx]}: {dist_km} km · {int(dur_min)} min"
        ).add_to(m)
    folium.Marker(start_ll, popup="🟢 START",       icon=folium.Icon(color="green", icon="play",  prefix="fa")).add_to(m)
    folium.Marker(end_ll,   popup="🔴 DESTINATION", icon=folium.Icon(color="red",   icon="flag",  prefix="fa")).add_to(m)
    for h in hazards:
        sev       = h["severity"]
        color     = "red" if sev == "critical" else "orange" if sev == "high" else "beige"
        icon_name = "exclamation-triangle" if sev in ["critical", "high"] else "info"
        popup_html = f"""
        <div style='font-family:sans-serif;min-width:200px'>
            <b style='color:#EF4444'>⚠ {h['type']}</b><br>
            <small>{h['place']}</small><br>
            <hr style='margin:6px 0'>
            <b>{h['km_from_start']} km</b> from start<br>
            <span style='color:#F59E0B'>Severity: {sev.upper()}</span>
        </div>"""
        folium.Marker(
            [h["lat"], h["lon"]],
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color=color, icon=icon_name, prefix="fa")
        ).add_to(m)
    return m


def format_duration(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    return f"{h}h {m}m" if h > 0 else f"{m} min"


def deg2tile(lat, lon, zoom):
    """Convert lat/lon to OSM tile x/y numbers."""
    lat_r = math.radians(lat)
    n = 2 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.log(math.tan(lat_r) + 1.0 / math.cos(lat_r)) / math.pi) / 2.0 * n)
    return x, y


def fetch_map_image(lat, lon, zoom=16):
    """
    Fetch a 3×2 grid of OSM tiles centred on (lat, lon) and stitch into
    a single 768×512 image with a red location pin drawn on top.
    Returns a base64-encoded PNG string ready for an <img> src attribute.
    Falls back to a styled placeholder if tiles cannot be fetched.
    """
    TILE_SIZE = 256
    COLS, ROWS = 3, 2

    cx, cy = deg2tile(lat, lon, zoom)
    # top-left tile of the grid
    x0 = cx - COLS // 2
    y0 = cy - ROWS // 2

    canvas = Image.new("RGB", (TILE_SIZE * COLS, TILE_SIZE * ROWS), (30, 30, 30))

    headers = {"User-Agent": "RoadMindAI/1.0 (road intelligence app)"}
    servers = ["a", "b", "c"]

    for row in range(ROWS):
        for col in range(COLS):
            tx, ty = x0 + col, y0 + row
            server = servers[(tx + ty) % 3]
            url = f"https://{server}.tile.openstreetmap.org/{zoom}/{tx}/{ty}.png"
            try:
                resp = requests.get(url, headers=headers, timeout=6)
                if resp.status_code == 200:
                    tile = Image.open(BytesIO(resp.content)).convert("RGB")
                    canvas.paste(tile, (col * TILE_SIZE, row * TILE_SIZE))
            except Exception:
                pass  # leave that tile as dark background

    # Draw a red pin marker at the exact coordinate
    # Pixel offset of (lat, lon) inside the canvas
    def _tile_pixel(lat_, lon_, zoom_):
        lat_r_ = math.radians(lat_)
        n_ = 2 ** zoom_
        fx = (lon_ + 180.0) / 360.0 * n_
        fy = (1.0 - math.log(math.tan(lat_r_) + 1.0 / math.cos(lat_r_)) / math.pi) / 2.0 * n_
        px = int((fx - x0) * TILE_SIZE)
        py = int((fy - y0) * TILE_SIZE)
        return px, py

    px, py = _tile_pixel(lat, lon, zoom)
    draw = ImageDraw.Draw(canvas)
    r = 10
    # Circle + cross-hair
    draw.ellipse([px - r, py - r, px + r, py + r], fill=(220, 38, 38), outline=(255, 255, 255), width=2)
    draw.line([px, py - r - 4, px, py - r], fill=(220, 38, 38), width=2)

    # Encode to base64
    buf = BytesIO()
    canvas.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"


# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 8px'>
        <div style='font-size:1.4rem;font-weight:800;color:white'>🛩️ RoadMind</div>
        <div style='font-size:0.7rem;color:#888;font-family:Space Mono,monospace;margin-top:2px'>ROAD INTELLIGENCE SYSTEM</div>
    </div>
    <hr style='border-color:#2A2A2A;margin:10px 0 18px'>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-head"> Journey Planner</div>', unsafe_allow_html=True)
    start_input = st.text_input("🟢 Starting Point", placeholder="e.g. Chennai, India")
    end_input   = st.text_input("🔴 Destination",    placeholder="e.g. Bangalore, India")

    st.markdown('<div class="section-head" style="margin-top:20px"> Options</div>', unsafe_allow_html=True)
    show_alternatives = st.toggle("Show alternative routes", value=True)
    scan_hazards      = st.toggle("Scan for real road hazards", value=True)
    show_images       = st.toggle("Show road images", value=True)

    st.markdown("<br>", unsafe_allow_html=True)
    analyse_btn = st.button(" Analyse Route", use_container_width=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("""
    <hr style='border-color:#2A2A2A;margin:24px 0 12px'>
    <div class="footer-box">
        <div class="dev">Developed by Hovarthan S</div>
        <div style='color:var(--orange);font-size:0.68rem;margin-top:1px'>An AI Innovator</div>
        <div class="tagline">RoadMap — Make your Journey Easier.</div>
        <div style='margin-top:6px;font-size:0.65rem;color:#555'>© Copyright 2026 · All rights reserved</div>
    </div>
    """, unsafe_allow_html=True)

# ─── MAIN AREA ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="road-header">
    <h1>Road<span>Mind</span> AI</h1>
    <p>REAL-TIME ROAD INTELLIGENCE · HAZARD DETECTION · SMART ROUTING</p>
</div>
""", unsafe_allow_html=True)

# ── LANDING STATE ──────────────────────────────────────────────────────────────
if not analyse_btn:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="stat-card"><div class="val">LIVE</div><div class="label">Real Road Data</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-card"><div class="val">OSM</div><div class="label">Map Source</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card"><div class="val">FREE</div><div class="label">Zero Cost</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-card"><div class="val">AI</div><div class="label">Hazard Analysis</div></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#141414;border:1px solid #2A2A2A;border-radius:12px;padding:32px;text-align:center;margin-top:20px'>
        <div style='font-size:3rem;margin-bottom:12px'></div>
        <div style='font-size:1.3rem;font-weight:800;color:white;margin-bottom:8px'>Enter your journey details to begin</div>
        <div style='color:#888;font-size:0.85rem'>Enter a start and end location in the sidebar, then click <b style="color:#FF5A1F">Analyse Route</b></div>
        <div style='margin-top:20px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap'>
            <div style='background:#1C1C1C;border:1px solid #2A2A2A;border-radius:8px;padding:10px 18px;font-size:0.8rem'> Real interactive map</div>
            <div style='background:#1C1C1C;border:1px solid #2A2A2A;border-radius:8px;padding:10px 18px;font-size:0.8rem'> Live hazard detection</div>
            <div style='background:#1C1C1C;border:1px solid #2A2A2A;border-radius:8px;padding:10px 18px;font-size:0.8rem'> Road condition images</div>
            <div style='background:#1C1C1C;border:1px solid #2A2A2A;border-radius:8px;padding:10px 18px;font-size:0.8rem'> Alternative routes</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── ANALYSED STATE ─────────────────────────────────────────────────────────────
else:
    if not start_input or not end_input:
        st.warning("⚠️ Please enter both a starting point and destination.")
        st.stop()

    # Geocode
    with st.spinner(" Locating places..."):
        start_result = geocode(start_input)
        time.sleep(1)
        end_result = geocode(end_input)

    if not start_result:
        st.error(f"❌ Could not find: **{start_input}**. Try a more specific location.")
        st.stop()
    if not end_result:
        st.error(f"❌ Could not find: **{end_input}**. Try a more specific location.")
        st.stop()

    start_ll   = (start_result[0], start_result[1])
    end_ll     = (end_result[0],   end_result[1])
    start_name = start_result[2]
    end_name   = end_result[2]

    # Route
    with st.spinner(" Calculating routes..."):
        route_data = get_route(start_ll, end_ll, alternative=show_alternatives)

    if not route_data or "routes" not in route_data or not route_data["routes"]:
        st.error(" Could not calculate a route between these locations. Try different points.")
        st.stop()

    primary = route_data["routes"][0]
    dist_km = round(primary["distance"] / 1000, 1)
    dur_sec = primary["duration"]

    # Hazards
    hazards = []
    if scan_hazards:
        with st.spinner(" Scanning for road hazards via OpenStreetMap..."):
            hazards = analyze_route_hazards(route_data, start_ll)

    # ── SUMMARY METRICS ────────────────────────────────────────────────────────
    route_count = len(route_data.get("routes", []))
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="val">{dist_km}</div><div class="label">Total KM</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><div class="val">{format_duration(dur_sec)}</div><div class="label">Est. Time</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-card"><div class="val">{len(hazards)}</div><div class="label">Hazards Found</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="stat-card"><div class="val">{route_count}</div><div class="label">Routes Available</div></div>', unsafe_allow_html=True)

    # ── MAP — FULL WIDTH ───────────────────────────────────────────────────────
    st.markdown('<div class="section-head"> Live Route Map</div>', unsafe_allow_html=True)
    with st.spinner("Rendering map..."):
        fmap = build_map(start_ll, end_ll, route_data, hazards, show_alt=show_alternatives)
        st_folium(fmap, width=None, height=520, returned_objects=[])

    # ── ROUTE CARDS + JOURNEY INFO BELOW MAP ──────────────────────────────────
    routes       = route_data.get("routes", [])
    route_labels = ["🟠 Primary Route", "🔵 Alternative A", "🟢 Alternative B"]

    st.markdown('<div class="section-head"> Available Routes</div>', unsafe_allow_html=True)
    route_cols = st.columns(len(routes[:3]))
    for i, r in enumerate(routes[:3]):
        d    = round(r["distance"] / 1000, 1)
        t    = format_duration(r["duration"])
        best = " best" if i == 0 else ""
        with route_cols[i]:
            st.markdown(f"""
            <div class="route-card{best}">
                <div class="route-name">{route_labels[i]}</div>
                <div class="route-meta">{d} km &nbsp;·&nbsp; {t}</div>
            </div>
            """, unsafe_allow_html=True)

    # Journey info bar
    st.markdown(f"""
    <div style='background:#1C1C1C;border:1px solid #2A2A2A;border-radius:8px;padding:14px 18px;
                margin-top:4px;font-size:0.72rem;font-family:Space Mono,monospace;color:#888;
                display:flex;gap:32px;flex-wrap:wrap;align-items:center;'>
        <span><b style='color:#E8E8E8'>FROM</b>&nbsp; {start_name[:60]}{'…' if len(start_name)>60 else ''}</span>
        <span style='color:#FF5A1F'>▶</span>
        <span><b style='color:#E8E8E8'>TO</b>&nbsp; {end_name[:60]}{'…' if len(end_name)>60 else ''}</span>
        <span style='margin-left:auto;color:#FF5A1F'>Updated: {datetime.now().strftime('%H:%M:%S')}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── HAZARD REPORT — FULL WIDTH BELOW MAP ──────────────────────────────────
    st.markdown('<div class="section-head"> Hazard Report</div>', unsafe_allow_html=True)

    if not hazards:
        st.markdown("""
        <div style='border-radius:10px;padding:14px 18px;border-left:4px solid #22C55E;
                    background:rgba(34,197,94,0.1);font-size:0.85rem;'>
            <div style='font-weight:700;margin-bottom:4px;font-size:0.9rem'> No major hazards detected</div>
            <div style='color:#888;font-family:Space Mono,monospace;font-size:0.72rem'>Route appears clear based on OSM data</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Horizontal scrollable strip of hazard cards — full page width
        cards_html = '<div class="hazard-strip">'
        for h in hazards:
            sev       = h["severity"]
            cls       = "alert-danger" if sev == "critical" else "alert-warning" if sev == "high" else "alert-info"
            icon      = "🚫" if sev == "critical" else "⚠️" if sev == "high" else "ℹ️"
            badge_cls = "badge-red" if sev == "critical" else "badge-yellow" if sev == "high" else "badge-blue"
            cards_html += f"""
            <div class="hazard-h-card {cls}">
                <div class="alert-title">{icon} {h['type']}</div>
                <div style='margin:4px 0 6px;font-size:0.78rem;color:var(--text)'>{h['place'][:40]}{'…' if len(h['place'])>40 else ''}</div>
                <div class="alert-meta">
                     {h['km_from_start']} km from start<br>
                    <span class='badge {badge_cls}' style='margin-top:4px;display:inline-block'>{sev}</span>
                </div>
            </div>"""
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)

    # ── ROAD CONDITION IMAGES — inline static OSM tiles ───────────────────────
    if show_images:
        st.markdown('<div class="section-head"> Road Condition Images Along Route</div>', unsafe_allow_html=True)

        coords     = primary["geometry"]["coordinates"]
        sample_pts = sample_route_points(coords, 4)
        img_cols   = st.columns(len(sample_pts))

        for idx, (lon, lat) in enumerate(sample_pts):
            with img_cols[idx]:
                dist  = round(haversine(start_ll[0], start_ll[1], lat, lon), 1)
                place = reverse_geocode(lat, lon)
                # Fetch real OSM tiles, stitch into image, encode as base64 — always visible
                img_b64 = fetch_map_image(lat, lon, zoom=16)
                st.markdown(f"""
                <div class="road-img-card">
                    <img src="{img_b64}" alt="Road at {dist} km"
                         style="width:100%;height:160px;object-fit:cover;display:block;border-radius:10px 10px 0 0"/>
                    <div class="img-info">
                        <div class="place"> {dist} km from start</div>
                        <div class="desc">{place[:48]}{'…' if len(place)>48 else ''}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TURN-BY-TURN STEPS ─────────────────────────────────────────────────────
    with st.expander(" Turn-by-Turn Navigation Steps"):
        steps = primary.get("legs", [{}])[0].get("steps", [])
        if steps:
            for i, step in enumerate(steps[:20]):
                maneuver    = step.get("maneuver", {})
                instruction = maneuver.get("type", "").replace("_", " ").title()
                modifier    = maneuver.get("modifier", "")
                name        = step.get("name") or "unnamed road"
                d           = round(step.get("distance", 0))
                dur         = round(step.get("duration", 0) / 60, 1)
                icon        = "🔄" if "turn" in instruction.lower() else "⬆️" if "straight" in modifier else "↗️"
                st.markdown(f"""
                <div style='padding:8px 12px;border-left:2px solid #2A2A2A;margin:4px 0;font-size:0.82rem'>
                    {icon} <b>{instruction} {modifier}</b> onto <span style='color:#FF5A1F'>{name}</span>
                    <span style='color:#888;font-family:Space Mono,monospace;font-size:0.7rem'> — {d}m · {dur} min</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No step-by-step data available for this route.")

    # ── FULL REPORT DOWNLOAD ───────────────────────────────────────────────────
    st.markdown('<div class="section-head"> Full Report</div>', unsafe_allow_html=True)

    report_text = f"""
ROADMIND AI — ROAD INTELLIGENCE REPORT
Developed by Hovarthan S | An AI Innovator
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

JOURNEY SUMMARY
  From     : {start_input}
  To       : {end_input}
  Distance : {dist_km} km
  Est. Time: {format_duration(dur_sec)}
  Routes   : {route_count} found

{'='*60}
HAZARD ANALYSIS ({len(hazards)} issues found)
{'='*60}
"""
    if not hazards:
        report_text += "\n✅ No road hazards detected along this route.\n"
    else:
        for h in hazards:
            report_text += f"""
⚠  {h['type'].upper()}
   Location : {h['place']}
   Distance : {h['km_from_start']} km from start
   Severity : {h['severity'].upper()}
   Coords   : {h['lat']:.5f}, {h['lon']:.5f}
{'-'*40}
"""

    report_text += f"\n{'='*60}\nAVAILABLE ROUTES\n{'='*60}\n"
    for i, r in enumerate(routes[:3]):
        d = round(r['distance'] / 1000, 1)
        t = format_duration(r['duration'])
        report_text += f"  Route {i+1}: {d} km · {t}\n"

    report_text += f"""
{'='*60}
RoadMap — Make your Journey Easier.
© Copyright 2026 Hovarthan S | All rights reserved
[Generated by RoadMind AI — powered by OpenStreetMap, OSRM, Overpass API]
"""

    st.download_button(
        "⬇️ Download Full Report (.txt)",
        data=report_text,
        file_name=f"roadmind_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=True
    )
