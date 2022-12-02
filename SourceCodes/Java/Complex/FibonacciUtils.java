package week2;

public class FibonacciUtils {

    /**
     * recursiveFibonacci
     * calculates nth fibonacci number recursively
     *
     * @param nthFibonacciNumber: is the place of the fibonacci number
     * @return the nth fibonacci number
     * time complexity: nth fibonacci number
     *
     */
    public static int recursiveFibonacci(int nthFibonacciNumber){

        if (nthFibonacciNumber <= 1)
            return nthFibonacciNumber;

        return recursiveFibonacci(nthFibonacciNumber - 1)
                + recursiveFibonacci(nthFibonacciNumber - 2);
    }

    /**
     * listFibonacci
     * this algorithm stores the fibonacci numbers inside of an array
     * and then calculates the last 2 numbers
     * @param nthFibonacciNumber: is the place of the fibonacci number and the size of the array
     * @return the nth fibonacci number
     * time complexity: 2n + 2
     *
     */

    public static long listFibonacci(int nthFibonacciNumber){
        long[] fibonacciArray = new long[nthFibonacciNumber + 1];
        fibonacciArray[0] = 0;
        fibonacciArray[1] = 1;
        if(nthFibonacciNumber <= 1){
            return nthFibonacciNumber;
        }
        for(int i = 2; i < nthFibonacciNumber + 1; i++){
            fibonacciArray[i] = fibonacciArray[i-1] + fibonacciArray[i - 2];
        }
        return fibonacciArray[nthFibonacciNumber];
    }

    /**
     * fibonacciArray
     * this algorithm stores and prints the fibonacci sequence
     * @param nthFibonacciNumber: is the place of the fibonacci number and the size of the array
     * @return fibonacci sequence array
     */

    public static long[] fibonacciArray(int nthFibonacciNumber){
        long[] fibonacciArray = new long[nthFibonacciNumber + 1];
        fibonacciArray[1] = 1;
        for(int i = 2; i < nthFibonacciNumber + 1; i++){
            fibonacciArray[i] = fibonacciArray[i-1] + fibonacciArray[i - 2];
        }
        return fibonacciArray;
    }

    /**
     * naiveGCD
     * finds the greatest common divisor of 2 numbers
     *
     * @param num1: int number 1
     * @param num2: int number 2
     * @return greatestDivisor is the greatest common divisor
     * runtime approx. num1 + num2
     */

    public static int naiveGCD(int num1, int num2){
        int greatestDivisor = 0;
        for(int i = 1; i <= num1 + num2; i++){
            if(num1 % i == 0 && num2 % i == 0){
                greatestDivisor = i;
            }
        }
        return greatestDivisor;
    }

    /**
     * euclideanGCD
     * finds the greatest common divisor via recursive function
     * if num2 becomes 0, the greatest common divisor is num1
     * otherwise, the function keeps solving greatest common divisor till it
     * reaches 0
     *
     * @param num1
     * @param num2
     * @return greatest common divisor
     *
     * Time Complexity: log(num1 * num2)
     *
     */

    public static long euclideanGCD(long num1, long num2){
        if(num2 == 0){
            return num1;
        }
        return euclideanGCD(num2, (num1 % num2));
    }

    /**
     * lastFibonacci
     * @param nthFibonacciNumber place
     * @return the Last digit of the given fibonacci number location
     */

    public static int lastFibonacci(int nthFibonacciNumber){

        if(nthFibonacciNumber <= 1){
            return nthFibonacciNumber;
        }
        int[] fibonacciArray = new int[3];
        fibonacciArray[0] = 0;
        fibonacciArray[1] = 1;
        int counter = 1;
        while(counter++ < nthFibonacciNumber){
            fibonacciArray[2] = (fibonacciArray[0] % 10) + (fibonacciArray[1] % 10);
            fibonacciArray[0] = (fibonacciArray[1] % 10) + (fibonacciArray[2] % 10);
            counter++;
            fibonacciArray[1] = (fibonacciArray[2] % 10)  + (fibonacciArray[0] % 10);
            counter++;
        }
        return fibonacciArray[nthFibonacciNumber % 3] % 10;
    }

    /**
     * improvedFibonacci returns the nth fibonacci number.
     * improved version of my algorithm
     * @param nthFibonacciNumber place
     * @return nth fibonacci number's value
     */

    public static int improvedFibonacci(int nthFibonacciNumber){

        if(nthFibonacciNumber <= 1){
            return nthFibonacciNumber;
        }
        int[] fibonacciArray = new int[3];
        fibonacciArray[0] = 0;
        fibonacciArray[1] = 1;
        int counter = 1;
        while(counter++ < nthFibonacciNumber){
            fibonacciArray[2] = fibonacciArray[0]  + fibonacciArray[1] ;
            fibonacciArray[0] = fibonacciArray[1]  + fibonacciArray[2] ;
            counter++;
            fibonacciArray[1] = fibonacciArray[2]  + fibonacciArray[0] ;
            counter++;
        }
        return fibonacciArray[nthFibonacciNumber % 3];
    }

    /**
     * lcm Least Common Multiple
     * @param num1: int number 1
     * @param num2: int number 2
     * @return least common multiple lcm
     */

    public static long lcm (int num1, int num2){
        long lcm =  (long) num1 * ((long) num2 / euclideanGCD(num1, num2));
        return lcm;
    }

    /**
     * pisanoPeriodLength: Calculates the fibonacci numbers with pisano period
     * @param modulo: the modulo number we want to find from these fibonacci numbers
     * @return length: pisano period repeats in a certain length
     */

    public static long pisanoPeriodLength(long modulo) {
        long F1 = 0, F2 = 1, F, length = 0;
        for (int i = 0; i < modulo * modulo; i++) {
            F = (F1 + F2) % modulo;
            F1 = F2;
            F2 = F;
            if (F1 == 0 && F2 == 1) {
                length = i + 1;
                break;
            }
        }
        return length;
    }

    /**
     * getFibonacciHugeFast: finds fibonacci sequence's desired number fast
     * @param number: nth fibonacci number
     * @param modulo: the desired modulo for the nthFibonacci number
     * @return nth % modulo
     */

    public static long getFibonacciHugeFast(long number, long modulo) {
        long remainder = number % pisanoPeriodLength(modulo);

        long F1 = 0, F2 = 1, F = remainder;
        for (int i = 1; i < remainder; i++) {
            F = (F1 + F2) % modulo;
            F1 = F2;
            F2 = F;
        }
        return F % modulo;
    }

    /**
     * improvedFibonacciSum is improved version of my fibonacci sum algorithm
     * @param nthFibonacciNumber location
     * @return sum of all fibonacci numbers
     */

    public static long improvedFibonacciSum(long nthFibonacciNumber){

        if(nthFibonacciNumber <= 1){
            return (int) nthFibonacciNumber;
        }
        long modNth = nthFibonacciNumber % 3;
        long[] fibonacciArray = new long[3];
        long[] tempFibonacci = new long[3];
        fibonacciArray[0] = 0;
        fibonacciArray[1] = 1;
        long counter = 1;
        while(counter++ < nthFibonacciNumber){
            fibonacciArray[2] = fibonacciArray[0]  + fibonacciArray[1] ;
            if(counter == 2) {
                tempFibonacci[2] += fibonacciArray[2] + fibonacciArray[1];
            }
            else{
                tempFibonacci[2] = fibonacciArray[2] + tempFibonacci[1];
            }
            fibonacciArray[0] = fibonacciArray[1]  + fibonacciArray[2] ;
            tempFibonacci[0] = tempFibonacci[2] + fibonacciArray[0];
            counter++;
            fibonacciArray[1] = fibonacciArray[2]  + fibonacciArray[0] ;
            tempFibonacci[1] = tempFibonacci[0] + fibonacciArray[1];
            counter++;
        }
        return tempFibonacci[(int) modNth];
    }

    public static long improvedSquaredDigitSum(long nthFibonacciNumber){

        if(nthFibonacciNumber <= 1){
            return (int) nthFibonacciNumber;
        }
        long modNth = nthFibonacciNumber % 3;
        long[] fibonacciArray = new long[3];
        long[] tempFibonacci = new long[3];
        fibonacciArray[0] = 0;
        fibonacciArray[1] = 1;
        long counter = 1;
        while(counter++ < nthFibonacciNumber){
            fibonacciArray[2] = (fibonacciArray[0] % 10)  + (fibonacciArray[1] % 10);
            if(counter == 2) {
                tempFibonacci[2] += fibonacciArray[2] + fibonacciArray[1];
            }
            else{
                tempFibonacci[2] = (fibonacciArray[2] % 10) + (tempFibonacci[1] % 10);
            }
            fibonacciArray[0] = (fibonacciArray[1] % 10)  + (fibonacciArray[2] % 10);
            tempFibonacci[0] = (tempFibonacci[2] % 10) + (fibonacciArray[0] % 10);
            counter++;
            fibonacciArray[1] = (fibonacciArray[2] % 10) + (fibonacciArray[0] % 10);
            tempFibonacci[1] = (tempFibonacci[0] % 10) + (fibonacciArray[1] % 10);
            counter++;
        }
        return tempFibonacci[(int) modNth] * tempFibonacci[(int) modNth] % 10;
    }

}
