import java.util.Scanner;

public class hanoi {

    public static int NUMBER_OF_STEPS = 1;
    /**
     * hanoi: computes lesser moves for a hanoi tower.
     * @param numberOfDisks: number of disks
     * @param A: source column
     * @param C: target column
     * @param B: temporary
     */

    public static void hanoi(int numberOfDisks, String A, String C, String B){

        if(numberOfDisks > 0){
            hanoi(numberOfDisks - 1, A, B, C);
            System.out.println(NUMBER_OF_STEPS + ". step: " + A + "-->" + C);
            NUMBER_OF_STEPS ++;
            hanoi(numberOfDisks - 1, B, C, A);
        }

    }


    public static void main(String[] args){
        Scanner input = new Scanner(System.in);
        System.out.println("Enter the number of disks");
        int numberOfDisks = input.nextInt();
        hanoi(numberOfDisks, "A", "C", "B");
    }

}
