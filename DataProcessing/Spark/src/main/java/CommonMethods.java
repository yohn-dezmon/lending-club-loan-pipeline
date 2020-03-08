import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Properties;

public class CommonMethods {

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
}
