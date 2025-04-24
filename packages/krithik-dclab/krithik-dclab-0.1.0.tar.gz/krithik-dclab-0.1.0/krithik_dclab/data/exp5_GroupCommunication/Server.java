import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Vector;
import java.util.concurrent.ConcurrentLinkedQueue;

public class Server {
    private static Vector<ClientHandler> clients = new Vector<>();
    private static ConcurrentLinkedQueue<String> messageQueue = new ConcurrentLinkedQueue<>();

    public static void main(String[] args) {
        try (ServerSocket listener = new ServerSocket(9001)) {
            System.out.println("Server running on port 9001...");
            while (true) {
                ClientHandler handler = new ClientHandler(listener.accept());
                clients.add(handler);
                handler.start();
            }
        } catch (Exception e) {
            System.err.println("Server error: " + e.getMessage());
        }
    }

    private static class ClientHandler extends Thread {
        private Socket socket;
        private PrintWriter out;
        private BufferedReader in;
        private String name;
        private boolean running = true;

        public ClientHandler(Socket socket) {
            this.socket = socket;
        }

        public void run() {
            try {
                in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                out = new PrintWriter(socket.getOutputStream(), true);
                
                // Request and validate client name
                out.println("SUBMITNAME");
                name = in.readLine();
                if (name == null || name.trim().isEmpty()) {
                    name = "Anonymous_" + System.currentTimeMillis();
                }
                
                System.out.println(name + " connected");
                broadcast("SERVER: " + name + " joined the chat");

                // Main message handling loop
                while (running) {
                    String input = in.readLine();
                    if (input == null) {
                        break;
                    }
                    String message = name + ": " + input;
                    messageQueue.offer(message);
                    broadcast("MESSAGE " + message);
                }
            } catch (Exception e) {
                System.err.println("Error handling client " + name + ": " + e.getMessage());
            } finally {
                disconnect();
            }
        }

        private void broadcast(String message) {
            synchronized (clients) {
                for (ClientHandler client : clients) {
                    if (client.out != null) {
                        client.out.println(message);
                    }
                }
            }
        }

        private void disconnect() {
            running = false;
            clients.remove(this);
            if (name != null) {
                broadcast("SERVER: " + name + " left the chat");
                System.out.println(name + " disconnected");
            }
            try {
                if (out != null) out.close();
                if (in != null) in.close();
                if (socket != null) socket.close();
            } catch (Exception e) {
                System.err.println("Error closing resources: " + e.getMessage());
            }
        }
    }
}