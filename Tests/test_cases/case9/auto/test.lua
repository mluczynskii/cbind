-- Function to test inc(long int) function
function test_inc()
    for i = -100, 10000 do
        if CFunction.inc(i) ~= i + 1 then
            print("Test failed for inc(long int) function with input: " .. i)
            print("Result: " .. CFunction.inc(i))
            return false
        end
    end

    for i = 1, 100 do
        local x = math.random(100000, 10000000)
        if CFunction.inc(x) ~= x + 1 then
            print("Test failed for inc(long int) function with input: " .. i)
            print("Result: " .. CFunction.inc(x))
            return false
        end
    end
    return true
end


-- Function to test square(long int) function
function test_square()
    for i = -100, 10000 do
        if CFunction.square(i) ~= i*i then
            print("Test failed for square(long int) function with input: " .. i)
            print("Result: " .. CFunction.square(i))
            return false
        end
    end
    return true
end

-- Function to test add(long int, long int) function
function test_add()
    for i = -100, 1000 do
        for j = -100, 1000 do
            if CFunction.add(i, j) ~= i + j then
                print("Test failed for add(long int, long int) function with input: " .. i .. " " .. j)
                print("Result: " .. CFunction.add(i, j))
                return false
            end
        end
    end
    return true
end



if test_inc() and test_square() and test_add() then
    io.stderr:write("true\n")
else
    io.stderr:write("false\n")
end
