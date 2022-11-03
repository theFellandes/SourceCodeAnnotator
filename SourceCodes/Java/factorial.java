import java.util.Scanner;

public class factorial {

    /**
     * listFactorial: finds the nth factorial number
     * @param nthFactorialNumber: index of the sought factorial number
     * @return nth factorial number
     */

    public static long listFactorial(int nthFactorialNumber){
        //if cases for 0, 1 and 2.
        if(nthFactorialNumber == 0 || nthFactorialNumber == 1)
            return 1;
        if(nthFactorialNumber == 2)
            return 2;
        long[] factorialArray = new long[3];
        factorialArray[0] = 1;
        factorialArray[1] = 2;
        int counter = 1;
        while(counter <= nthFactorialNumber){
            factorialArray[counter % 3] = counter * factorialArray[(counter - 1) % 3];
            counter++;
        }
        return factorialArray[nthFactorialNumber % 3];
    }

    public static void main(String[] args){
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();
        System.out.println(listFactorial(n));
    }

}
