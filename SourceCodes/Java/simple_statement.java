package com.company;

public class Main {

    public static void main(String[] args) {
        System.out.println("Hello"); //asdf
        appendStatement = simpleStatement("World");
        System.out.println(appendStatement);
    }

    public static void simpleStatement(String inputString){
        if(inputString.equals("World")){
            return inputString;
        }
        else{
            return "Not World";
        }
    }
}
