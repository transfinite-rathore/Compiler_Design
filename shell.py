import Sans

while True:
    text = input('Sans> ')
    result, error = Sans.run('<stdin>', text)

    if error:
        print(error.as_string())
    else:
        print(result)

# TARUN
# Abhishek Pandey
# mohan
# Gaurang
# Aishwarya
# push and pull working


# pulled the master branch TARUN_AGRAWAl
