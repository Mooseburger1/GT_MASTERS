import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
public class MaxPayment {
  public static void main(String[] args) throws Exception {
    if (args.length != 2) {
      System.err.println("Usage: MaxPayment <input path> <output path>");
      System.exit(-1);
    }
    // create a Hadoop job and set the main class
    Job job = Job.getInstance();
    job.setJarByClass(MaxPayment.class);
    job.setJobName("MaxPayment");
    // set the input and output path
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    // set the Mapper and Reducer class
    job.setMapperClass(MaxPaymentMapper.class);
    job.setReducerClass(MaxPaymentReducer.class);
    // specify the type of the output
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(FloatWritable.class);
    // run the job
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}