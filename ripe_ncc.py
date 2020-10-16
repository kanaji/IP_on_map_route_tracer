from datetime import datetime
from ripe.atlas.cousteau import (
  Ping,
  Traceroute,
  AtlasSource,
  AtlasCreateRequest
)

ATLAS_API_KEY = ""

ping = Ping(af=4, target="www.google.gr", description="testing new wrapper")

traceroute = Traceroute(
    af=4,
    target="www.ripe.net",
    description="testing",
    protocol="ICMP",
)

source = AtlasSource(type="area", value="WW", requested=5)

atlas_request = AtlasCreateRequest(
    start_time=datetime.utcnow(),
    key=ATLAS_API_KEY,
    measurements=[ping, traceroute],
    sources=[source],
    is_oneoff=True
)

(is_success, response) = atlas_request.create()