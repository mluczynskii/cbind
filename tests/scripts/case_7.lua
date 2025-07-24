local API = rawget(_G, "API")
assert(API, "error: main module is not pre-loaded")

local red, green, blue = API.RGB.RED, API.RGB.GREEN, API.RGB.BLUE 
local black, magenta = API.CMYK.BLACK, API.CMYK.MAGENTA 

assert(
  API.is_black(black) == 1
  and API.is_black(magenta) == 0
)
assert(
  API.color_char(red) == "R"
  and API.color_char(green) == "G" 
  and API.color_char(blue) == "B"
)
assert(
  API.char_color("R") == red 
  and API.char_color("G") == green 
  and API.char_color("B") == blue
)