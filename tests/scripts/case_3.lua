local API = rawget(_G, "API")
assert(API, "error: main module is not pre-loaded")

for _ = 1, 10e4 do
  local ascii = math.random(65, 90) -- A-Z
  local success, result = pcall(function()
    return API.increment(string.char(ascii))
  end)
  assert(not success, "Expected API.increment to fail on invalid input")
end