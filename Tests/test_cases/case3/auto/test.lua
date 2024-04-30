function inc(x)
    return x + 1
end

function square(x)
    return x * x
end

-- Test for apply function
function test_apply()
    for i = 0, 100 do
        if CFunction.apply(i, inc) ~= i + 1 then
            print("Test failed for apply function with callback inc(x),  input: " .. i)
            return false
        end

        if CFunction.apply(i, square) ~= i * i then
            print("Test failed for apply function with callback square(x), input: " .. i)
            return false
        end
    end
    return true
end

function foo()
    return 42
end

-- Test for execute function
function test_execute()
    if CFunction.execute(CFunction.foo) ~= 42 then
        print("Test failed for execute function with callback CFunction.foo()")
        return false
    end

    if CFunction.execute(foo) ~= 42 then
        print("Test failed for execute function with callback foo()")
        return false
    end
    return true
end

-- Test for inc_and_apply function
function test_inc_and_apply()
    for i = 0, 100 do
        if CFunction.inc_and_apply(i, inc) ~= i + 2 then
            print("Test failed for inc_and_apply function with callback inc(x), input: " .. i)
            return false
        end
        if CFunction.inc_and_apply(i, square) ~= (i + 1) * (i + 1) then
            print("Test failed for inc_and_apply function with callback square(x), input: " .. i)
            return false
        end
    end
    return true
end

if test_apply() and test_execute() and test_inc_and_apply() then
    io.stderr:write("true\n")
else
    io.stderr:write("false\n")
end