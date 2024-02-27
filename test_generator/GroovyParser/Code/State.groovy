package mypackage

import mypackage.Variable
class State {

    public String receiver = ""
    public String action
    public ArrayList<Variable> output = new ArrayList<Variable>()
    public ArrayList<Identifier> input = new ArrayList<Identifier>()
    public ArrayList<State> child = null

    public void print(level, file) {
        for (def i = 0; i < level; ++i) {
            file.append("\t")
        }

        file.append(this.toString() + '\n')
        if (this.child){
            println(this.child)
            for (State ch : this.child) {
                if (ch)
                    ch.print(level + 1, file)
            }
        }
    }

    public String toString() {
        return String.format('{"Receiver": "%s", "Action": "%s", "Input": %s, "Output": %s, "Child": %s}', 
                            this.receiver,
                            this.action, 
                            this.input, 
                            this.output, 
                            this.child)
        // return String.format('{"Receiver": "%s", "Action": "%s", "Input": %s, "Output": %s}', this.receiver, this.action, this.input, this.output)
    }

    public void setInput(Identifier in){
        this.input = new ArrayList<Identifier>([in])
    }

    public void setInput(ArrayList<Identifier> in) {
        this.input = in
    }
    
    public void setOutput(Identifier out){
        this.output = new ArrayList<Identifier>([out])
    }

    public void setOutput(ArrayList<Identifier> out) {
        this.output = out
    }

    public void setChild(ArrayList<State> ch) {
        this.child = ch
    }
    
    public void setChild(State ch){
        this.child = new ArrayList<State>([ch])
    }
    
}
