package edu.gatech.cse6242;

import java.text.DecimalFormat;
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;


public class myReducer extends Reducer<Text, Text, Text, Text>{
    public void reduce(Text pickupId, Iterable<Text> values, Context context) throws IOException, InterruptedException{
        int sum = 0;
        double totalFare = 0.0;

        for (Text value : values){
            String[] tokens = value.toString().split(",");
            if (tokens[2].trim() != "0"){
                double fare = Double.parseDouble(tokens[1].trim());
                if (fare > 0){
                    sum++;
                    totalFare += fare;
                }
            }
        }
        String output = String.format("%,.2f", totalFare);
        Text v = new Text(Integer.toString(sum) + "," + output);
        context.write(pickupId, v);
    }
}