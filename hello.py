print("=====================================")
print("Welcome here")
print("My first post!")
print("=====================================")


username = input("Enter your username: ")
age = int(input("Enter your age: "))
category = input("Enter your category: ")

print("\nInstagram Profile")
print("====================")
print("Username:", username)
print("Age:", age)
print("Category:", category)

if age >40 and category == "fun":
    print("You are quite old, what is fun for you???")