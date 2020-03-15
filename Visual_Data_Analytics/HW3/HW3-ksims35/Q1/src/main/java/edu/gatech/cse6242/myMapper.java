package edu.gatech.cse6242;

import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;



public class myMapper extends Mapper<LongWritable, Text, Text, Text>{
    public void map(LongWritable key, Text lineText, Context context) throws IOException, InterruptedException{
        String[] line = lineText.toString().split(",");

        if (line.length == 4){
            String pickupID = line[0];
            String distance = line[2];
            String fare = line[3];
            context.write(new Text(pickupID), new Text("1," + fare + "," + distance));
        }
        else{
            System.out.println("Bad Entry");
        }
    }
}