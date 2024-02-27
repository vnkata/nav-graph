# Groovy Parser

This parser parse input test script into tree structure

For building: Run the following command

    make build

For running: Put all Groovy script into Data folder and run this command

    make run

The output is written in Output folder with the corresponding name

## Format

For an identifier (Variable, Constant, Statement)

    {"type": "Variable", "name": "a", "datatype": "int"}
    {"type": "Constant", "value": "123", "datatype": "int"}
    {"type": "Statement", "code": "1 == 2"}

For a test step:

    a = WebUI.doSomething(123)
    {
        "receiver": "WebUI",
        "action": "doSomething",
        "input":[{"type": "Constant", "value": "123", "datatype": "int"}],
        "output": [{"type": "Variable", "name": "a", "datatype": "Object"}]
    }

If step A is inside the block of step B, it is denoted by a tab at the begining of the line

    if (1 < 2 )
        doSomething()
    else
        doSomethingElse()

    <If statement>
        <doSomething statement>
    <Else Statement>
        <doSomethingElse statment>
