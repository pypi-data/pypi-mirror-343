import java.io.*;
import java.net.*;

public class MutualServer implements Runnable {
    private Socket socket;
    private static ServerSocket ss;

    MutualServer(Socket newSocket) {
        this.socket = newSocket;
    }

    public static void main(String[] args) {
        try {
            ss = new ServerSocket(7000);
            System.out.println("Server Started");
            while (true) {
                Socket s = ss.accept();
                MutualServer es = new MutualServer(s);
                Thread t = new Thread(es);
                t.start();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void run() {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            while (true) {
                System.out.println(in.readLine());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}