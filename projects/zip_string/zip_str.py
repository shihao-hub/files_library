with open("zip_test.zip", "rb") as file:
    for line in file:
        fp = open("zip_test.txt", "w")
        fp.write(str(line))
        fp.close()
        break

