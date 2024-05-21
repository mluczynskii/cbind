-- Function to test return_ten, square functions
function test()
    for i = 1, 10000 do
        if CFunction.square(i) ~= i*i then
            print("Test failed for square function with input: " .. i)
            print("Result: " .. CFunction.square(i))
            return false
        end
    end

    for i = 1, 100 do
        x = math.random(100, 10000)
        expected = (x + 10)*(x + 10)
        if CFunction.square(CFunction.return_ten() + x) ~= expected then
            print("Test failed for square function with return_ten, input: " .. x)
            print("Result: " .. CFunction.square(CFunction.return_ten() + x))
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
