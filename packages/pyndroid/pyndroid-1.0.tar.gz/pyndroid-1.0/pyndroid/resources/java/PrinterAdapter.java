package net.example.pydroid;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import net.example.pydroid.R;
import net.example.pydroid.Printer;
import java.util.List;

public class PrinterAdapter extends RecyclerView.Adapter<PrinterAdapter.PrinterViewHolder> {
    private List<Printer> printers;
    private OnPrinterClickListener listener;

    public interface OnPrinterClickListener {
        void onPrinterClick(Printer printer);
    }

    public PrinterAdapter(List<Printer> printers, OnPrinterClickListener listener) {
        this.printers = printers;
        this.listener = listener;
    }

    @NonNull
    @Override
    public PrinterViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_printer, parent, false);
        return new PrinterViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull PrinterViewHolder holder, int position) {
        Printer printer = printers.get(position);
        holder.tvPrinterId.setText(String.valueOf(printer.getId()));
        holder.tvPrinterModel.setText(printer.getModel());
        holder.tvPrinterStatus.setText(printer.getStatus());
        holder.itemView.setOnClickListener(v -> listener.onPrinterClick(printer));
    }

    @Override
    public int getItemCount() {
        return printers.size();
    }

    static class PrinterViewHolder extends RecyclerView.ViewHolder {
        TextView tvPrinterId, tvPrinterModel, tvPrinterStatus;

        public PrinterViewHolder(@NonNull View itemView) {
            super(itemView);
            tvPrinterId = itemView.findViewById(R.id.tvPrinterId);
            tvPrinterModel = itemView.findViewById(R.id.tvPrinterModel);
            tvPrinterStatus = itemView.findViewById(R.id.tvPrinterStatus);
        }
    }
}