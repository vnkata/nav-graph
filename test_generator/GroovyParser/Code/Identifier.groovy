package mypackage

import groovy.json.*

class Identifier {
    public String id
    Identifier() {

    }

    Identifier(String id) {
        this.id = id
    }
}

class Constant extends Identifier{
    public String value;
    public String datatype;

    Constant() {
        super("Constant")
    }

    Constant(String value, String type) {
        super("Constant")
        this.value = value
        this.datatype = type
    }

    Constant(String value) {
        super("Constant")
        this.value = value
        this.datatype = "string"
    }

    public String toString() {
        return String.format('{"type": "%s", "value": "%s", "datatype": "%s"}', 
                        super.id.toString().replace('"', "'"), 
                        this.value.toString().replace('"', "'"), 
                        this.datatype.toString().replace('"', "'"))
    }
}

class Variable extends Identifier{
    public String name
    public String datatype

    Variable() {
        super("Variable")
    }

    Variable(String name, String varType) {
        super("Variable")
        this.name = name;
        this.datatype = varType
    }
    
    Variable(String name) {
        super("Variable")
        this.name = name
        this.datatype = ""
    }

    public String toString() {
        return String.format('{"type": "%s", "name": "%s", "datatype": "%s"}', 
                        super.id.toString().replace('"', "'"), 
                        this.name.toString().replace('"', "'"), 
                        this.datatype.toString().replace('"', "'"))
    }
}

class Statement extends Identifier {
    public String code
    Statement() {
        super("Statement")
    }

    public String toString() {
        return String.format('{"type": "%s", "code": "%s"}', 
                    super.id.toString().replace('"', "'"), 
                    this.code.toString().replace('"', "'"))
    }
}