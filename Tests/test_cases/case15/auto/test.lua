-- Function to test sub function which shouldn't be imported
function test_sub()
    if CFunction.sub then
        print("Test failed - function sub shouldn't be imported")
        return false
    else
        return true
    end
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

if test_sub() and test_add() then
    io.stderr:write("true\n")
else
    io.stderr:write("false\n")
end
