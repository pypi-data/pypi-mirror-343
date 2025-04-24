import java.io.*;

class RingAlgo {
    int cood, ch, crash;
    int prc[];

    public void election(int n, int init) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        System.out.println("\nThe Coordinator Has Crashed!");
        // Ring election process
        int flag = 0;
        int current = init;
        int next = (current == n - 1) ? 0 : current + 1;
        int highestId = current; // Start with the initial process as the highest
        int newCoordinator = highestId;
        while (flag == 0) {
            System.out.println("Process " + (current + 1) + " passing its ID to next process in the ring.");
            // Send current process id to next process
            if (prc[current] == 1) { // If the process is active
                // Compare and store the highest process ID
                if (current > highestId) {
                    highestId = current;
                }
                if (prc[next] == 0) {
                    System.out.println("Process " + (current + 1) + " is sending the ID to next process.");
                    current = next;
                    next = (current == n - 1) ? 0 : current + 1;
                } else {
                    System.out.println("Process " + (current + 1) + " sent its ID to " + (next + 1));
                    current = next;
                    next = (current == n - 1) ? 0 : current + 1;
                }
            } else {
                // If process is not active, skip it
                System.out.println("Process " + (current + 1) + " is dead, skipping.");
                current = next;
                next = (current == n - 1) ? 0 : current + 1;
            }
            if (current == init) {
                flag = 1; // End the election loop after a full cycle
            }
        }
        newCoordinator = highestId; // Set the new coordinator (highest ID)
        cood = newCoordinator;
        System.out.println("\n*** New Coordinator Is Process " + cood + " ***");
    }

    public void Ring() throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        System.out.println("Enter The Number of Processes: ");
        int n = Integer.parseInt(br.readLine());
        prc = new int[n];
        crash = 0;
        for (int i = 0; i < n; i++) {
            prc[i] = 1;
        }
        cood = n;
        do {
            System.out.println("\n\t1. Crash A Process");
            System.out.println("\t2. Recover A Process");
            System.out.println("\t3. Display New Coordinator");
            System.out.println("\t4. Exit");
            ch = Integer.parseInt(br.readLine());
            switch (ch) {
                case 1:
                    System.out.println("\nEnter A Process To Crash");
                    int cp = Integer.parseInt(br.readLine());
                    if ((cp > n) || (cp < 1)) {
                        System.out.println("Invalid Process! Enter A Valid Process");
                    } else if ((prc[cp - 1] == 1) && (cood != cp)) {
                        prc[cp - 1] = 0;
                        System.out.println("\nProcess " + cp + " Has Been Crashed");
                    } else if ((prc[cp - 1] == 1) && (cood == cp)) {
                        prc[cp - 1] = 0;
                        election(n, cp - 1);
                    } else {
                        System.out.println("\nProcess " + cp + " Is Already Crashed");
                    }
                    break;
                case 2:
                    System.out.println("\nCrashed Processes Are: \n");
                    for (int i = 0; i < n; i++) {
                        if (prc[i] == 0) {
                            System.out.println(i + 1);
                            crash++;
                        }
                    }
                    System.out.println("Enter The Process You Want To Recover");
                    int rp = Integer.parseInt(br.readLine());
                    if ((rp < 1) || (rp > n)) {
                        System.out.println("\nInvalid Process. Enter A Valid ID");
                    } else if ((prc[rp - 1] == 0) && (rp > cood)) {
                        prc[rp - 1] = 1;
                        System.out.println("\nProcess " + rp + " Has Recovered");
                        cood = rp;
                        System.out.println("\nProcess " + rp + " Is The New Coordinator");
                    } else if (crash == n) {
                        prc[rp - 1] = 1;
                        cood = rp;
                        System.out.println("\nProcess " + rp + " Is The New Coordinator");
                        crash--;
                    } else if ((prc[rp - 1] == 0) && (rp < cood)) {
                        prc[rp - 1] = 1;
                        System.out.println("\nProcess " + rp + " Has Recovered");
                    } else {
                        System.out.println("\nProcess " + rp + " Is Not A Crashed Process");
                    }
                    break;
                case 3:
                    System.out.println("\nCurrent Coordinator Is Process " +
                            cood);
                    break;
                case 4:
                    System.exit(0);
                    break;
                default:
                    System.out.println("\nInvalid Entry!");
                    break;
            } // end switch
        } while (ch != 4);
    } // end of Ring()

    public static void main(String args[]) throws IOException {
        RingAlgo ob = new RingAlgo();
        ob.Ring();
    }
}