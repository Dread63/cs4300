def main():
    integer = 5
    floating_point = 5.75
    string = "Architecture"
    boolean = False

    for x in range (0, 10):
        integer = integer * 2

    print(integer)

    floating_point = floating_point * (5.5765)
    print(floating_point)

    string = string + " is super important!"
    print(string)

    string = string.replace("s", "X")
    print(string)

    for _ in range(0, 10):

        if not boolean:
            print("Statement True!")
        else:
            print("Statement False!")
        boolean = not boolean

if __name__ == "__main__":
    main()