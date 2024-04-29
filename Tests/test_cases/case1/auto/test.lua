-- Function to test increment function
function test()
    for i = 1, 10000 do
        if CFunction.inc(i) ~= i + 1 then
            print("Test increment failed for input: " .. i)
            return false
        end
    end

    for i = 1, 100 do
        local x = math.random(100000, 10000000)
        if CFunction.inc(x) ~= x + 1 then
            print("Test increment failed for input: " .. x)
            return false
        end
    end
    return true
end

if test() then
    io.stderr:write("true\n")
else
    io.stderr:write("false\n")
end
