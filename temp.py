def foo(files,count):
    foo_helper(files,count)

def foo_helper(files,count):
    if count == 0:
        return
    files.append(count)
    foo_helper(files,count-1)


files = []
foo(files,3)
print("Files: ",files)