#Only for flares > M1

from sunpy.net import Fido
from sunpy.net import attrs as a

event_type = 'FL'
tstart = '2021/02/14'
tend = '2025/02/28'
#tend = '2021/06/25'
result = Fido.search(a.Time(tstart,tend), a.hek.EventType(event_type), a.hek.FL.GOESCls > 'M1.0', a.hek.OBS.Observatory == "GOES")
#print(result.show('hpc_bbox','refs'))
hek_results = result["hek"]
filtered_results = hek_results["event_starttime","event_endtime"]

#for flare in filtered_results:
    #print(f"This flare started at {flare['event_starttime']} and ended at {flare['event_endtime']}")
filtered_results.write("goes_feb_2021_to_feb_2025_flares", format="csv")