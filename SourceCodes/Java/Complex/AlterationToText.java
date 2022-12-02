import java.util.regex.*;

import static java.util.regex.Pattern.CASE_INSENSITIVE;

public class AlterationToText {

    public String originalText;

    public AlterationToText(String originalText) {
        this.originalText = originalText;
    }

    /**
     * 1st alteration
     * Replaces the shorthand representation of not (n't) with the long version ( not).
     * Aydın Burak Kuşçu 041901043
     */
    public void alterationLongNot() {
        Pattern pat = Pattern.compile("(?<=([Cc]))an't");
        Matcher matcher = pat.matcher(originalText);
        originalText = matcher.replaceAll("annot");

        pat = Pattern.compile("(?<=([Ss]))han't");
        matcher = pat.matcher(originalText);
        originalText = matcher.replaceAll("hall not");

        pat = Pattern.compile("(?<=([Ww]))on't");
        matcher = pat.matcher(originalText);
        originalText = matcher.replaceAll("ill not");

        pat = Pattern.compile("n't", CASE_INSENSITIVE);
        matcher = pat.matcher(originalText);
        originalText = matcher.replaceAll(" not");
    }

    /**
     * 2nd alteration
     * Replaces the incorrect usage of has and have after subjects. I, you, we, they => have; he, she, it => has.
     * Aydın Burak Kuşçu 041901043
     */
    public void alterationHasHave() {
        Pattern pat = Pattern.compile("(?<=((S|s|)|([Hh])e|[Ii]t)) have");
        Matcher matcher = pat.matcher(originalText);
        originalText = matcher.replaceAll(" has");

        pat = Pattern.compile("(?<=([Ii]|[Yy]ou|[Ww]e|[Tt]hey)) has");
        matcher = pat.matcher(originalText);
        originalText = matcher.replaceAll(" have");
    }

    /**
     * 3rd alteration
     * Corrects the incorrect placement of auxiliary verbs and subjects in question sentences.
     * Aydın Burak Kuşçu 041901043
     */
    public void alterationAuxiliaryVerbToCorrectPosition() {
        Pattern pat = Pattern.compile("(?<=(^Wh|^How))([^ ]*)(.*?) (I|you|we|they|he|she|it|my.*?|your.*?|our.*?|their.*?|his.*?|her.*?|its.*?|the.*?|[A-Z].*?) (am|is|are|was|were|has|have|had|did|shall|will|should|would|may|might|must|can|could|does|do|need)((\\s.*)\\?)");
        Matcher matcher = pat.matcher(originalText);
        String subject;
        String auxVerb;
        String start;
        String end;
        if (matcher.find()) {
            start = matcher.group(1) + matcher.group(2) + matcher.group(3);
            subject = matcher.group(4);
            auxVerb = matcher.group(5);
            end = matcher.group(6);
            originalText = start + " " + auxVerb + " " + subject + end;
        }
    }

    /**
     * 4th alteration
     * Replaces the ands in consecutive ands with the comma (,) except the last and.
     * Aydın Burak Kuşçu 041901043
     */
    public void alterationAndToComma() {
        Pattern pat = Pattern.compile(" and (?=([^ ]* ){0,2}([^ ]*)? and )");
        Matcher matcher = pat.matcher(originalText);
        originalText = matcher.replaceAll(", ");
    }

    /**
     * 10th alteration
     * Converts the cause and effect sentences where the because is in the middle of two clauses to sentences where
     * the because is at the start of the sentence.
     * Aydın Burak Kuşçu 041901043
     */
    public void alterationBecauseToStart() {
        Pattern pat = Pattern.compile("because ([^.]*)(?=\\.)");
        Matcher matcher = pat.matcher(originalText);
        String becauseClause;
        String otherClause;
        if (matcher.find()) {
            becauseClause = matcher.group();
            becauseClause = becauseClause.substring(0, 1).toUpperCase() + becauseClause.substring(1);
            otherClause = originalText.substring(0, matcher.start());
            otherClause = otherClause.strip();
            if (otherClause.charAt(0) != 'I') {
                otherClause = (otherClause.substring(0, 1).toLowerCase() + otherClause.substring(1));
            }
            originalText = becauseClause + ", " + otherClause + originalText.substring(matcher.end());
        }
    }

    /**
     * alterationArticle(): fifth alteration that fixes the articles
     * to its correct article
     * Oğuzhan Güngör 041901016
     */
    public void alterationArticle() {
        Pattern pat = Pattern.compile(" (a)(n) ([^aeiou])", CASE_INSENSITIVE);
        Matcher matcher = pat.matcher(originalText);
        originalText = matcher.replaceAll(" $1 $3");

        pat = Pattern.compile(" (a) ([aeiou])", CASE_INSENSITIVE);
        matcher = pat.matcher(originalText);
        originalText = matcher.replaceAll(" $1n $2");

        pat = Pattern.compile(" (a)(n) (university)", CASE_INSENSITIVE);
        matcher = pat.matcher(originalText);
        originalText = matcher.replaceAll(" $1 $3");

        pat = Pattern.compile(" (a) (hour)", CASE_INSENSITIVE);
        matcher = pat.matcher(originalText);
        originalText = matcher.replaceAll(" $1n $2");
    }

    /**
     * alterationAbbreviation(): sixth alteration that extracts
     * quotes. Replace ' quotes with " and fix the complications of the string.
     * Oğuzhan Güngör 041901016
     */
    public void alterationAbbreviation(){
        Pattern pat = Pattern.compile("\"(([A-Z])([^ ]*) (of |or |and |))+(([A-Z])([^ ]*))\"(?!( \\())");
        Matcher matcher = pat.matcher(originalText);
        Pattern pat2 = Pattern.compile("[A-Z]");
        while(matcher.find()) {
            String name = matcher.group(0);
            Matcher match2 = pat2.matcher(name);
            StringBuilder abbreviation = new StringBuilder();
            while(match2.find()) {
                abbreviation.append(match2.group(0));
            }
            originalText = matcher.replaceFirst("$0 (" + abbreviation + ")");
            matcher = pat.matcher(originalText);
        }
    }

    /**
     * alterationExtractQuotes(): seventh alteration that extracts
     * quotes. Replace ' quotes with " and fix the complications of the string.
     * Oğuzhan Güngör 041901016
     */
    public void alterationExtractQuotes() {
        Pattern pat = Pattern.compile("(said|say|saying|that|:|this)( *)(')([a-zA-Z])(.*?)([.!?])(')");
        Matcher matcher = pat.matcher(originalText);
        while (matcher.find()) {
            originalText = matcher.replaceFirst("$1 \""
                    + matcher.group(4).toUpperCase()
                    + matcher.group(5)
                    + matcher.group(6)
                    + "\"");
            matcher = pat.matcher(originalText);
        }
    }

    /**
     * alterationExtractEMail(): eighth alteration that finds the e-mail
     * in the conversation and covers the e-mail with ''
     * in order to separate it from the conversation
     * Oğuzhan Güngör 041901016
     */
    public void alterationExtractEMail() {
        Pattern pat = Pattern.compile("(?<!')[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+(?!')");
        Matcher matcher = pat.matcher(originalText);
        originalText = matcher.replaceAll("'$0'");
    }

    /**
     * alterationDoubleNegative(): ninth alteration that makes
     * double negative to single negative.
     * Oğuzhan Güngör 041901016
     */
    public void alterationDoubleNegative() {
        Pattern pat = Pattern.compile("(?<= n)(ot) (anything|anybody|any|ever)", CASE_INSENSITIVE);
        Matcher matcher = pat.matcher(originalText);

        while (matcher.find()) {
            if (matcher.group(2).matches("anything")) {
                originalText = matcher.replaceFirst("othing");
            } else if (matcher.group(2).matches("anybody")) {
                originalText = matcher.replaceFirst("obody");
            } else if (matcher.group(2).matches("any")) {
                originalText = matcher.replaceFirst("one");
            } else {
                originalText = matcher.replaceFirst("ever");
            }
            matcher = pat.matcher(originalText);
        }
    }
}
