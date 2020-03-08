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
import com.opencsv.CSVParser;
import com.opencsv.CSVParserBuilder;
import com.opencsv.CSVReader;
import org.apache.directory.api.util.GeneralizedTime;
import sun.jvm.hotspot.gc_implementation.g1.G1Allocator;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

public class S3toJava {

    public static void main(String[] args) throws FileNotFoundException, IOException {

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
