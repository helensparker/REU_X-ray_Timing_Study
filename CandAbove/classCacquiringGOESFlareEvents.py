from sunpy.net import Fido
from sunpy.net import attrs as a

event_type = 'FL'
tstart = '2021/02/14'
tend = '2025/02/28'
result = Fido.search(a.Time(tstart,tend), a.hek.EventType(event_type), a.hek.FL.GOESCls > 'C1.0', a.hek.OBS.Observatory == "GOES")
hek_results = result["hek"]
filtered_results = hek_results["event_starttime","event_endtime"]

filtered_results.write("classCandAbovegoes_feb_2021_to_feb_2025_flares", format="csv")