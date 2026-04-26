--- SOURCE INTENT (design-spec.json) ---
{
  "project": {
    "structure_type": "Pergola",
    "shape": "Hexagon"
  },
  "dimensions": {
    "height_total_ft": 10.5,
    "max_diagonal_ft": 10.0
  },
  "materials": {
    "post_size": "6x6"
  },
  "site": {
    "location": "Saanich, BC",
    "canonical_location_id": "BC_SAANICH"
  },
  "style": {
    "joinery_preference": "Traditional mortise and tenon",
    "hardware": "Minimal to none, traditional all-wood joinery",
    "post_bases": "Concrete pier blocks with standoffs"
  }
}


--- ENGINEERED PHYSICS (structural-model.json) ---
{
  "members": {
    "posts": { "quantity": 6, "dimensions": "6x6", "cutLength_ft": 8.33, "spanDistance_ft": 5.0 },
    "beams": { "quantity": 6, "dimensions": "4x8", "depth_in": 7.25 },
    "hipRafters":  { "quantity": 6, "dimensions": "4x6" }
  },
  "roofStructure": { "pitch": "4:12" },
  "overhang_in": 12,
  "_locked": false
}


--- GENERATED OUTPUT 1 (blueprint-plan.svg) ---
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
<!-- COORDINATE MAP: scale=42px/ft, grade_y=640, post_top_y=290, apex_y=195 -->
<!-- TOPOLOGY_SKIP -->
<rect width="1000" height="1000" fill="white"/>
<text x="50" y="50" font-family="monospace" font-size="20">PLAN VIEW - 10' HEXAGON</text>
<text x="50" y="80" font-family="monospace" font-size="16">Pitch: 4:12</text>
<text x="50" y="110" font-family="monospace" font-size="16">Miter: 28.7° / Bevel: 9.1°</text>
<!-- Post Representations -->
<rect x="500" y="200" width="20" height="20" fill="#c8a96e" stroke="black"/>
<rect x="760" y="350" width="20" height="20" fill="#c8a96e" stroke="black"/>
<rect x="760" y="650" width="20" height="20" fill="#c8a96e" stroke="black"/>
<rect x="500" y="800" width="20" height="20" fill="#c8a96e" stroke="black"/>
<rect x="240" y="650" width="20" height="20" fill="#c8a96e" stroke="black"/>
<rect x="240" y="350" width="20" height="20" fill="#c8a96e" stroke="black"/>
<!-- Beams -->
<polygon points="510,210 770,360 770,660 510,810 250,660 250,360" fill="none" stroke="black" stroke-width="4"/>
</svg>


--- GENERATED OUTPUT 2 (blueprint-isometric.svg) ---
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
<!-- COORDINATE MAP: scale=42px/ft, grade_y=640, post_top_y=290, apex_y=195 -->
<!-- TOPOLOGY_SKIP -->
<rect width="1000" height="1000" fill="white"/>
<text x="50" y="50" font-family="monospace" font-size="20">ISOMETRIC VIEW - 10' HEXAGON</text>
<text x="50" y="80" font-family="monospace" font-size="16">Pitch: 4:12</text>
<text x="50" y="110" font-family="monospace" font-size="16">Miter: 28.7° / Bevel: 9.1°</text>
<!-- Simple Wireframe Projection -->
<polygon points="500,200 650,250 650,400 500,450 350,400 350,250" fill="none" stroke="black" stroke-width="2"/>
<line x1="350" y1="250" x2="350" y2="600" stroke="black" stroke-width="2"/>
<line x1="650" y1="250" x2="650" y2="600" stroke="black" stroke-width="2"/>
<line x1="500" y1="450" x2="500" y2="800" stroke="black" stroke-width="2"/>
</svg>


