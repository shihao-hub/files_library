if __name__ == "__main__":
    try:
        while True:
            user_input = input()
            if user_input.lower() == "exit":
                break
            print(user_input)
    except EOFError:
        pass
