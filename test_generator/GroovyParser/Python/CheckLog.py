with open("Log/log.txt", "r") as file:
    content = file.read()

if 'We missed' in content:
    print("Something strange happens")
else:
    print("Run complete successfully")