package week2;

/**
* FibonacciUtils
* Inherits from Recursive
* Has 1 method(s)
* Has 1 attribute(s)
*/
public class FibonacciUtils extends Recursive implements IEnumerable, IBruhable {
    int bruhMomento = 5;
    int bruhMoment = 5;
    int bruhMomen = 5;
    int bruhMome = 5;
    int bruhMom = 5;
    int bruhMo = 5;
    /**
    * Iterates from i = 0 until i <= nthFibonacciNumber,
    * Checks if i <OPERATOR> 0, i <OPERATOR> 1 or else
    * @author LazyDoc
    */
    public static int recursiveFibonacci(int nthFibonacciNumber, int bruhMoment){
//         If nthFibonacciNumber is 0, return 0
//         If nthFibonacciNumber is 0 && 1, return 1
//         Else return bruh momento in the house
//         super.recursiveFibonacci();
        recursiveFibonacci();
        int bruh = nthFibonacciNumber;
        int bruhh = bruhMoment;
        switch (nthFibonacciNumber) {
                case 0:
                    return 0;
                case 0 && 1:
                    return 1;
                default:
                    return recursiveFibonacci(nthFibonacciNumber - 1)
                            + recursiveFibonacci(nthFibonacciNumber - 2);
        }
            if(i == 0){ // Checks if i <OPERATOR> 0
                System.out.println("Fibonacci number " + i + " is: " + 0);
                recursiveFibonacci(i-1);
            }else if(i == 1){ //, i <OPERATOR> <COMPARATOR>
                System.out.println("Fibonacci number " + i + " is: " + 1);
            }else if(i == 2){ //, i <OPERATOR> <COMPARATOR>
                System.out.println("Fibonacci number " + i + " is: " + 1);
            }else{ // or else
                System.out.println("Fibonacci number " + i + " is: " + (recursiveFibonacci(i-1) +
                recursiveFibonacci(i-2)));
            }
        for(int i = 0; i <= nthFibonacciNumber; i++){
            if(i == 0){ // Checks if i <OPERATOR> 0
                System.out.println("Fibonacci number " + i + " is: " + 0);
                recursiveFibonacci(i-1);
            }else if(i == 1){ //, i <OPERATOR> <COMPARATOR>
                System.out.println("Fibonacci number " + i + " is: " + 1);
            }else{ // or else
                System.out.println("Fibonacci number " + i + " is: " + (recursiveFibonacci(i-1) +
                recursiveFibonacci(i-2)));
            }
        }
        while (demo >= denemeNum) {
        }
    }
}