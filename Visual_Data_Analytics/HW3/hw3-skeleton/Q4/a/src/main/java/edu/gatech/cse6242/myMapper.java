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
    extends Mapper<LongWritable, Text, Text, IntWritable>{

        public void map(LongWritable key, Text lineText, Context context) throws IOException, InterruptedException{

            String line = lineText.toString();
            String PULoc = line.split("\t")[0];
            String DOLoc = line.split("\t")[1];
            
            Text outNode = new Text(PULoc);
            Text inNode = new Text(DOLoc);

            IntWritable out = new IntWritable(0);
            IntWritable in = new IntWritable(1);

            context.write(outNode, out);
            context.write(inNode, in);


        }
    }
