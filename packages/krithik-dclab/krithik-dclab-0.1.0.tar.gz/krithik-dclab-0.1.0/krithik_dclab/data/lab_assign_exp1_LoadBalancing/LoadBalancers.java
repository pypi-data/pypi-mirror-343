import java.util.Scanner;
import java.util.Arrays;

class LoadBalancers {
    static void printLoadRoundRobin(int servers, int processes) {
        int each = processes / servers;
        int extra = processes % servers;
        for (int i = 0; i < servers; i++) {
            int total = each + (extra-- > 0 ? 1 : 0);
            System.out.println("Server " + (char) ('A' + i) + " has " + total + " processes");
        }
    }

    static void printLoadWeightedRoundRobin(int[] weights, int processes) {
        int totalWeight = Arrays.stream(weights).sum();
        int[] allocation = new int[weights.length];
        for (int i = 0; i < processes; i++) {
            int maxWeightIndex = 0;
            for (int j = 0; j < weights.length; j++) {
                if (weights[j] > weights[maxWeightIndex]) {
                    maxWeightIndex = j;
                }
            }
            allocation[maxWeightIndex]++;
            weights[maxWeightIndex]--; // Decrease weight temporarily to simulate process allocation
        }
        for (int i = 0; i < allocation.length; i++) {
            System.out.println("Server " + (char) ('A' + i) + " has " + allocation[i] + " processes");
        }
    }

    static void printLoadLeastConnection(int[] connections, int processes) {
        for (int i = 0; i < processes; i++) {
            int minIndex = 0;
            for (int j = 1; j < connections.length; j++) {
                if (connections[j] < connections[minIndex]) {
                    minIndex = j;
                }
            }
            connections[minIndex]++;
        }
        for (int i = 0; i < connections.length; i++) {
            System.out.println("Server " + (char) ('A' + i) + " has " + connections[i] + " connections");
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the number of servers and processes: ");
        int servers = sc.nextInt();
        int processes = sc.nextInt();

        int[] weights = new int[servers];
        int[] connections = new int[servers];
        Arrays.fill(weights, 1); // Default weight of 1 for each server
        Arrays.fill(connections, 0); // No initial connections

        while (true) {
            System.out.println("\nChoose load balancing algorithm:");
            System.out.println("1. Round Robin");
            System.out.println("2. Weighted Round Robin");
            System.out.println("3. Least Connection");
            System.out.println("4. Exit");
            int choice = sc.nextInt();

            switch (choice) {
                case 1:
                    printLoadRoundRobin(servers, processes);
                    break;

                case 2:
                    System.out.println("Enter weights for each server:");
                    for (int i = 0; i < servers; i++) {
                        System.out.println("Weight for server " + (char) ('A' + i) + ": ");
                        weights[i] = sc.nextInt();
                    }
                    printLoadWeightedRoundRobin(weights.clone(), processes);
                    break;

                case 3:
                    System.out.println("Enter initial connections for each server:");
                    for (int i = 0; i < servers; i++) {
                        System.out.println("Connections for server " + (char) ('A' + i) + ": ");
                        connections[i] = sc.nextInt();
                    }
                    printLoadLeastConnection(connections.clone(), processes);
                    break;

                case 4:
                    return;

                default:
                    System.out.println("Invalid choice. Please select a valid option.");
                    break;
            }

            System.out.println("\nDo you want to update servers or processes? (yes/no)");
            if (sc.next().equalsIgnoreCase("yes")) {
                System.out.println("1. Add servers\n2. Remove servers\n3. Add processes\n4. Remove processes");
                int updateChoice = sc.nextInt();
                switch (updateChoice) {
                    case 1:
                        System.out.println("How many more servers: ");
                        servers += sc.nextInt();
                        weights = Arrays.copyOf(weights, servers);
                        connections = Arrays.copyOf(connections, servers);
                        Arrays.fill(weights, weights.length - servers, weights.length, 1);
                        Arrays.fill(connections, connections.length - servers, connections.length, 0);
                        break;

                    case 2:
                        System.out.println("How many servers to remove: ");
                        int removeServers = sc.nextInt();
                        servers -= removeServers;
                        weights = Arrays.copyOf(weights, servers);
                        connections = Arrays.copyOf(connections, servers);
                        break;

                    case 3:
                        System.out.println("How many more processes: ");
                        processes += sc.nextInt();
                        break;

                    case 4:
                        System.out.println("How many processes to remove: ");
                        processes -= sc.nextInt();
                        break;

                    default:
                        System.out.println("Invalid choice, returning to main menu.");
                }
            }
        }
    }
}