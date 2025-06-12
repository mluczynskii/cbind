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

for _ = 1, 10e4 do 
  local a = math.random(-255, 255)
  local b = math.random(-1e4, 1e4) 
  local c = math.random(-1e8, 1e8) 
  local d = math.random() * 100
  local result = API.simple_num(a, b, c, d)
  local expected = a + b + c + d 
  assert(result <= expected + 8 and result >= expected - 8, "simple_num: invalid result")
end