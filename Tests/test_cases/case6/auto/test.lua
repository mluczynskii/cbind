function randomLetter()
    randomNumber = math.random(65, 90)
    return string.char(randomNumber)
end

-- Function to test identity(char) function
function test_identity()
    for i = 1, 10000 do
        x = randomLetter()
        if CFunction.identity(x) ~= x then
            print("Test identity(char) failed for input: " .. x)
            print("Result: " .. CFunction.identity(x))
            return false
        end
    end
    return true
end

function min_char(a, b)
    if a < b then
        return a
    else
        return b
    end
end

-- Function to test min_char(char, char) function
function test_min_char()
    for i = 1, 10000 do
        x = randomLetter()
        y = randomLetter()
        if CFunction.min_char(x, y) ~= min_char(x, y) then
            print("Test min_char(char, char) failed for input: " .. x .. " " .. y)
            print("Result: " .. CFunction.min_char(x, y))
            return false
        end
    end
    return true
end


if test_identity() and test_min_char() then
    io.stderr:write("true\n")
else
    io.stderr:write("false\n")
end
