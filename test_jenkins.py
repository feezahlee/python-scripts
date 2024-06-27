file_content = "this is just for testing"
file_path = "/var/lib/jenkins/testfile.txt"

# Writing to the file
with open(file_path, 'w') as file:
    file.write(file_content)

print(f"File created successfully at: {file_path}")
