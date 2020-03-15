package edu.gatech.cse6242;

import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class myMapper2
    extends Mapper<LongWritable, Text, Text, IntWritable>{
        private static IntWritable one = new IntWritable(1);

        public void map(LongWritable key, Text lineText, Context context) throws IOException, InterruptedException{

            String line = lineText.toString();
            String nodeID = line.split("\t")[0];
            String diff = line.split("\t")[1];
            
            

            
            context.write(new Text(diff), one);


        }
    }
