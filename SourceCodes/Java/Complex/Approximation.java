import java.util.Scanner;

public class Approximation {

    public static void main(String[] args){

        Scanner input = new Scanner(System.in);
        System.out.println("Enter the n value");
        double e = 1.0; //Newton's series expansions first 1 * x^0
        double n = input.nextDouble();

        //Compute e value for n
        //e = 1 / x^0 + (1 / x^1) + (1 / x^2) ... (1 / x^n)
        for(double i = 1; i <= n; i++){
            double denominator = i;
            for(double j = i - 1; j >= 1; j--){
                denominator *= j;
            }
            e += 1 / denominator;
        }

        System.out.println("The e value for n = " + n + ": " + e);

    }

}
