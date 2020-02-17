# pygrab
Simple password retrieval tool in python

  Designed to extract a single password from a user/password data file                          
                                                                            
  NOTE: this program was designed to read passwords in a certain format, as follows
  >                     firstName lastName
  >                     \n
  >                     Login Name: *******
  >                     Password: ***********
  >                     \n
  >                     \n
  >                     \n
As long as the login and passwords are on the 2nd and 3rd lines
respective to firstName lastName, it will be able to be read correctly

##  TO DO
Add error handling for invalid file types
Add more information to debug function
Fix the not enough lines error

##  Known Issues
If a file has less than 4 or 5 lines of text, program will throw an error
Trying to read certain file types causes issues, anything that isnt a text file

See: TO DO

##  1.2 Changes
Fixed case handling for last name entries
Changed login/password output to original lines from read file
