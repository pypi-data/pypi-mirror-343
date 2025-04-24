package net.example.pydroid;

import android.content.Intent;
import android.database.Cursor;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import net.example.pydroid.R;
import net.example.pydroid.PrinterAdapter;
import net.example.pydroid.DatabaseHelper;
import net.example.pydroid.Printer;

import java.util.ArrayList;
import java.util.List;

public class PrintersActivity extends AppCompatActivity {
    private RecyclerView rvPrinters;
    private TextView tvNoPrinters;
    private DatabaseHelper dbHelper;
    private PrinterAdapter adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_printers);

        rvPrinters = findViewById(R.id.rvPrinters);
        tvNoPrinters = findViewById(R.id.tvNoPrinters);
        dbHelper = new DatabaseHelper(this);

        rvPrinters.setLayoutManager(new LinearLayoutManager(this));
        loadPrinters();
    }

    private void loadPrinters() {
        List<Printer> printerList = new ArrayList<>();
        Cursor cursor = dbHelper.getAllPrinters();

        if (cursor.getCount() == 0) {
            tvNoPrinters.setVisibility(View.VISIBLE);
            rvPrinters.setVisibility(View.GONE);
        } else {
            tvNoPrinters.setVisibility(View.GONE);
            rvPrinters.setVisibility(View.VISIBLE);
            while (cursor.moveToNext()) {
                int id = cursor.getInt(cursor.getColumnIndexOrThrow("id"));
                String model = cursor.getString(cursor.getColumnIndexOrThrow("model"));
                String status = cursor.getString(cursor.getColumnIndexOrThrow("status"));
                printerList.add(new Printer(id, model, status));
            }
        }
        cursor.close();

        adapter = new PrinterAdapter(printerList, printer -> {
            Intent intent = new Intent(this, HistoryActivity.class);
            intent.putExtra("printer_id", printer.getId());
            startActivity(intent);
        });
        rvPrinters.setAdapter(adapter);
    }
}