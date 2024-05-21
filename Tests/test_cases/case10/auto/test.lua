-- Function to test inc(short int) function
function test_inc()
    for i = -100, 10000 do
        if CFunction.inc(i) ~= i + 1 then
            print("Test failed for inc(short int) function with input: " .. i)
            print("Result: " .. CFunction.inc(i))
            return false
        end
    end
    return true
end


-- Function to test square(short int) function
function test_square()
    for i = -100, 181 do
        if CFunction.square(i) ~= i*i then
            print("Test failed for square(short int) function with input: " .. i)
            print("Result: " .. CFunction.square(i))
            return false
        end
    end
    return true
end

-- Function to test add(short int, short int) function
function test_add()
    for i = -100, 10000 do
        for j = -100, 1000 do
            if CFunction.add(i, j) ~= i + j then
                print("Test failed for add(short int, short int) function with input: " .. i .. " " .. j)
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
