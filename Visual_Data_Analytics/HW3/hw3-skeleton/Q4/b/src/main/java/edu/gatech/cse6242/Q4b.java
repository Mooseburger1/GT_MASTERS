package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Q4b {

  public static void main(String[] args) throws Exception {
    /* TODO: Update variable below with your gtid */
<<<<<<< HEAD
    final String gtid = "ksims35";
=======
    final String gtid = "gburdell3";
>>>>>>> 43030924a565b33aa7d6a6280504b8f3a3183245

    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q4b");

    /* TODO: Needs to be implemented */
<<<<<<< HEAD
    job.setJarByClass(Q4b.class);

    job.setMapperClass(myMapper.class);
    job.setReducerClass(myReducer.class);

    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(FloatWritable.class);

=======
>>>>>>> 43030924a565b33aa7d6a6280504b8f3a3183245

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
