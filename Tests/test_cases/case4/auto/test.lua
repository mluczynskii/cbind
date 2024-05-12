function numerator(xs)
    return xs[1]
end

function test_numerator()
    for i = 0, 100 do
        for j = 1, 100 do
            xs = {i, j}
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
    return a[1] * b
end

function test_multiply()
    for i = 1, 1000 do
        for j = 100, 2000 do
            if CFunction.multiply({i}, j) ~= multiply({i}, j) then
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