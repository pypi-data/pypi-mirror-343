package net.example.pydroid;

import android.database.Cursor;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import net.example.pydroid.R;
import net.example.pydroid.HistoryAdapter;
import net.example.pydroid.DatabaseHelper;
import net.example.pydroid.PrintHistory;

import java.util.ArrayList;
import java.util.List;

public class HistoryActivity extends AppCompatActivity {
    private RecyclerView rvHistory;
    private TextView tvNoHistory;
    private DatabaseHelper dbHelper;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history);

        rvHistory = findViewById(R.id.rvHistory);
        tvNoHistory = findViewById(R.id.tvNoHistory);
        dbHelper = new DatabaseHelper(this);

        rvHistory.setLayoutManager(new LinearLayoutManager(this));
        int printerId = getIntent().getIntExtra("printer_id", -1);
        loadHistory(printerId);
    }

    private void loadHistory(int printerId) {
        List<PrintHistory> historyList = new ArrayList<>();
        Cursor cursor = dbHelper.getPrintHistory(printerId);

        if (cursor.getCount() == 0) {
            tvNoHistory.setVisibility(View.VISIBLE);
            rvHistory.setVisibility(View.GONE);
        } else {
            tvNoHistory.setVisibility(View.GONE);
            rvHistory.setVisibility(View.VISIBLE);
            while (cursor.moveToNext()) {
                int id = cursor.getInt(cursor.getColumnIndexOrThrow("id"));
                int userId = cursor.getInt(cursor.getColumnIndexOrThrow("user_id"));
                String modelName = cursor.getString(cursor.getColumnIndexOrThrow("model_name"));
                String timestamp = cursor.getString(cursor.getColumnIndexOrThrow("timestamp"));
                historyList.add(new PrintHistory(id, printerId, userId, modelName, timestamp));
            }
        }
        cursor.close();

        HistoryAdapter adapter = new HistoryAdapter(historyList);
        rvHistory.setAdapter(adapter);
    }
}