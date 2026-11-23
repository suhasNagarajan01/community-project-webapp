import math
import re
from decimal import Decimal
from accounts.models import WorkerProfile

# Centroids for Bengaluru localities
LOCALITY_COORDINATES = {
    'indiranagar': (12.9784, 77.6408),
    'koramangala': (12.9352, 77.6245),
    'hsr layout': (12.9121, 77.6446),
    'hsr': (12.9121, 77.6446),
    'btm layout': (12.9166, 77.6101),
    'btm': (12.9166, 77.6101),
    'jayanagar': (12.9308, 77.5838),
    'whitefield': (12.9698, 77.7500),
    'marathahalli': (12.9591, 77.6974),
    'electronic city': (12.8399, 77.6770),
    'mg road': (12.9756, 77.6066),
    'central': (12.9716, 77.5946),
    'hebbal': (13.0358, 77.5970),
    'rajajinagar': (12.9982, 77.5530),
    'malleshwaram': (13.0031, 77.5643),
    'ejipura': (12.9392, 77.6276),
    'defence colony': (12.9750, 77.6420),
    'bellandur': (12.9304, 77.6784),
}

def extract_locality_key(text):
    if not text:
        return 'central'
    t = text.lower()
    for key in sorted(LOCALITY_COORDINATES.keys(), key=lambda k: -len(k)):
        if key in t:
            return key
    return 'central'

def haversine_distance(coord1, coord2):
    """Calculates geodesic distance in kilometers between two lat/lon coordinates."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    radius = 6371.0 # Earth radius in km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    # Minimum realistic distance within neighborhood
    return max(0.8, round(distance, 1))

def calculate_distance_between(loc1, loc2):
    k1 = extract_locality_key(loc1)
    k2 = extract_locality_key(loc2)
    c1 = LOCALITY_COORDINATES[k1]
    c2 = LOCALITY_COORDINATES[k2]
    return haversine_distance(c1, c2)

def analyze_location_for_workers(job_location, radius_km, skill=None):
    """
    Analyzes job location against registered workers to find nearby matches
    within the contractor-specified n-km radius.
    Nearby workers are informed first, while the job remains open to all in the platform.
    """
    radius = float(radius_km)
    workers = WorkerProfile.objects.select_related('user').all()
    if skill:
        workers = workers.filter(skills__icontains=skill)

    nearby_matches = []
    other_workers = []

    for w in workers:
        worker_loc = w.user.locality or w.user.city
        dist = calculate_distance_between(job_location, worker_loc)
        item = {
            'worker': w,
            'distance_km': dist,
            'is_within_radius': dist <= radius
        }
        if dist <= radius:
            nearby_matches.append(item)
        else:
            other_workers.append(item)

    nearby_matches.sort(key=lambda x: x['distance_km'])

    # Determine priority match timing based on radius
    if radius <= 3:
        match_timing_minutes = 20
    elif radius <= 5:
        match_timing_minutes = 30
    elif radius <= 10:
        match_timing_minutes = 45
    else:
        match_timing_minutes = 60

    return {
        'nearby_workers': [m['worker'] for m in nearby_matches],
        'nearby_count': len(nearby_matches),
        'total_count': len(workers),
        'radius_km': radius,
        'match_timing_minutes': match_timing_minutes,
        'nearby_matches_data': nearby_matches,
    }
