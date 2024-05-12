function numerator(xs)
    return xs["x"]
end

function test_numerator()
    for i = 0, 100 do
        for j = 1, 100 do
            xs = {}
            xs["x"] = i
            xs["y"] = j
            if CFunction.numerator(xs) ~= numerator(xs) then
                print("Test failed for numerator function, input: i = " .. i .. ", j = " .. j)
                print("Result: " .. CFunction.numerator(xs) .. ", expected: " .. numerator(xs))
                return false
            end
        end
    end
    return true
end

function multiply(a, b)
    return a["val"] * b
end

function test_multiply()
    for i = 1, 1000 do
        for j = 100, 2000 do
            arr = {}
            arr["val"] = i
            if CFunction.multiply(arr, j) ~= multiply(arr, j) then
                print("Test failed for multiply function, input: i = " .. i .. ", j = " .. j)
                return false
            end
        end
    end
    return true
end

if test_numerator() and test_multiply() then
    io.stderr:write("true\n")
else
    io.stderr:write("false\n")
end