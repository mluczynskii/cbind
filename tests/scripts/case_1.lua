local API = rawget(_G, "API")
assert(API, "error: main module is not pre-loaded")

for _ = 1, 10e4 do
  local n = math.random(-1e4, 1e4)
  assert(API.increment(n) == n + 1, "increment: invalid result")
end

for _ = 1, 10e4 do
  local ascii = math.random(65, 90) -- A-Z
  assert(API.foo(1, string.char(ascii)) == string.char(ascii+1), "foo: invalid result")
end