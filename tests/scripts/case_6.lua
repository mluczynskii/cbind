local API = rawget(_G, "API")
assert(API, "error: main module is not pre-loaded")

local n = API.wrap(5, API.ctype.INT)
assert(API.unwrap(n) == 5)
API.funny(n)
assert(API.unwrap(n) == 2137)
assert(API.dereference(n) == 2137)

local ptr = API.grab_ptr()
assert(API.dereference(ptr) == 420)