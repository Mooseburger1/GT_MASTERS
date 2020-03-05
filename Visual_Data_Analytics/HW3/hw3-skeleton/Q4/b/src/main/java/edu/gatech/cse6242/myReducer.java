package edu.gatech.cse6242;

import java.text.DecimalFormat;
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;




public class myReducer extends Reducer<IntWritable, FloatWritable, IntWritable, Text>{
    public void reduce(IntWritable key, Iterable<FloatWritable> values, Context context) throws IOException, InterruptedException{


        double N = 0.0;
        double total = 0.0;
        
        

        for (FloatWritable val : values){
            N ++;
            total = total + val.get();
        }

        double avg = total / N;
        String output = String.format("%.2f", avg);
        context.write(key, new Text(output));
    }
}