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


public class myMapper
    extends Mapper<LongWritable, Text, IntWritable, FloatWritable>{

        public void map(LongWritable key, Text lineText, Context context) throws IOException, InterruptedException{

            String line = lineText.toString();
            String count = line.split("\t")[2];
            String fare = line.split("\t")[3];
            


            IntWritable key_ = new IntWritable(Integer.parseInt(count));
            FloatWritable value = new FloatWritable(Float.parseFloat(fare));

            context.write(key_, value);
            

        }
    }
