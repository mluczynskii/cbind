local API = rawget(_G, "API")
assert(API, "error: main module is not pre-loaded")

function ascii_shift(x, c)
  return string.char(string.byte(c) + x)
end 

for _ = 1, 10e4 do
  local x = math.random(-20, 20)
  local call, key_a = API.call(ascii_shift, x, "A")
  local call_typedef, key_b = API.call_typedef(ascii_shift, x, "A")
  assert(call == ascii_shift(x, "A"), string.format("call: invalid result"))
  assert(call_typedef == ascii_shift(x, "A"), string.format("call_typedef: invalid result"))
  API.delete_callback(key_a)
  API.delete_callback(key_b)
end

for _ = 1, 10e4 do
  local n = math.random(-1e4, 1e4)
  local call_2, _ = API.call_2(API.increment, n)
  assert(call_2 == n + 1, "call_2: invalid result")
end