
#######################################################################
# pwgrab 1.2
#
#  Designed to extract a single password from a user/password data file                          
#                                                                            
#  NOTE: this program was designed to read passwords in a certain format, as follows
#                       firstName lastName
#                       \n
#                       Login Name: *******
#                       Password: ***********
#                       \n
#                       \n
#                       \n
#             As long as the login and passwords are on the 2nd and 3rd lines
#             respective to firstName lastName, it will be able to be read correctly
#
#  TO DO:
#             Add error handling for invalid file types
#             Add more information to debug function
#             Fix the not enough lines error
#
#  Known Issues:
#             If a file has less than 4 or 5 lines of text, program will throw an error
#             Trying to read certain file types causes issues, anything that isnt a text file
#             See: TO DO
#
#  1.2 Changes:
#             Fixed case handling for last name entries
#             Changed login/password output to original lines from read file
#
# @ Tristan Staso                                                              
#######################################################################

import glob, argparse
global gv 
gv = "\npwgrab 1.2 (Oct 15 2018)" #current version
def version():
    print(gv)

def debug(info,argsf):
    if len(info[0]) > 0:
        print("\nFiles read by " + str(ret))
        for i in range(len(info[0])):
            print("     -" + str(info[0][i]))
    else:
        print("\nNo files read.")
    if info[1][0] > 1:
        print("\n" + str(info[1][0]) + " total lines read.")
    if len(info[2]) > 0:
        for i in range(len(info[2])):
            last, num, fileName = info[2][i]
            print("User '" + str(last) + "' found on line " + str(num) + " in " + str(fileName))
    arg_str = str(argsf)
    print("\nARGUMENTS")
    print(arg_str[10:][:-1])
    print(gv)

def print_block(store,select):
    print("")
    for i in range(len(store[0])):
        print(store[select][i],end="")
    print("")
def ret(lname,debugvar,argsf):
    store = []
    new = []
    debug_list = [[] for i in range(4)]
        # list of debug variables to output if debug argument is passed
        #[0] = # of files read w/ file name
        #[1] = # total number of lines read
        #[2] = names found and their respective line number and where they were found
        #[3] = user arguments
    #for i in range(1,len(args)):
        #print(args[i])
    lines_read = 0
    if(lname[0].islower()):
        lname = lname[0].upper() + lname[1:]
    ftype = "*." + str(argsf.fileType)
    lname = lname[0] + lname[1:].lower()
    if argsf.fileName:
        target = [argsf.fileName]
    else:
        target = glob.glob(ftype)
    for f in target:
        file = open(f)
        if debugvar:
            debug_list[0].append(file.name)
        for num, line in enumerate(file,1):
            lines_read+=1
            if lname in line.replace("\n","").split(" "):
                if debugvar:
                    found = lname, num, file.name
                    debug_list[2].append(found)    
                new.append(line)
                new.append("\n")
                temp = open(f)
                for i, j in enumerate(temp,1):
                    limit = num + 4
                    if i == num + 2:
                        new.append(j)
                    if i == num + 3:
                        j = j.replace("\n","")
                        new.append(j)
                    if i > limit:
                        break
                store.append(new)
                new = []
    if len(store) > 1:
        multiple_instance(store,lname)
    elif len(store) == 1:
        print_block(store,0)
    else:
        print("User not found.")
    if debugvar:
        debug_list[1].append(lines_read)
        debug(debug_list,argsf)

def multiple_instance(store,last):
    print("Multiple instances of user '" + str(last) + "' found.")
    for i in range(len(store)):
        print(str(i+1) + ") " + str(store[i][0][:-1] + " | " + str(store[i][2][:-1])))
    print("Select one. Enter 0 to cancel.")
    ipt = -1
    while ipt > len(store) or ipt <= 0:
        try:
            ipt = int(input("> ")) 
            if ipt > len(store) or ipt < 0:
                print("Please enter a value between 1 and " + str(len(store)) + ". Enter 0 to cancel.")
            elif ipt == 0:
                break
            else:
                print_block(store,ipt-1)
        except:
            print("Please enter a value between 1 and " + str(len(store)) + ". Enter 0 to cancel.")

F_MAP = {"debug" : debug, "version" : version, "ret" : ret}

def main():
    ipt_parse = argparse.ArgumentParser(description="Retrieve and output user passwords."
                                        ,usage="pwgrab <lastName> [fileName] [fileType] {args}")
    ipt_parse.add_argument("-version",dest="command",action="store_const",const="version"
                           ,help="Display current version")
    ipt_parse.add_argument("-debug",dest="debug",action="store_true"
                           ,help="Information regarding file type, location, and program data")
    ipt_parse.add_argument("lastName",type=str,nargs='?'
                           ,help="Users last name, case insensitive")
    ipt_parse.add_argument("-t",dest="fileType",type=str, nargs=1,default="prt"
                           ,help="Specify a custom file type.")
    ipt_parse.add_argument("fileName",type=str, nargs='?',default=None
                           ,help="Specify a file.")
    #ipt_parse.add_argument("ret",action="store_false",help="Retrieve stored user password: pwgrab ret <lastName>")
    argsf, unknown = ipt_parse.parse_known_args()
    debugvar=argsf.debug
    if argsf.command:
        func = F_MAP[argsf.command]
        func()
    elif argsf.lastName:
        ret(argsf.lastName,debugvar,argsf)
    else:
        print("Usage: pwgrab <lastName> [fileName] [fileType] {args}\nType 'pwgrab -h' for help")
        
main()



