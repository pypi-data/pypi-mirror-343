import java.util.Scanner;

class LoadBalancers {
    static void printLoad(int servers, int processes) {
        int each = processes / servers;
        int extra = processes % servers;
        for (int i = 0; i < servers; i++) {
            int total = each + (extra-- > 0 ? 1 : 0);
            System.out.println("Server " + (char) ('A' + i) + " has " + total + " processes");
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter the number of servers and processes: ");
        int servers = sc.nextInt();
        int processes = sc.nextInt();

        while (true) {
            printLoad(servers, processes);
            System.out.println("1. Add servers\n2. Remove Servers\n3. Add Processes\n4. Remove Processes\n5. Exit");

            switch (sc.nextInt()) {
                case 1:
                    System.out.println("How many more servers: ");
                    servers += sc.nextInt();
                    break;

                case 2:
                    System.out.println("How many servers to remove: ");
                    servers -= sc.nextInt();
                    break;

                case 3:
                    System.out.println("How many more processes: ");
                    processes += sc.nextInt();
                    break;

                case 4:
                    System.out.println("How many processes to remove: ");
                    processes -= sc.nextInt();
                    break;

                case 5:
                    return;

                default:
                    System.out.println("Invalid choice. Please select a valid option.");
                    break;
            }
        }
    }
}