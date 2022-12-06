package com.company;

public class Main {

    public static void main(String[] args) {
        int randomNumber = getRandomNumber(0, 10);
        int randomNumber2 = getRandomNumber(0, 10);
        int randomNumbersAdded = addition(randomNumber, randomNumber2);
        int userId = incrementNumberByOne(getDefaultUserId());
        userId = incrementNumberBy20(userId);
        stanza = appendStringWithStanza("Stanza");
    }

    public static int getRandomNumber(int lowerBound, int upperBound){
        Random random = new Random();
        return random.nextInt(lowerBound, upperBound);
    }

    public static int addition(int number1, int number2){
        return number1 + number2;
    }

    public static int getDefaultUserId(){
        return 20;
    }

    public static int incrementNumberByOne(int number){
        return number++;
    }

    public static int incrementNumberBy20(int number){
        return number + 20;
    }

    public static String appendStringWithStanza(String inputString){
        return inputString + " Stanza";
    }
}
