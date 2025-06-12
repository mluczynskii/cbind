local API = rawget(_G, "API")
assert(API, "error: main module is not pre-loaded")

for _ = 1, 10e4 do
  local a = math.random(-1e3, 1e3)
  local b = math.random(-1e3, 1e3)
  local p = API.pair_t.new(a, b)
  assert(API.sum(p) == a + b, "sum: invalid result")
end