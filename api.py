from skyfield.api import Loader, load
from skyfield.data import mpc
from skyfield.constants import GM_SUN_Pitjeva_2005_km3_s2 as GM_SUN
import spiceypy as spice
from datetime import datetime, timedelta

# de421.bsp is also provided offline
# load = Loader('/tmp')

# loads ephemeris files over internet
planets = load('de421.bsp')

# source: ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp/de421.bsp
spice.furnsh('de421.bsp')
# source: https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/latest_leapseconds.tls
spice.furnsh('latest_leapseconds.tls')
# source: https://sppgway.jhuapl.edu/lpredict_ephem
spice.furnsh('spp_nom_20180812_20250831_v037_RO4.bsp')

# load minor planets/comets database over internet
# not need since neowise is not shown anymore
#with load.open(mpc.COMET_URL) as f:
#    comets = mpc.load_comets_dataframe(f)

# comets = comets.set_index('designation', drop=False)

# loads time scale files over internet
ts = load.timescale()

def f2i(arr):
    return [[int(x), int(y), int(z)] for x,y,z in arr]

def get_current_position(planet):
    return list(planets[planet].at(ts.now()).ecliptic_xyz().km)

def get_positions(planet, days_before, days_after, step=24):
    now = ts.now()
    x, y, z = planets[planet].at(ts.utc(now.utc.year,
                                        now.utc.month,
                                        now.utc.day,
                                        range(now.utc.hour+days_before*24,
                                              now.utc.hour+days_after*24,
                                              step),
                                        now.utc.minute,
                                        now.utc.second)).ecliptic_xyz().km
    coords = list()
    for xc, yc, zc in zip(x, y, z):
        coords.append([xc, yc, zc])
    return f2i(coords)

def get_mpc_current_position(designation):
    row = comets.loc[designation]
    coords = list()
    comet = planets['sun'] + mpc.comet_orbit(row, ts, GM_SUN)
    x, y, z = comet.at(ts.now()).ecliptic_xyz().km
    return [x, y, z]


def get_mpc_positions(designation):
    row = comets.loc[designation]
    coords = list()
    comet = planets['sun'] + mpc.comet_orbit(row, ts, GM_SUN)
    now = ts.now()
    x, y, z = comet.at(ts.utc(now.utc.year, now.utc.month, range(now.utc.day-30, now.utc.day+30))).ecliptic_xyz().km
    for xc, yc, zc in zip(x, y, z):
        coords.append([xc, yc, zc])
    return f2i(coords)


def get_psp_current_position():
    tspy = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    ts = spice.utc2et(tspy)
    pos, lt = spice.spkezp(-96, ts, 'ECLIPJ2000', 'NONE', 0)
    x, y, z = pos
    return [x, y, z]


def get_psp_positions(from_days, to_days, step=24):
    now = datetime.now()
    coords = list()
    for i in range(from_days*24, to_days*24, step):
        tspy = (now + timedelta(hours=i)).strftime('%Y-%m-%dT%H:%M:%S')
        ts = spice.utc2et(tspy)
        # -96 is the ID of PSP
        pos, lt = spice.spkezp(-96, ts, 'ECLIPJ2000', 'NONE', 0)
        x, y, z = pos
        coords.append([x, y, z])
    return f2i(coords)
