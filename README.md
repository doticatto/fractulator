# FRACTULATOR
Welcome to the **FRACTULATOR**. John Mahoney's personal foray into a command line fraction calculator.
Yes, he could have used the built in Python fraction and greatest common denominator / least common multiple functionality but that felt like cheating.
  
The fractulator is designed to be a simple tool to use, and it is very much so if you follow a few simple rules.

## Setup
* First of all, make sure you `chmod +x fractulator.py` to make it executable.  
* In order to avoid having to escape all of your `*` characters, run `set -f` before using the tool

## Usage 
* Fractulator makes it easy to run command line fraction operations.
* The following operations are supported:
  * `+` (Addition)
  * `-` (Subtraction)
  * `*` (Multiplication)
  * `/` (Divison)  
* Here is an example:
    * `./fractulator.py 6/3 + 14/2 * 19/17`
    * Examples with `*` assume you have run `set -f` beforehand
    
* Fractulator supports whole numbers and mixed numbers as well:
    * `./fractulator.py 3 * 2_1/4`
    * Syntax for a mixed number is `whole_numerator/denominator`
    
* When dealing with negative fractions, put the minus sign as the first character in the fraction, or you will receive a parsing error:
    * `./fractulator.py -4/3 + -2_5/6`

* The output will be a whole number, mixed number, or fraction depending on what the result simplifies to
    * `./fractulator.py 6/3 + 14/2 * 19` outputs `135`
    * `./fractulator.py 16/17 * 18/19` outputs `288/323`
    * `./fractulator.py 16/17 + 18/19` outputs `1_287/323`

* When an invalid input is supplied, you will receive the error reason in the output and the help text will be displayed
    * `./fractulator.py 16/17 @ 18/19`  
`Invalid input: 16/17 @ 18/19, @ is not a valid operator`
    * `./fractulator.py 16/17 * 18q/19`  
      `Invalid fraction input: 18q/19`
      
* Have fun with fraculator! All of the methods are well documented so if you find yourself needing a non-standard 
  fraction library for Python go right ahead and do as you please with it!
  
Thank you!
- John
