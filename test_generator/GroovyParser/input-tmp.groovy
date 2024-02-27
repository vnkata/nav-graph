path = "abcd"
dummy = 0
def ar = new int[3];
ar[3] = "abcd"
ar[5] = 5
ar[10] = WebUI.doSomething("has string",10)
test = WebUI.doSomething(5,test1,"string")
alo = WebUI.callTestCase(path,dummy)
WebUI.click(alo)
alo = WebUI.callTestCase(path,ar[5])
WebUI.click(alo)
WebUI.click(button + path)

for (int i = 0; i < 10; ++i){
    WebUI.callTestCase(alo)
    WebUI.click()
    // WebUI.doSomething()
}

switch(doSomething()) {
    case a:
        doAnotherThing()
        break
    case b:
        doSomethingElse()
        break
    default:
        hello()
        break
}

switch(astring){
    case 'asda':
        doSomething()
        break
    default:
        doNothing()
        break
}

try {
    def arr = new int[3];
    arr[3] = "abcd"
    arr[5] = 5
    arr[10] = WebUI.doSomething("has string",10)
    test = WebUI.doSomething(5,test1,"string")
} catch(Exception ex) {
    println("Catching the exception");
}
finally {
    sleep()
}

for (int i =0;i<a.length;++i){
    a[i] = i+1
}
// // switch(doSomething()) {
// //     case a:
// //         doAnotherThing()
// //         break
// //     case b:
// //         doSomethingElse()
// //         break
// //     default:
// //         hello()
// //         break
// // }

// // try {
// //     def arr = new int[3];
// //     arr[5] = 5;
// // } catch(Exception ex) {
// //     println("Catching the exception");
// // }
// // finally {
// //     sleep()
// // }
// // GlobalVariable.name = 'Hellos'