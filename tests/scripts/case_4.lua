local API = rawget(_G, "API")
assert(API, "error: main module is not pre-loaded")

function ascii_shift(x, c)
  return string.char(string.byte(c) + x)
end 

for _ = 1, 100 do
  local x = math.random(-20, 20)
  assert(API.call(ascii_shift, x, "A") == ascii_shift(x, "A"), string.format("call: invalid result"))
  assert(API.call_typedef(ascii_shift, x, "A") == ascii_shift(x, "A"), string.format("call_typedef: invalid result"))
end

for _ = 1, 10e4 do
  local n = math.random(-1e4, 1e4)
  assert(API.call_2(API.increment, n) == n + 1, "call_2: invalid result")
end