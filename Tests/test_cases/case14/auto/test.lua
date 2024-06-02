-- Function to test square function
function test_square()
    for i = 1, 10000 do
        if CFunction.square(i) ~= i*i then
            print("Test failed for square function with input: " .. i)
            print("Result: " .. CFunction.square(i))
            return false
        end
    end

    return true
end

-- Function to test add function
function test_add()
    for i = 1, 1000 do
        for j = 1, 1000 do
            if CFunction.add(i, j) ~= i + j then
                print("Test failed for add function with input: " .. i .. " + " .. j)
                print("Result: " .. CFunction.add(i, j))
                return false
            end
        end
    end

    return true;
end

if test_square() and test_add() then
    io.stderr:write("true\n")
else
    io.stderr:write("false\n")
end
