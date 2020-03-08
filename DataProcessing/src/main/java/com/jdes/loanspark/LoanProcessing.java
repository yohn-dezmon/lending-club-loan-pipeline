package com.jdes.loanspark;
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
        
        dateFormatted.show();
       

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

        HashMap<String, String> mapOfProps = new HashMap<String, String>();
        mapOfProps.put("accessKey", accessKey);
        mapOfProps.put("secretKey", secretKey);
        mapOfProps.put("bucketName",bucketName);
        mapOfProps.put("loanKey", loanKey);
        mapOfProps.put("master", master);
        mapOfProps.put("s3URL", s3URL);
            

        return mapOfProps;
    }

}
