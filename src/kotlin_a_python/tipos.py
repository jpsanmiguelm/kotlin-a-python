# edad: int = "hola"
# print(edad)


def saludo(nombre: str | None) -> str:
    if nombre is None:
        return "ANONYMOUS"
    return nombre


print(saludo("juan"))
print(saludo(None))


def greet(name: str) -> str:
    return f"Hi {name}"


print(greet("Sanmi"))


def ageType(age: int) -> str:
    if age >= 18:
        return "Adult"
    elif age >= 13:
        return "teen"
    else:
        return "kid"


print(ageType(20))
print(ageType(15))
print(ageType(10))


def checkNull(name: str | None) -> str:
    if name is not None:
        print(f"Juanis tiene {len(name)} letras")
        return f"Has a name: {name}"
    if name is None:
        return "Has no name"


print(checkNull("Juanis"))
print(checkNull(None))


def isAdult(age: int) -> str:
    return "adult" if age >= 18 else "minor"


print(isAdult(18))
print(isAdult(1))


def greet2(name: str | None) -> str:
    return name.upper() if name is not None else "ANONYMOUS"


print(greet2("juan"))
print(greet2(None))
