#from functions.get_files_info import get_files_info
#from functions.get_file_content import get_file_content
#from functions.write_file import write_file
from functions.run_python_file import run_python_file

#def test(test_name, working_directory, directory):
#    print(test_name)
#    print(get_files_info(working_directory, directory))

def test(working_directory, file_path, args=[]):
    #print (f"Result for '{file_path}' file: ")
    #print(get_file_content(working_directory, file_path))
    #print(write_file(working_directory,file_path,content))
    print(run_python_file(working_directory,file_path,args)) 


#test("Result for current directory:","./calculator", ".")
#test("Result for 'pkg' directory:", "./calculator", "pkg")
#test("Result for '/bin' directory:", "./calculator", "/bin")
#test("Result for '../' directory:", "./calculator", "../")
#test("Result for 'lorem.txt' file:", "calculator", "lorem.txt")
#test("calculator", "main.py")
#test("calculator", "pkg/calculator.py")
#test("calculator", "/bin/cat")
#test("calculator", "pkg/does_not_exist.py")
#test("calculator","lorem.txt","wait, this isn't lorem ipsum")
#test("calculator","pkg/morelorem.txt","lorem ipsum dolor sit amet")
#test("calculator","/tmp/temp.txt","this should not be allowed")i

test("calculator","main.py")
test("calculator","main.py",["3 + 5"])
test("calculator","test.py")
test("calculator","../main.py")
test("calculator","nonexistent.py")
test("calculator","lorem.txt")
