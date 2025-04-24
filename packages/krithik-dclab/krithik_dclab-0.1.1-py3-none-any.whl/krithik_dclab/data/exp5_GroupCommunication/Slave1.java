import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

public class Slave1 {
    public static void main(String[] args) {
        Socket socket = null;
        BufferedReader in = null;
        PrintWriter out = null;
        Scanner scanner = new Scanner(System.in);
        boolean running = true;

        try {
            socket = new Socket("localhost", 9001);
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out = new PrintWriter(socket.getOutputStream(), true);

            // Send name
            System.out.print("Enter your name: ");
            String name = scanner.nextLine();
            out.println(name);

            // Start message receiver thread
            BufferedReader finalIn = in;
            new Thread(() -> {
                try {
                    String line;
                    while ((line = finalIn.readLine()) != null) {
                        if (line.startsWith("MESSAGE ")) {
                            System.out.println("\nNew message: " + line.substring(8));
                            System.out.print("Enter choice (1-3): ");
                        } else if (line.startsWith("SERVER: ")) {
                            System.out.println("\nServer: " + line.substring(8));
                            System.out.print("Enter choice (1-3): ");
                        }
                    }
                } catch (Exception e) {
                    System.err.println("Connection lost: " + e.getMessage());
                }
            }).start();

            // Main menu loop
            while (running) {
                System.out.println("\nSelect an option:");
                System.out.println("1. Check for new messages");
                System.out.println("2. Send a message");
                System.out.println("3. Exit");
                System.out.print("Enter choice (1-3): ");

                int choice;
                try {
                    choice = scanner.nextInt();
                    scanner.nextLine(); // Consume newline
                } catch (Exception e) {
                    scanner.nextLine();
                    System.out.println("Invalid input. Please enter a number.");
                    continue;
                }

                switch (choice) {
                    case 1:
                        System.out.println("Messages are displayed automatically when received.");
                        break;
                    case 2:
                        System.out.print("Enter a message: ");
                        String message = scanner.nextLine();
                        out.println(message);
                        System.out.println("Message sent.");
                        break;
                    case 3:
                        running = false;
                        break;
                    default:
                        System.out.println("Invalid choice. Please try again.");
                }
            }
        } catch (Exception e) {
            System.err.println("Slave1 client error: " + e.getMessage());
        } finally {
            try {
                if (out != null) out.close();
                if (in != null) in.close();
                if (socket != null) socket.close();
                scanner.close();
            } catch (Exception e) {
                System.err.println("Error closing resources: " + e.getMessage());
            }
        }
    }
}