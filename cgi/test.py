import sys
filename = "C:\\Users\\Lector\\source\\repos\\Server-KN-P-222\\cgi\\Python.png"
with open(filename, "rb") as file :
        sys.stdout.buffer.write(b"Content-Type: image/png\n\n")
        sys.stdout.buffer.write(file.read())