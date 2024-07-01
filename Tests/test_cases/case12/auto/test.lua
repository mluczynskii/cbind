function randomFloat()
    return 1 + (1000 - 1) * math.random()
end

local epsilon = 0.1

-- Function to test my_div(double, double) function
function test_my_div()
    for i = 1, 1000 do
        x = randomFloat()
        y = randomFloat()
        if math.abs(CFunction.my_div(x, y) - x/y) > epsilon then
            print("Test failed for my_div(double, double) function with input: " .. x .. " " .. y)
            print("Result: " .. CFunction.div(x, y))
            return false
        end
    end
    return true
end

-- Function to test my_mult(double, double) function
function test_my_mult()
    for i = 1, 1000 do
        x = randomFloat()
        y = randomFloat()
        if math.abs(CFunction.my_mult(x, y) - x*y) > epsilon then
            print("Test failed for my_mult(double, double) function with input: " .. x .. " " .. y)
            print("Result: " .. CFunction.mult(x, y))
            return false
        end
    end
    return true
end



if test_my_div() and test_my_mult() then
    io.stderr:write("true\n")
else
    io.stderr:write("false\n")
end
