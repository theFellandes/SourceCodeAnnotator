import java.util.Scanner;

public class reversed {

    public static void main(String[] args){
        Scanner input = new Scanner(System.in);
        System.out.println("Enter number");
        int inputValue = input.nextInt();
        System.out.println("N:");
        int N = input.nextInt();
        if(sizeReturn(inputValue, N)){
            System.out.println("This cannot be reversed by this location.");
            return;
        }
        reversed(inputValue, N);
    }

    public static void reversed(int number, int N){
        int[] tempArray = new int[N];
        for(int i = 0; i < N; i++){
            tempArray[i] = number % 10;
            number /= 10;
        }
        for(int i = 0; i < N; i++){
            number *= 10;
            number += tempArray[i];
        }
        System.out.println(number);
    }

    public static boolean sizeReturn(int number, int N){
        int counter = 0;
        while(number != 0){
            number /= 10;
            counter++;
        }
        return (counter < N);
    }
}
