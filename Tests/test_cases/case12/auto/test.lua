function randomFloat()
    return 1 + (1000 - 1) * math.random()
end

local epsilon = 0.1

-- Function to test div(double, double) function
function test_div()
    for i = 1, 1000 do
        x = randomFloat()
        y = randomFloat()
        if math.abs(CFunction.div(x, y) - x/y) > epsilon then
            print("Test failed for div(double, double) function with input: " .. x .. " " .. y)
            print("Result: " .. CFunction.div(x, y))
            return false
        end
    end
    return true
end

-- Function to test mult(double, double) function
function test_mult()
    for i = 1, 1000 do
        x = randomFloat()
        y = randomFloat()
        if math.abs(CFunction.mult(x, y) - x*y) > epsilon then
            print("Test failed for mult(double, double) function with input: " .. x .. " " .. y)
            print("Result: " .. CFunction.mult(x, y))
            return false
        end
    end
    return true
end



if test_div() and test_mult() then
    io.stderr:write("true\n")
else
    io.stderr:write("false\n")
end
