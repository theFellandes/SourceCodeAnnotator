import java.util.*; 
import java.io.*;

class FindIntersections {

  public static String FindIntersection(String[] strArr) {
    
    String[] firstArray = splitSubArray(strArr[0]);
    String[] secondArray = splitSubArray(strArr[1]);  

    String[] intersection = findIntersectingElements(firstArray, secondArray);
    String output = "";
    for(String element : intersection){
      output += element + ",";
    }
    
    return removeLastCharacter(output);
  }

  
  public static String[] findIntersectingElements(String[] firstArray, String[] secondArray){
    LinkedHashSet<String> set = new LinkedHashSet<>();

    set.addAll(Arrays.asList(firstArray));     
    set.retainAll(Arrays.asList(secondArray));
     
    //convert to array
    String[] intersection = {};
    intersection = set.toArray(intersection);

    return intersection;
  }

  public static String removeLastCharacter(String str){  
    //the replaceAll() method removes the string and returns the string  
    return (str == null) ? null : str.replaceAll(".$", "");  
  }  
  
  public static String[] splitSubArray(String strArr){
    String[] subArray = null;  
    //converting using String.split() method with whitespace as a delimiter  
    subArray = strArr.split(",");
    String[] sanitazedArray = new String[subArray.length];

    int index = 0;
    for(String element : subArray){
      sanitazedArray[index++] = element.replaceAll("\\s+","");
    }

    return sanitazedArray;
  }

  public static void main (String[] args) {  
    // keep this function call here     
    Scanner s = new Scanner(System.in);
    System.out.print(FindIntersection(s.nextLine())); 
  }

}