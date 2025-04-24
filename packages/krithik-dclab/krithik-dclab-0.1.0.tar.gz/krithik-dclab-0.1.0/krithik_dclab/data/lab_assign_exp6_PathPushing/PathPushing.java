import java.util.ArrayList;
import java.util.List;

public class PathPushing {
    public static void main(String[] args) {
        int numProcesses = 4;
        int numResources = 3;

        Graph graph = new Graph(numProcesses, numResources);

        // Add edges to represent resource requests and allocations
        // Process 0 requests resource 0
        graph.addEdge(0, 4);
        // Process 1 requests resource 1
        graph.addEdge(1, 5);
        // Process 2 requests resource 2
        graph.addEdge(2, 6);
        // Resource 0 is allocated to process 1
        graph.addEdge(4, 1);
        // Resource 1 is allocated to process 2
        graph.addEdge(5, 2);
        // Resource 2 is allocated to process 0
        graph.addEdge(6, 0);

        // Detect deadlock
        if (graph.isDeadlock()) {
            System.out.println("Deadlock detected!");
        } else {
            System.out.println("No deadlock detected!");
        }
    }
}

class Graph {
    int numProcesses, numResources;
    List<List<Integer>> adjList;  // Use ArrayList of Lists

    // Constructor
    public Graph(int numProcesses, int numResources) {
        this.numProcesses = numProcesses;
        this.numResources = numResources;
        adjList = new ArrayList<>(numProcesses + numResources);  // Create an ArrayList of Lists
        
        // Initialize each list in the adjacency list
        for (int i = 0; i < numProcesses + numResources; i++) {
            adjList.add(new ArrayList<>());  // Initialize the list for each node
        }
    }

    // Add a directed edge to the graph
    public void addEdge(int from, int to) {
        adjList.get(from).add(to);
    }

    // Perform DFS and check for deadlock, showing path-pushing steps
    public boolean isDeadlock() {
        boolean[] visited = new boolean[numProcesses + numResources];
        boolean[] stack = new boolean[numProcesses + numResources];

        // Perform DFS for each process
        for (int process = 0; process < numProcesses; process++) {
            if (!visited[process]) {
                System.out.println("\nStarting DFS for process " + process);
                if (dfs(process, visited, stack)) {
                    return true;
                }
            }
        }
        return false;
    }

    // Depth-First Search for cycle detection (with debug output)
    private boolean dfs(int v, boolean[] visited, boolean[] stack) {
        visited[v] = true;
        stack[v] = true;

        // Debug output to show the current path
        System.out.print("Visiting: " + v + " -> ");
        for (int i = 0; i < adjList.get(v).size(); i++) {
            System.out.print(adjList.get(v).get(i) + " ");
        }
        System.out.println();

        for (int neighbor : adjList.get(v)) {
            if (!visited[neighbor]) {
                System.out.println("Exploring: " + v + " -> " + neighbor);
                if (dfs(neighbor, visited, stack)) {
                    return true;
                }
            } else if (stack[neighbor]) {
                // Cycle detected
                System.out.println("Cycle detected: " + v + " -> " + neighbor);
                return true;
            }
        }

        stack[v] = false; // Backtrack
        return false;
    }
}
