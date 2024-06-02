local path = "test_cases/case14/auto/"

function sleep(n)
    os.execute("sleep " .. tonumber(n))
end

function print_one()
    os.execute("echo '1' >> " .. path .. "in")
end

function clean_input_file()
    os.execute("echo '' > " .. path .. "in")
end

function compare_files(file1, file2)
    local f1 = io.open(file1, "r")
    local f2 = io.open(file2, "r")

    if not f1 or not f2 then
        if f1 then f1:close() end
        if f2 then f2:close() end
        print("Can not open file")
        return false
    end

    local content1 = f1:read("*all")
    local content2 = f2:read("*all")

    f1:close()
    f2:close()

    return content1 == content2
end
  
clean_input_file()
CFunction.add_function(print_one, 0)
sleep(3.5)
CFunction.delete_function(0)
sleep(3)

local are_equal = compare_files(path .. "in", path .. "out")

if are_equal then
    io.stderr:write("true\n")
else
    io.stderr:write("false\n")
end
