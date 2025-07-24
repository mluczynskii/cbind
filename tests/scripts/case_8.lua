local API = rawget(_G, "API")
assert(API, "error: main module is not pre-loaded")

local werewolf = API.monster_t.new()
local green_int = API.RGB.GREEN
werewolf:set_fur_color(API.RGB.GREEN)
assert(werewolf:get_fur_color() == API.RGB.GREEN)
assert(werewolf:get_years_lived() == green_int)