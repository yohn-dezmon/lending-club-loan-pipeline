import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.HashMap;
import java.util.Properties;

public class LoanProcessing {

    public static void main(String[] args) throws FileNotFoundException, IOException {
        /*String s3URL;

        if (args.length == 1) {
            // the inputDir
            s3URL = args[0];
        } else {
            System.out.println("Error with commandline inputs!");
            return;
        } */

        CommonMethods cm = new CommonMethods();
        HashMap<String,String> mapOfProps = cm.getPropStrs();
        String master = mapOfProps.get("master");
        String accessKey = mapOfProps.get("accessKey");
        String secretKey = mapOfProps.get("secretKey");
//        String loanKey = mapOfProps.get("loanKey");
        String s3URL = mapOfProps.get("s3URL");


        SparkSession spark = SparkSession.builder().master(master).appName("LoanProcessing").
                config("some config", "value").getOrCreate();

        Dataset<Row> loanDataset = spark.read().format("csv").option("header","true").load("s3a://" + accessKey + ":"+secretKey+"@"+s3URL);

        loanDataset.createOrReplaceTempView("loans");

        Dataset<Row> dateFormatted = loanDataset.sqlContext().sql("Select * "
                +"from loans LIMIT 10");


    }
}
