package week2;

public class FibonacciUtils {
    /**
    * Checks if i <OPERATOR> 1
    *
    * @author LazyDoc
    */
    public static int recursiveFibonacci(int nthFibonacciNumber){

        if (nthFibonacciNumber <= 1)
            return nthFibonacciNumber;

        return recursiveFibonacci(nthFibonacciNumber - 1)
                + recursiveFibonacci(nthFibonacciNumber - 2);
    }
}