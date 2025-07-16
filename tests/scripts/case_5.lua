-- case_5: nested data-types and returning a struct
local API = rawget(_G, "API")
assert(API, "error: main module is not pre-loaded")

for _ = 1, 10e4 do
  local x, y = math.random(-1e3, 1e3), math.random(-1e3, 1e3)
  local player = API.player_t.new(API.pair_t.new(x, y), 100)
  local off_x, off_y = math.random(-10, 10), math.random(-10, 10)
  local new_player = API.move_player(player, API.pair_t.new(off_x, off_y))
  assert(
    player:get_position():get_first() + off_x == new_player:get_position():get_first()
    and player:get_position():get_second() + off_y == new_player:get_position():get_second(),
    "move_player: failed to update player's coordinates correctly!"
  )
  assert(
    player:get_health() == new_player:get_health(),
    "move_player: unexpected change to player's health!"
  )
end

for _ = 1, 10e4 do 
  local player = API.player_t.new(API.pair_t.new(-1, 12), 100)
  local damage = math.random(0, 200)
  local new_player = API.take_damage(player, damage)
  assert(
    player:get_position():get_first() == new_player:get_position():get_first()
    and player:get_position():get_second() == new_player:get_position():get_second(),
    "take_damage: unexpected change to player's coordinates!"
  )
  assert(
    math.max(0, player:get_health() - damage) == new_player:get_health(),
    "take_damage: failed to update player's health correctly!"
  )
end 