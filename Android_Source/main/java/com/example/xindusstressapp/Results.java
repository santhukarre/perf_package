package com.example.xindusstressapp;

import android.util.Log;

import com.github.mikephil.charting.data.BarData;
import com.github.mikephil.charting.data.BarDataSet;
import com.github.mikephil.charting.data.BarEntry;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;


public class Results {

    int numOfRows=0, numOfCols =0;
    String xVals[] ;
    ArrayList dataSets = null;

    public ArrayList getXAxisValues() {
        ArrayList xAxis = new ArrayList();
        for (int i = 0; i < numOfCols; i++) {
            xAxis.add("Col" + Integer.toString(i));
        }
        return xAxis;
    }

    public ArrayList<BarEntry> createDataSet(String line) {
        String tokens[] = line.split(",");
        numOfCols = tokens.length;
        ArrayList<BarEntry> valueSet1 = new ArrayList<BarEntry>();
        for(int i=0; i<tokens.length; i++) {
            BarEntry v1e1 = new BarEntry(Integer.parseInt(tokens[i].trim()), i); // Jan
            valueSet1.add(v1e1);
        }
        return  valueSet1;
    }

    public void readResults() {
        Map<String, Integer> highScores = new LinkedHashMap<>();
        dataSets = new ArrayList();
        xVals = new String[10];
        String scoreFile = "results.csv";
        FileInputStream is;
        BufferedReader reader;
        final File file = new File("/data/" + scoreFile);

        if (file.exists()) {
            try {
                is = new FileInputStream(file);
                reader = new BufferedReader(new InputStreamReader(is));
                String line = null;
                try {
                    line = reader.readLine();
                    xVals[numOfRows] = Integer.toString(numOfRows);
                    numOfRows++;
                    Log.d("TEST:", "Header : "+ line);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                while(line != null){
                    try {
                        line = reader.readLine();
                        Log.d("EXAMPLE:", "Header : "+ line);
                        xVals[numOfRows] = Integer.toString(numOfRows);
                        numOfRows++;
                        parseRow(numOfRows, line, highScores);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
        }
    }

    public ArrayList getDataSet() {
        return dataSets;
    }

    public void parseRow(int numOfRows, String row, Map<String, Integer> highScores)
        throws IOException {
        if(row != null) {
    ArrayList<BarEntry> valueSet1 = createDataSet(row);
    BarDataSet barDataSet1 = new BarDataSet(valueSet1, "Brand " +Integer.toString(numOfRows));

    dataSets.add(barDataSet1);

    String[] columns = row.split(",");
    highScores.put(columns[0], Integer.valueOf(columns[1].trim()));
    }
    }
}
