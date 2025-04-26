MODEL gpt-image-1
BACKGROUND transparent
MODERATION low
QUALITY high
SIZE 1024x1024

PROMPT Create a clean top-down 2D sprite on a fully transparent background, rendered at the stated pixel dimensions so every asset aligns perfectly with the city-grid scale; use crisp, slightly stylized flat-shaded colors with subtle texture noise for asphalt or building roofs, soft antialiased edges, and a gentle overhead noon light that casts minimal shadow directly beneath the object; isolate exactly one subject per file with no extra elements, ensure all strokes and highlights remain inside the canvas to avoid bleed, and keep the style consistent across roads, buildings, vehicles and decorative tiles so they can be dynamically layered without seams or palette clashes.

ASSET road_straight_ns.png A seamless 256×256-pixel top-down tile portraying a straight north-to-south stretch of dark-gray asphalt with two single-lane directions divided by a crisp dashed yellow center line, clean white shoulder lines, subtle mottled texture and faint tire scuffs, edges feathering into full transparency so the sprite can butt vertically against duplicates without visual seams.

ASSET road_straight_ew.png A 256×256-pixel east-to-west road tile identical in style to the north-south variant but rotated to run left–right, preserving the dashed yellow center stripe, white edge lines and gentle surface noise, engineered for perfect horizontal tiling on a transparent background.

ASSET road_corner_ne.png A 256×256-pixel ninety-degree bend that carries traffic from south to east, showing smoothly curved dashed center markings, lane-edge stripes that widen toward the outer radius, tiny gutter drains at the outer curb and micro-chips in the asphalt, all rendered top-down with antialiased curves and transparent outside corners so the piece nests flush against adjacent straight tiles.

ASSET road_corner_nw.png A mirrored twin of the northeast corner bending south-to-west, retaining the same lane markings, curb drains and texture, laid out for seamless alignment with north-south and west-east straights, stored as a transparent PNG.

ASSET road_corner_se.png A clockwise curve turning north-to-east, sharing identical visual treatment and resolution with the other corner tiles, crafted for plug-and-play placement in the grid network.

ASSET road_corner_sw.png A counter-clockwise bend turning north-to-west with the same dashed center arc, edge lines and subtle grit, completing the full set of corner assets for intersection construction.

ASSET road_intersection_4way.png A 256×256-pixel four-way crossroad featuring intersecting dashed center lines, zebra-stripe crosswalks at each curb, tiny stop-line bars, evenly spaced sewer grates in the corners and a neutral transparent border that lets sidewalks or buildings butt directly against the paving.

ASSET road_intersection_t_north.png A T-junction where the stem opens southward into an east-west through-road, complete with lane arrows showing permitted left-or-right turns, full dashed center markings, reflective raised dots at the merge point and crosswalks on all three sides, delivered as a transparent PNG.

ASSET road_intersection_t_south.png The southern mirror of the previous tile, stem opening northward, exhibiting identical markings, arrows and surface details adapted to the opposite orientation for quick tiling.

ASSET road_intersection_t_east.png A T-junction whose stem opens westward into a north-south through-road, matching visual language and resolution, ready for rotation-free placement.

ASSET road_intersection_t_west.png A T-junction whose stem opens eastward into a north-south through-road, rounding out the directional T-set with consistent markings and texture.

ASSET building_car_store.png A 256×256-pixel top-down sprite showing a single-lot glass-fronted car showroom with a bold red “CAR STORE” roof sign, two roll-up garage doors, a tiny forecourt with three striped parking bays and a subtle shadow to give volume, bordered by a narrow sidewalk but otherwise transparent.

ASSET building_repair_garage.png An overhead 256×256-pixel asset of a brick repair garage featuring a broad roller door, rooftop AC units, a painted wrench icon on the asphalt apron and an oil-stained driveway, everything else transparent so it snaps into the street grid.

ASSET building_gas_station.png A compact 256×256-pixel filling station with two covered pumps, a small kiosk, bright canopy lights and painted lane arrows guiding cars through, rendered in crisp vector style with transparent margins.

ASSET building_car_wash.png A 256×256-pixel drive-through car-wash bay outlined by blue foam brushes, dripping water animations baked into the texture and an illuminated “WASH” sign on the roof, transparent outside the structure footprint.

ASSET building_taxi_stand.png A 256×256-pixel yellow-roofed kiosk marked “TAXI” with a sheltered curb lane, striped pickup zone and a glowing call button pad, pavement blended into transparent background for modular placement.

ASSET building_police_station.png A 256×256-pixel municipal building with navy-blue roof, a silver badge emblem, two reserved police-car bays painted on the asphalt and a short antenna mast, drawn in flat clean lines atop transparency.

ASSET building_police_academy.png A tucked-away 256×256-pixel low-profile brick structure bearing a discreet “ACADEMY” plaque, small training course cones on one side and muted color palette to keep it semi-hidden among regular blocks, transparent elsewhere.

ASSET building_mechanic_garage.png A darker 256×256-pixel industrial unit with corrugated roof, prominent gear-and-spanner logo on top, side ventilation fans and a grease-stained driveway, designed to fit flush against any road tile.

ASSET building_drive_thru_restaurant.png A 256×256-pixel fast-food outlet with a wrap-around drive-thru lane, bright billboard menu board, red-tiled roof and a single service window, road entry and exit rendered but transparent beyond the square footprint.

ASSET building_auction_house.png A 256×256-pixel civic hall with banner reading “CAR AUCTION”, twin flagpoles, a small queue lane marked in faded yellow and a hammer-icon skylight, finished with transparent gutters for seamless city placement.

ASSET building_detailing_station.png A 256×256-pixel shiny-silver shed with giant foamy sponge logo, open bay doors revealing blue detailing mats, hose reels coiled on the side wall and polished concrete apron, everything else transparent.

ASSET building_used_car_dealership_showroom.png A 256×256-pixel diagonal-glass showroom with bright pennant strings on the roof, a row of three color-coded spotlights shining on an empty forecourt and a bold “USED CARS” banner, transparent ground beyond the lot edge.

ASSET building_warehouse_depot.png A 256×256-pixel gray warehouse with roll-up cargo door, yellow safety bollards, rooftop skylights and pallet stacks painted just inside, perimeter fading to transparency.

ASSET building_residential_block.png A neutral 256×256-pixel four-story apartment block with rooftop garden patches, repeating balcony texture, small entrance canopy and subtle AC condensers, outside margins transparent for decorative filling of city blocks.

ASSET building_office_block.png A 256×256-pixel glass-and-steel office tower segment with mirrored curtain walls, rooftop chiller units and a simple lobby awning, rendered in soft pastel tones and transparent beyond the square footprint.

ASSET building_city_park.png A 256×256-pixel green space tile with neatly trimmed lawn, two crossing footpaths, a central fountain ringed by benches and three stylized trees casting elliptical shadows, outer edges transparent so parks can tessellate.

ASSET car_compact_generic.png A 96×48-pixel top-down sprite of a compact silver sedan with black tinted windows, soft highlight reflection along the hood, circular wheel wells, neutral license plate and no brand markings, fully anti-aliased and saved on transparency for easy palette swaps.

ASSET car_taxi.png A 96×48-pixel bright-yellow sedan sprite sharing the compact silhouette but sporting a small roof-mounted “TAXI” light box, checkerboard side stripe and subtle wear grime, rendered cleanly over a transparent background.

ASSET car_police.png A 96×48-pixel patrol sedan sprite with monochrome white-on-black livery, roof-bar red-blue light cluster, minimalist shield emblem on the doors and steely gray wheels, all pixels trimmed to transparency outside the body.

ASSET van_delivery.png A 112×56-pixel box van sprite in neutral white with sliding side door outline, twin rear doors, gray bumpers and small roof clearance marker lights, drawn from the same strict top-down angle and delivered with transparent backdrop.

ASSET car_salvage_rusty.png A 96×48-pixel battered sedan sprite in faded teal with scattered rust blotches, cracked windshield spider-webbing, a missing hubcap and dull headlight lenses, designed for auction or repair scenarios and saved on transparency.
