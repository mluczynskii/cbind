# cbind

A toolchain written in python used to automatically generate C binding for Lua based on AST (*Abstract Syntax Tree*) created by the `gcc` compiler.

## Usage/Examples

Given an API with a set of functions written in C, we want to create an additional `.c` source file that will allow `.lua` scripts to call these functions. Let's assume our API is in `api.c`:

- **Creating the AST**

```bash
gcc -c -fdump-tree-original-raw api.c
```

- **Parsing the AST into `dump.json`**

```bash
python3 cbind/parser.py api.c.005t.original
```

- **Turning the parsed AST into a `binding.c` source file**

```bash
python3 cbind/main.py dump.json -o binding.c
```

The generated source file provides an interface for running scripts in Lua: `init_lua`, `exec_script` and `close_lua`. An example of using this interface can be found in `tests/src/main.c`. Last thing to do is compiling everything into the final binary - see `Makefile`

## Dependencies

Whole project was developed and tested on versions listed below, but it's very likely that it will run on some older ones.

- python-3.13.2
- gcc-14.2.1
- [libffcall-2.4](https://www.gnu.org/software/libffcall/)
- [Lua-5.4.7](https://www.lua.org/download.html) (the C API)

## Running Tests

To run tests, run the following command inside the `test` directory.

```bash
bash validate.sh
```

## Contributing

Since this is a solo project and I am just a student, all contributions are very welcome.
