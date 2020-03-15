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




public class myReducer extends Reducer<Text, IntWritable, Text, IntWritable>{
    public void reduce(Text nodeId, Iterable<IntWritable> directions, Context context) throws IOException, InterruptedException{


        int diff = 0;

        for (IntWritable dir : directions){
            if (dir.get() == 0){
                diff++;
            }
            else{
                diff = diff - 1;
            }
        }

        context.write(nodeId, new IntWritable(diff));
    }
}