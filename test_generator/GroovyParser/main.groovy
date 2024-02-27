import mypackage.Constant
import mypackage.Identifier
import mypackage.Variable
import mypackage.NodeVisitor

import org.codehaus.groovy.ast.ASTNode
import org.codehaus.groovy.ast.builder.AstBuilder
import groovy.json.JsonOutput
import static groovy.io.FileType.FILES



def baseDir = new File("Data");
def filePath = [];
baseDir.traverse(type: FILES, maxDepth: 0) { filePath.add(it) };

AstBuilder builder = new AstBuilder();
for (String name : filePath){
	File file = new File(name)
	String fileContent = file.text
    String[] lines = fileContent.split('\n')
    for (int i = 0; i < lines.length; ++i){
        if (lines[i]){
            //lines[i] = lines[i].strip()
            if (lines[i].length() < 6)
                continue
            print(lines[i].substring(0, 6))
            if (lines[i].substring(0, 6).equals("import")){
                print("\n")
                lines[i] = ''
            }
        }
    }
    fileContent = String.join('\n', lines)
    print(fileContent)

	def ast = builder.buildFromString(fileContent)
    def states = new ArrayList<State>()
    for (def node : ast) {
        states += NodeVisitor.visitNode(node)
    }

    def outPath = name.replace("Data", "Output").replace(".groovy", ".txt")
    def out = new File(outPath)
    out.write("")

    for (def state : states) {
        if (state)
            //state.print(0, out)
            out.append(state.toString() + '\n')
    }   
}