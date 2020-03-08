import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.AmazonS3Exception;
import com.amazonaws.services.s3.model.Bucket;
import com.amazonaws.services.s3.model.GetObjectRequest;
import com.amazonaws.services.s3.model.S3Object;
import com.opencsv.CSVReader;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;

import java.io.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Properties;

public class LoanProcessing {

    public static void main(String[] args) {
        /*String s3URL;

        if (args.length == 1) {
            // the inputDir
            s3URL = args[0];
        } else {
            System.out.println("Error with commandline inputs!");
            return;
        } */

        HashMap<String,String> mapOfProps = new HashMap<String, String>();
        try {
            mapOfProps = getPropStrs();
        } catch(IOException e) {
            e.printStackTrace();
        }
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

    public static HashMap<String, String> getPropStrs() throws FileNotFoundException, IOException {
        // The bucket name for s3 is stored in private.properties which is not uploaded to the github repo
        String basePath = new File("").getAbsolutePath();
        String pathToProps = basePath+"/private.properties";
        Properties props2 = new Properties();
        FileInputStream fis = new FileInputStream(pathToProps);
        props2.load(fis);
        String accessKey = props2.getProperty("accessKey");
        String secretKey = props2.getProperty("secretKey");
        String bucketName = props2.getProperty("bucketName");
        String loanKey = props2.getProperty("loanKey");
        String master = props2.getProperty("master");
        String s3URL = props2.getProperty("s3URL");

        HashMap<String, String> mapOfProps = new HashMap<String, String>() {
            {
                put("accessKey", accessKey);
                put("secretKey", secretKey);
                put("bucketName",bucketName);
                put("loanKey", loanKey);
                put("master", master);
                put("s3URL", s3URL);
            }
        };

        return mapOfProps;
    }

    public void s3ToJava() throws IOException{

        HashMap<String,String> mapOfProps = getPropStrs();
        String accessKey = mapOfProps.get("accessKey");
        String secretKey = mapOfProps.get("secretKey");
        String bucketName = mapOfProps.get("bucketName");
        String loanKey = mapOfProps.get("loanKey");

        // passing in AWS credentials
        AWSCredentials credentials = new BasicAWSCredentials(accessKey, secretKey);
        // connecting to s3
        final AmazonS3 s3client = AmazonS3ClientBuilder
                .standard()
                .withCredentials(new AWSStaticCredentialsProvider(credentials))
                .withRegion(Regions.US_EAST_1)
                .build();

        try {
            // listing potential buckets
            List<Bucket> buckets = s3client.listBuckets();
            for(Bucket bucket : buckets) {
                System.out.println(bucket.getName());
            }
        } catch (AmazonS3Exception e) {
            System.err.println(e.getErrorMessage());
        }

        // Reading in the CSV file from s3
        S3Object object = s3client.getObject(new GetObjectRequest(bucketName, loanKey));
        InputStream objectData = object.getObjectContent();

        /*CSVParser parser = new CSVParserBuilder()
                .withSeparator(',')
                .withIgnoreQuotations(true)
                .build();*/

        // converting InputStream to CSVReader object
        CSVReader reader = new CSVReader(new InputStreamReader(objectData));
/*               .withSeparator(',')
//                .withIgnoreQuotations(true)
               .build();*/
        List<String[]> list = new ArrayList<>();
        String[] line;
        // Testing output
        while ((line = reader.readNext()) != null) {
            list.add(line);
            for (String s: line) {
                System.out.print(" "+s);
            }
            System.out.println(" ");
        }
        reader.close();

    }

    public List<String[]> readAll(Reader reader) throws Exception {
        CSVReader csvReader = new CSVReader(reader);
        List<String[]> list = new ArrayList<>();
        list = csvReader.readAll();
        reader.close();
        csvReader.close();
        return list;
    }
}
