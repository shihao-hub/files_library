with open("zip_test.txt","r") as file:
    with open("zip_test_out.zip","wb") as fp:
        exec(f"output = {file.read()}")
        fp.write(locals()["output"])