# breadmake (cli tool)

`breadmake` is a cli build tool to replace most simple use cases of GNU
`make`. It was not build with things like cache, speed, etc in mind. It was
created to simplify `Makefile` systems with a lot of `bash` conditional
statements. Most of the complex functions of a `Makefile` are deferred to the
shell, therefore it should be capable of the same things `make` can do.
