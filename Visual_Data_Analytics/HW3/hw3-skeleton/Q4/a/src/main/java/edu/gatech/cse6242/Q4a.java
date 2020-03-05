package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Q4a {

  public static void main(String[] args) throws Exception {
<<<<<<< HEAD
    String outputTempDir = args[1] + "temp";
    /* TODO: Update variable below with your gtid */
    final String gtid = "ksims35";
=======

    /* TODO: Update variable below with your gtid */
    final String gtid = "gburdell3";
>>>>>>> 43030924a565b33aa7d6a6280504b8f3a3183245

    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q4a");

    /* TODO: Needs to be implemented */
<<<<<<< HEAD
    job.setJarByClass(Q4a.class);

    job.setMapperClass(myMapper.class);
    job.setReducerClass(myReducer.class);

    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(outputTempDir));
    


    boolean success = job.waitForCompletion(true);
  
    Job job2 = Job.getInstance(conf, "Q4a");
    job2.setJarByClass(Q4a.class);
    job2.setMapperClass(myMapper2.class);
    job2.setReducerClass(myReducer2.class);
    job2.setOutputKeyClass(Text.class);
    job2.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job2, new Path(outputTempDir));
    FileOutputFormat.setOutputPath(job2, new Path(args[1]));
    System.exit(job2.waitForCompletion(true) ? 0 : 1);
    
=======

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
>>>>>>> 43030924a565b33aa7d6a6280504b8f3a3183245
  }
}
