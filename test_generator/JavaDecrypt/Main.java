import utils.CryptoUtil;
import utils.CryptoUtil.CryptoInfo;
import java.io.IOException;
import java.security.GeneralSecurityException;

public class Main {

    public static void main(String[] args) throws GeneralSecurityException, IOException {
        String encryptString = args[0];
        CryptoInfo cryptoInfo = CryptoUtil.getDefault(encryptString);

        String pass = CryptoUtil.decode(cryptoInfo);
        System.out.println(pass);
    }
}