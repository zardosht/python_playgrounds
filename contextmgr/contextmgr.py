# class OpenFile():
#     def __init__(self, filename, mode):
#         self.filename = filename
#         self.mode = mode

#     def __enter__(self):
#         self.file = open(self.filename, self.mode)
#         return self.file

#     def __exit__(self, exc_type, exc_val, traceback):
#         self.file.close()



# with OpenFile("sample.txt", "w") as f:
#     f.write("Testing")


# print(f.closed)




# #### Using contextlib ####
# # This is equivalent to using the class
# # Everything up to yield statement is equivalent to __enter__ method of the context manager class above. 
# # At the yield the code withint the with statement is going to run
# # Everything after the yield method is equivalent to __exit__ method of our context manager class.

# from contextlib import contextmanager

# @contextmanager
# def open_file(file, mode):
#     f = open(file, mode)
#     yield f
#     f.close()


# with open_file("sample.txt", "w") as f:
#     f.write("aaaa bbb ccc ddd eee fff ggg hhh iii jjj")

# print(f.closed)



#### Using contextlib  with error handling ####
# Put the setup code (everything before yield statement) and the yield statement 
# itself into a try block
# Put the tear down code (everthing after yield statement) into a finally block. 


# from contextlib import contextmanager

# @contextmanager
# def open_file(file, mode):
#     try:
#         f = open(file, mode)
#         yield f
    
#     finally:
#         f.close()


# with open_file("sample.txt", "w") as f:
#     f.write("aaaa bbb ccc ddd eee fff ggg hhh iii jjj")

# print(f.closed)

#
# ============================================
# 
# A practical example: 

import os
import contextlib

# We can replace something like the below code: 

## setup
# cwd = os.getcwd()
# os.chdir("dir1")

## work
# print(os.listdir())

## teardown
# os.chdir(cwe)

## doing the above multiple times: 
# cwd = os.getcwd()
# os.chdir("dir2")
# print(os.listdir())
# os.chdir(cwe)

# ---------------------------------------------
# Using Context Manager to something like below: 

from contextlib import contextmanager

@contextmanager
def change_dir(destination):
    try: 
        cwd = os.getcwd()
        os.chdir(destination)
        yield
    
    finally:
        os.chdir(cwd)


for dest in ["dir1", "dir2"]:
    with change_dir(dest):
        print(os.listdir())

