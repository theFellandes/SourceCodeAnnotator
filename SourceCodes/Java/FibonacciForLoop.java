package week2;

public class FibonacciUtils extends Recursive implements IEnumerable, IBruhable {
    int bruhMomento = 5;
    int bruhMoment = 5;
    int bruhMomen = 5;
    int bruhMome = 5;
    int bruhMom = 5;
    int bruhMo = 5;

    public static String getWorld(int demo, int demo2){
        String world = "Hello" + "World";
        String bruh = world + "bruh";
        int myInt = 0;
        myInt += demo;
        myInt = demo2;
    }

    protected static int recursiveFibonacci(int nthFibonacciNumber, bruh bruhMoment){
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

    public static int power(int base, int exponent) {
        int result = 1;
        for (int i = 0; i < exponent; i++) {
            result *= base;
        }
        return result;
    }
}