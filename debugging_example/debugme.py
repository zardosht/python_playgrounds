import debugging_example.helper as helper



def do_something(var):
    var = 3
    print(var)
    helper.do_something_else(var)

def main():
    var = 2
    do_something(var)
    foo = 15
    do_something(foo)


if __name__ == "__main__":
    print("hello")
    main()


