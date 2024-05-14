require "binding"

function increment(x) do
    return x+1
end

function decrement(x) do
    return x+1
end

function test_counter() do
    x = 0
    cnt = {}
    cnt["val"] = 0
    for i = 1,2000 do
        if i % 5 == 0 then
            x = decrement(x)
            CFunction.decrement(cnt)
        else
            x = increment(x)
            CFunction.increment(cnt)
        end
        if x ~= cnt["val"] then
            print("Test failed for counter structure, input: i = " .. i)
            return false
        end
    end
    return true
end
    
if test_counter() then
    io.stderr:write("true\n")
else
    io.stderr:write("false\n")
end