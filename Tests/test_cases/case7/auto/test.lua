function randomLetter()
    randomNumber = math.random(65, 90)
    return string.char(randomNumber)
end

function randomString()
    local length = math.random(1, 5)
    local str = ""
    for i = 1, length do
        str = str .. randomLetter()
    end
    return str
end

-- Function to test identity(char*) function
function test_identity()
    for i = 1, 10000 do
        x = randomString()
        if CFunction.identity(x) ~= x then
            print("Test identity(char*) failed for input: " .. x)
            print("Result: " .. CFunction.identity(x))
            return false
        end
    end
    return true
end

function min_string(a, b)
    if a < b then
        return a
    else
        return b
    end
end

-- Function to test min_string(char*, char*) function
function test_min_string()
    for i = 1, 10000 do
        x = randomString()
        y = randomString()
        if CFunction.min_string(x, y) ~= min_string(x, y) then
            print("Test min_string(char*, char*) failed for input: " .. x .. " " .. y)
            print("Result: " .. CFunction.min_string(x, y))
            return false
        end
    end
    return true
end


if test_identity() and test_min_string() then
    io.stderr:write("true\n")
else
    io.stderr:write("false\n")
end
