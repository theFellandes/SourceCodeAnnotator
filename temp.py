import javalang
from javalang.tree import CompilationUnit

source_code = """
/**
* test
* 1234
**/
class HelloWorldApp {
/**
AAAAA
**/
    public static void main(String[] args) {
        hashmap map = new hashmap();
        var testing = 0;
        int testing2 = 0;
        testing = testing2;
        System.out.println("Hello World!"); // Display the string.
    }
    
    /**
BBBBB
**/
    public static void main(String[] args) {
        hashmap map = new hashmap();
        var testing = 0;
        int testing2 = 0;
        testing = testing2;
        System.out.println("Hello World!"); // Display the string.
    }
}
"""

tree: CompilationUnit = javalang.parse.parse(source_code)

print(tree)

# for path, node in tree:
    # print(path)
    # print()
    # print(node)
    # print("\n\n\n")
#
# for path, node in tree.filter(javalang.tree.ClassDeclaration):
#     print(path, node)