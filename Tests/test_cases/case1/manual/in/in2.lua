function foo(x)
    for i = 0, x do
        io.write(CFunction.inc(i))
    end
    print()
end


foo(4)
foo(5)
