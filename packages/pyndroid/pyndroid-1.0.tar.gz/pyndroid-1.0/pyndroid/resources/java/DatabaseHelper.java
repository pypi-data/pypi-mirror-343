package net.example.pydroid;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

public class DatabaseHelper extends SQLiteOpenHelper {
    private static final String DATABASE_NAME = "PrinterManager.db";
    private static final int DATABASE_VERSION = 1;

    // Table names
    private static final String TABLE_USERS = "Users";
    private static final String TABLE_PRINTERS = "Printers";
    private static final String TABLE_PRINT_HISTORY = "PrintHistory";

    // Users table columns
    private static final String COL_USER_ID = "id";
    private static final String COL_USER_LOGIN = "login";
    private static final String COL_USER_PASSWORD = "password";

    // Printers table columns
    private static final String COL_PRINTER_ID = "id";
    private static final String COL_PRINTER_MODEL = "model";
    private static final String COL_PRINTER_STATUS = "status";

    // PrintHistory table columns
    private static final String COL_HISTORY_ID = "id";
    private static final String COL_HISTORY_PRINTER_ID = "printer_id";
    private static final String COL_HISTORY_USER_ID = "user_id";
    private static final String COL_HISTORY_MODEL_NAME = "model_name";
    private static final String COL_HISTORY_TIMESTAMP = "timestamp";

    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        // Create Users table
        db.execSQL("CREATE TABLE " + TABLE_USERS + " (" +
                COL_USER_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
                COL_USER_LOGIN + " TEXT UNIQUE, " +
                COL_USER_PASSWORD + " TEXT)");

        // Create Printers table
        db.execSQL("CREATE TABLE " + TABLE_PRINTERS + " (" +
                COL_PRINTER_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
                COL_PRINTER_MODEL + " TEXT, " +
                COL_PRINTER_STATUS + " TEXT)");

        // Create PrintHistory table
        db.execSQL("CREATE TABLE " + TABLE_PRINT_HISTORY + " (" +
                COL_HISTORY_ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
                COL_HISTORY_PRINTER_ID + " INTEGER, " +
                COL_HISTORY_USER_ID + " INTEGER, " +
                COL_HISTORY_MODEL_NAME + " TEXT, " +
                COL_HISTORY_TIMESTAMP + " TEXT, " +
                "FOREIGN KEY(" + COL_HISTORY_PRINTER_ID + ") REFERENCES " + TABLE_PRINTERS + "(" + COL_PRINTER_ID + "), " +
                "FOREIGN KEY(" + COL_HISTORY_USER_ID + ") REFERENCES " + TABLE_USERS + "(" + COL_USER_ID + "))");

        // Insert sample data
        insertSampleData(db);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_PRINT_HISTORY);
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_PRINTERS);
        db.execSQL("DROP TABLE IF EXISTS " + TABLE_USERS);
        onCreate(db);
    }

    private void insertSampleData(SQLiteDatabase db) {
        // Insert sample printers
        ContentValues printer1 = new ContentValues();
        printer1.put(COL_PRINTER_MODEL, "Creality Ender 3");
        printer1.put(COL_PRINTER_STATUS, "готов");
        db.insert(TABLE_PRINTERS, null, printer1);

        ContentValues printer2 = new ContentValues();
        printer2.put(COL_PRINTER_MODEL, "Prusa i3 MK3");
        printer2.put(COL_PRINTER_STATUS, "занят");
        db.insert(TABLE_PRINTERS, null, printer2);
    }

    // User-related methods
    public boolean registerUser(String login, String password) {
        SQLiteDatabase db = this.getWritableDatabase();
        ContentValues values = new ContentValues();
        values.put(COL_USER_LOGIN, login);
        values.put(COL_USER_PASSWORD, password);
        long result = db.insert(TABLE_USERS, null, values);
        db.close();
        return result != -1;
    }

    public boolean checkUser(String login, String password) {
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.query(TABLE_USERS, new String[]{COL_USER_ID},
                COL_USER_LOGIN + "=? AND " + COL_USER_PASSWORD + "=?",
                new String[]{login, password}, null, null, null);
        int count = cursor.getCount();
        cursor.close();
        db.close();
        return count > 0;
    }

    public boolean isLoginUnique(String login) {
        SQLiteDatabase db = this.getReadableDatabase();
        Cursor cursor = db.query(TABLE_USERS, new String[]{COL_USER_ID},
                COL_USER_LOGIN + "=?", new String[]{login}, null, null, null);
        int count = cursor.getCount();
        cursor.close();
        db.close();
        return count == 0;
    }

    // Printer-related methods
    public Cursor getAllPrinters() {
        SQLiteDatabase db = this.getReadableDatabase();
        return db.query(TABLE_PRINTERS, null, null, null, null, null, null);
    }

    // PrintHistory-related methods
    public Cursor getPrintHistory(int printerId) {
        SQLiteDatabase db = this.getReadableDatabase();
        return db.query(TABLE_PRINT_HISTORY, null, COL_HISTORY_PRINTER_ID + "=?",
                new String[]{String.valueOf(printerId)}, null, null, null);
    }
}