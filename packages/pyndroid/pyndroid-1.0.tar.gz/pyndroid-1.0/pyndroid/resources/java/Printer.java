package net.example.pydroid;

public class Printer {
    private int id;
    private String model;
    private String status;

    public Printer(int id, String model, String status) {
        this.id = id;
        this.model = model;
        this.status = status;
    }

    // Getters
    public int getId() { return id; }
    public String getModel() { return model; }
    public String getStatus() { return status; }
}