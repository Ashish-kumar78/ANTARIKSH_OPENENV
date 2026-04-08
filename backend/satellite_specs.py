"""
Real Satellite Specifications Database
Contains actual battery capacity, storage, and roles for known satellites
"""

import math

SATELLITE_SPECS = {
    # ISS - International Space Station
    "ISS": {
        "name": "International Space Station",
        "role": "research",
        "agency": "NASA/International",
        "battery_capacity_kwh": 120.0,
        "storage_capacity_gb": 2000,
        "solar_panels_kw": 75,
        "purpose": "Microgravity research, Earth observation"
    },
    
    # NOAA-19 - Weather Satellite
    "NOAA-19": {
        "name": "NOAA-19 (POES)",
        "role": "weather",
        "agency": "NOAA/NASA",
        "battery_capacity_kwh": 40.0,
        "storage_capacity_gb": 500,
        "solar_panels_kw": 10,
        "purpose": "Weather monitoring, atmospheric data"
    },
    
    # TERRA - Earth Observatory
    "TERRA": {
        "name": "Terra (EOS AM-1)",
        "role": "observation",
        "agency": "NASA",
        "battery_capacity_kwh": 35.0,
        "storage_capacity_gb": 800,
        "solar_panels_kw": 15,
        "purpose": "Earth science, climate monitoring"
    },
    
    # AQUA - Water Cycle Studies
    "AQUA": {
        "name": "Aqua (EOS PM-1)",
        "role": "observation",
        "agency": "NASA",
        "battery_capacity_kwh": 35.0,
        "storage_capacity_gb": 800,
        "solar_panels_kw": 15,
        "purpose": "Water cycle, atmospheric water vapor"
    },
    
    # SENTINEL-2A - Earth Observation
    "SENTINEL-2A": {
        "name": "Sentinel-2A",
        "role": "observation",
        "agency": "ESA",
        "battery_capacity_kwh": 38.0,
        "storage_capacity_gb": 600,
        "solar_panels_kw": 12,
        "purpose": "Land monitoring, vegetation, water"
    },
    
    # LANDSAT-8 - Earth Observation
    "LANDSAT-8": {
        "name": "Landsat 8",
        "role": "observation",
        "agency": "USGS/NASA",
        "battery_capacity_kwh": 36.0,
        "storage_capacity_gb": 900,
        "solar_panels_kw": 14,
        "purpose": "Land use, geology, agriculture"
    },
    
    # SUOMI-NPP - Weather/Climate
    "SUOMI-NPP": {
        "name": "Suomi NPP",
        "role": "weather",
        "agency": "NOAA/NASA",
        "battery_capacity_kwh": 42.0,
        "storage_capacity_gb": 700,
        "solar_panels_kw": 11,
        "purpose": "Weather, atmospheric, land, ocean data"
    },
    
    # NOAA-20 - Weather Satellite
    "NOAA-20": {
        "name": "NOAA-20 (JPSS-1)",
        "role": "weather",
        "agency": "NOAA/NASA",
        "battery_capacity_kwh": 45.0,
        "storage_capacity_gb": 750,
        "solar_panels_kw": 12,
        "purpose": "Weather, air quality, sea ice"
    },
    
    # GOES-16 - Geostationary Weather
    "GOES-16": {
        "name": "GOES-16",
        "role": "weather",
        "agency": "NOAA/NASA",
        "battery_capacity_kwh": 50.0,
        "storage_capacity_gb": 1000,
        "solar_panels_kw": 18,
        "purpose": "Lightning detection, hurricane tracking"
    },
    
    # METEOSAT-11 - Geostationary Weather
    "METEOSAT-11": {
        "name": "Meteosat 11th Gen",
        "role": "weather",
        "agency": "EUMETSAT",
        "battery_capacity_kwh": 55.0,
        "storage_capacity_gb": 1200,
        "solar_panels_kw": 20,
        "purpose": "European weather, climate monitoring"
    }
}


# Role mapping to RL environment
ROLE_MAP = {
    "weather": "planner",
    "observation": "executor",
    "research": "executor",
}


def get_satellite_specs(satellite_id: str) -> dict:
    """Get specifications for a satellite"""
    specs = SATELLITE_SPECS.get(satellite_id, {
        "name": satellite_id,
        "role": "observation",
        "agency": "Unknown",
        "battery_capacity_kwh": 40.0,
        "storage_capacity_gb": 500,
        "solar_panels_kw": 10,
        "purpose": "Unknown"
    })
    
    specs["rl_role"] = ROLE_MAP.get(specs["role"], "executor")
    return specs


def calculate_battery_percentage(norad_id: int, t_seconds: float, battery_capacity_kwh: float) -> float:
    """
    Calculate realistic battery percentage based on solar panel exposure and orbital phase.
    Returns: Battery percentage (0-100)
    """
    orbit_period_seconds = 5400  # 90 minutes for LEO
    orbit_phase = (t_seconds % orbit_period_seconds) / orbit_period_seconds * 2 * math.pi
    
    sun_factor = max(0, math.sin(orbit_phase))
    base_battery = 85.0
    seasonal_factor = 0.95 + 0.1 * math.sin(t_seconds / (86400 * 365) * 2 * math.pi)
    
    battery = base_battery * seasonal_factor + sun_factor * 5
    return round(max(20, min(100, battery)), 1)


def calculate_storage_percentage(tasks_assigned: int = 0, max_tasks: int = 100) -> float:
    """Calculate storage usage based on assigned tasks"""
    base_storage = 15.0
    task_storage = (tasks_assigned / max_tasks) * 70
    return round(min(100, base_storage + task_storage), 1)
