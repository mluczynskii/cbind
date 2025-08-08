local API = rawget(_G, "API")
assert(API, "error: main module is not pre-loaded")

local GRID_SIZE = API.get_grid_size()
local red = API.get_default_color()
local blue = API.color_t.new(0, 0, 255, 255)

function pattern_1(x, y)
  if x == 0 or x == GRID_SIZE - 1 then return 1
  elseif y == 0 or y == GRID_SIZE - 1 then return 1
  else return 0 end
end

function pattern_2(x, y)
  local posx, posy = API.get_posx(), API.get_posy()
  if math.abs(x - posx) + math.abs(y - posy) == 1 then 
    return 1
  else 
    return 0
  end
end 

function set_pattern_1()
  API.set_attack_color(red)
  local _ = API.set_attack_pattern(pattern_1)
end 

function set_pattern_2()
  API.set_attack_color(blue)
  local _ = API.set_attack_pattern(pattern_2)
end 

set_pattern_1()
set_pattern_2()
