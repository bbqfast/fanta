#"WindowWidth"=dword:00000680
#"WindowHeight"=dword:000003a8

python_code = __import__('training-2')
reload(python_code)

python_code.begin()        