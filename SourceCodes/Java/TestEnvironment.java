package lab;


public class TestEnvironment {

    /**
     * digitSeperator
     * seperates digits of an int number
     *
     * @param number: number to seperate the digits
     * @return int[] of seperated numbers
     */

    public static int[] digitSeperator(int number){
        int count = 1;
        //in order to determine the size of the array, i've created a copy of the number
        int numberCopy = number;
        //determines the size of the array
        while(numberCopy / 10 != 0){
            numberCopy /= 10;
            count++;
        }
        //creates an empty array
        int[] digitArray = new int[count];
        //fills the empty array with the digits
        for(int i = count - 1; i >= 0; i--){
            digitArray[i] = number % 10;
            number /= 10;
        }
        return digitArray;
    }

    /**
     * digitSum
     * sums the digitArray's numbers
     *
     * @param digitArray: an int array of digits
     * @return sum
     */

    public static int digitSum(int[] digitArray){
        int sum = 0;
        for(int digit : digitArray){
            sum += digit;
        }
        return sum;
    }

}
