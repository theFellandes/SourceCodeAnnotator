package week2;

public class FibonacciUtils extends Recursive {
    /**
    * Iterates from i = 0 until i <= nthFibonacciNumber,
    * Checks if i <OPERATOR> 0, i <OPERATOR> 1 or else
    * @author LazyDoc
    */
    public static int recursiveFibonacci(int nthFibonacciNumber){
        super.recursiveFibonacci();
//             if(i == 0){ // Checks if i <OPERATOR> 0
//                 System.out.println("Fibonacci number " + i + " is: " + 0);
//                 recursiveFibonacci(i-1);
//             }else if(i == 1){ //, i <OPERATOR> <COMPARATOR>
//                 System.out.println("Fibonacci number " + i + " is: " + 1);
//             }else if(i == 2){ //, i <OPERATOR> <COMPARATOR>
//                 System.out.println("Fibonacci number " + i + " is: " + 1);
//             }else{ // or else
//                 System.out.println("Fibonacci number " + i + " is: " + (recursiveFibonacci(i-1) +
//                 recursiveFibonacci(i-2)));
//             }
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