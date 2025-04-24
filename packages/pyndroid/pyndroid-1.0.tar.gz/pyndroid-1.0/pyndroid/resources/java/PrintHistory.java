package net.example.pydroid;

public class PrintHistory {
    private int id;
    private int printerId;
    private int userId;
    private String modelName;
    private String timestamp;

    public PrintHistory(int id, int printerId, int userId, String modelName, String timestamp) {
        this.id = id;
        this.printerId = printerId;
        this.userId = userId;
        this.modelName = modelName;
        this.timestamp = timestamp;
    }

    // Getters
    public int getId() { return id; }
    public int getPrinterId() { return printerId; }
    public int getUserId() { return userId; }
    public String getModelName() { return modelName; }
    public String getTimestamp() { return timestamp; }
}