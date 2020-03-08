import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.AmazonS3Exception;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
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
        String bucketName = props2.getProperty("bucketToCreate");

        AWSCredentials credentials = new BasicAWSCredentials(accessKey, secretKey);

        final AmazonS3 s3client = AmazonS3ClientBuilder
                .standard()
                .withCredentials(new AWSStaticCredentialsProvider(credentials))
                .withRegion(Regions.US_EAST_1)
                .build();

        try {
            s3client.createBucket(bucketName);
        } catch (AmazonS3Exception e) {
            System.err.println(e.getErrorMessage());
        }




    }
}
