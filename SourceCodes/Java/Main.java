package com.company;

public class myClass extends baseClass {

    public static void main(String[] args) {
        System.out.println("Hello");
        printWorld();
    }

    public static int function(int param1) {
        super.myFunction();
        int bruh = param1 + 5 + 10;
        int bruh2 = param1;
        return 10;
    }

    public static String getWorld(int demo, int demo2){
        String world = "Hello" + "World";
        String bruh = world + "bruh";
        int myInt = 0;
        myInt += demo;
        myInt = demo2;
//         return world;
//         return "World";
//         return world + "World";
    }
}
