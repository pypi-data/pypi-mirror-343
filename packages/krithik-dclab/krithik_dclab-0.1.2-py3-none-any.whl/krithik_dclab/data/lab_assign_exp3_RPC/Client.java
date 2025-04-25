import java.io.*;
import java.net.*;

class Client {
    public static void main(String[] args) throws Exception {
        Socket sock = new Socket("192.168.56.1", 3000); // replace with IP address of your own PC
        BufferedReader keyRead = new BufferedReader(new InputStreamReader(System.in));
        OutputStream ostream = sock.getOutputStream();
        PrintWriter pwrite = new PrintWriter(ostream, true);
        InputStream istream = sock.getInputStream();
        BufferedReader receiveRead = new BufferedReader(new InputStreamReader(istream));
        System.out.println("Client ready, type and press Enter key");
        String receiveMessage, sendMessage, temp;
        while (true) {
            System.out.println("\nEnter operation to perform(add,sub, mul, div)....");
            temp = keyRead.readLine();
            sendMessage = temp.toLowerCase();
            pwrite.println(sendMessage);
            System.out.println("Enter first parameter :");
            sendMessage = keyRead.readLine();
            pwrite.println(sendMessage);
            System.out.println("Enter second parameter: ");
            sendMessage = keyRead.readLine();
            pwrite.println(sendMessage);
            System.out.flush();
            if ((receiveMessage = receiveRead.readLine()) != null)
                System.out.println(receiveMessage);
        }
    }
}