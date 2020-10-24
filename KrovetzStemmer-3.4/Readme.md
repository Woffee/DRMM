Download the most recent binary kstem-x.x.jar from https://sourceforge.net/projects/lemur/files/lemur/KrovetzStemmer-3.4/ and add the jar to your classpath. Create an instance of org.lemurproject.kstem.KrovetzStemmer, and call

    public String stem(String term)

in your code. KrovetzStemmer includes a simple main method that allows stemming a single term or an input file of terms, one per line.

For example:

    $ java -classpath /path/to/kstem-x.x.jar org.lemurproject.kstem.KrovetzStemmer -w someTerm
    someTerm someTermStem
    $ java -classpath /path/to/kstem-x.x.jar org.lemurproject.kstem.KrovetzStemmer someFile
    term1 term1Stem
    term2 term2Stem
    ...

You can also download the source and build the jar file with mvn, or include the source in your project.