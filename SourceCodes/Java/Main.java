package com.company;

/**
 * The hello world app for testing the source code annotator
 * @author Fellandes
 */
public class Main {

    /**
     * The main method for the Java code
     * @param args: command line arguments
     */
    public static void main(String[] args) {
	    /*
	    * write your code here
        */
        System.out.println("Hello"); //asdf
        printWorld();
    }

    /**
     * The method for printing the word World.
     */
     @books_data(book_name = "Effective Java", book_price = 30,
            author = "Joshua Bloch")
    public static void printWorld(){
        System.out.println("World");
    }
}
