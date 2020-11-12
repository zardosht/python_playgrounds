import subprocess

"""
Using subprocess module we can call external commands from Python 
and if needed we can also capture the output of those commands, 
or even pipe the output of one command to another. 

"""

"""
# Add shell=True, if you get an error for 
# FileNotFound. This happens if you run a command that is built-in
# in shell, like "ls"

# This runs the command and prints the output on the stdout. 
"""
# subprocess.run("ls", shell=True)

"""
With shell=True we can give the entire command as a string, 
including the arguments. 

!! Beware that with shell=True is a security hazard. If an untrusted  
string is passed as command. 
!! Don't run it with use input.  
"""
# subprocess.run("ls -la", shell=True)


"""
If we are not using shell=True, we cannot pass the entire command 
as a string. 
Instead we have to pass everything as list
"""
# subprocess.run(["ls", "-al"])

"""
Simply running the command, prints out the result on the stdout, like a
python script. 
This is because we are not capturing the stdout of the command; it goes
just where ever the stdout of the command normally goes, which is the 
terminal normally. 
"""

"""
this won't put the output into p1 as you might have thought
instead the p1 is an instance of CompletedProcess object. 
"""
# p1 = subprocess.run(["ls", "-al"])
# print(p1)

"""
We can do cool stuff with the CompletedProcess object, 
like getting its passed arguments, or getting its return code. 
"""
# print(p1.args)
# print(p1.returncode)

"""
If we try to print the p1.stdout, we get None
This is because we hadn't captured the stdout of the process. 
"""
# print(p1.stdout)


"""
Now we capture the stdout 
First, the command does not print anything to the terminal. 

"""

## Does not work in Python 3.6. Only from 3.7 above :(
# p1 = subprocess.run(["ls", "-al"], capture_output=True)

"""
Capture the output in Python 3.6 using PIPE

Notice the now we don't see anything in terminal. 
Instead, p1.stdout gives us the stdout of the process now. 
"""
# p1 = subprocess.run(["ls", "-al"], stdout=subprocess.PIPE)
# print(p1.stdout)

"""
Notice that the stdout is captured as bytes, not as string.
We can call decode() on it to get the string. 

We can also pass an argument to subprocess.run() and say we want 
text instead of bytes from stdout. 
"""
# p1 = subprocess.run(["ls", "-al"], stdout=subprocess.PIPE)
# print(p1.stdout.decode())

## Works only in Python 3.7 above. 
# p1 = subprocess.run(["ls", "-al"], capture_output=True, text=True)
# print(p1.stdout)

"""
We can redirect the stdout to other places as well. For example, 
let's say we want to redirect it to a file, for example for logging. 

For that, we can simply open up a file, and redirect the stdout to it. 
"""
# with open("output.txt", "w") as outfile:
#     p1 = subprocess.run(["ls", "-al"], stdout=outfile)




"""
How to handle errors? 

Note that an error on the external program does not raise an exception
in Python. Instead the p1 will have a non-zero error code. 

In Python 3.7 above, if we capture_output=True the stderr is also PIPEd. 
In 3.6 below, the stderr is printed on default stderr. 

So the below code writes the error on terminal, and p1.stdout will be 
empty, and the p1.stderr will be None. 
"""
# p1 = subprocess.run(["ls", "-al", "a_non_existing_file.txt"], 
#                     stdout=subprocess.PIPE)
# print(p1.returncode)
# print(p1.stdout)
# print(p1.stderr)

"""
Instead the following code will redirect the stderr as well, 
and p1.stderr contains the error. 
"""
# p1 = subprocess.run(["ls", "-al", "a_non_existing_file.txt"], 
#                     stdout=subprocess.PIPE, 
#                     stderr=subprocess.PIPE)
# print(p1.returncode)
# print(p1.stderr)

"""
So in order to check if the command was successfull or not, we have 
to check the return code.  
"""
# p1 = subprocess.run(["ls", "-al", "a_non_existing_file.txt"], 
#                     stdout=subprocess.PIPE, 
#                     stderr=subprocess.PIPE)
# if p1.returncode != 0:
#     print("An Error occurred: Error Code: ", p1.returncode)
#     print(p1.stderr.decode())


"""
If we want Python to throw an exception instead, if an error occurs, 
we should set check=True.
Then the Python throws a CalledProcessError exception. 

"""
# p1 = subprocess.run(["ls", "-al", "a_non_existing_file.txt"], 
#                     stdout=subprocess.PIPE, 
#                     stderr=subprocess.PIPE, 
#                     check=True)


"""
We can also redirect the stderr (or stdout) to /dev/null
The p1.stderr will be None then. 
"""
# p1 = subprocess.run(["ls", "-al", "a_non_existing_file.txt"], 
#                     stdout=subprocess.PIPE, 
#                     stderr=subprocess.DEVNULL)
# print(p1.stderr)


""" 
We can also change the input to the command. 
For example, imagine we want to take the output of one command, 
and have that to be the input of another.  

For example let's cat the content of a file, and then pass its output
to grep. 
"""
# p1 = subprocess.run(["cat", "sub_processes/test.txt"], 
#                     stdout=subprocess.PIPE, 
#                     stderr=subprocess.PIPE)

# print("p1 cat; return code: ", p1.returncode)
# print(p1.stdout.decode())


# p2 = subprocess.run(["grep", "-n", "test"],
#                     input=p1.stdout,
#                     stdout=subprocess.PIPE, 
#                     stderr=subprocess.PIPE)

# print("p2 grep; return code: ", p2.returncode)
# print(p2.stdout.decode())

""" 
Of course if we want to use shell=True, we could also pass everything
as one command with pipe. (which is not as fun of course :D)
"""
# p1 = subprocess.run("cat sub_processes/test.txt | grep -n test",
#                     stdout=subprocess.PIPE, 
#                     stderr=subprocess.PIPE, 
#                     shell=True)

# print(p1.stdout)




